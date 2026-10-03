import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from concurrent.futures import ThreadPoolExecutor
import threading
import logging

from config import (
    BASE_URL,
    TIMEOUT,
    DEFAULT_HEADERS,
    RETRY_BACKOFF_FACTOR,
    RETRY_STATUS_FORCELIST,
    RETRY_RESPECT_RETRY_AFTER
)


logger = logging.getLogger(__name__)


# Thread-local storage container for worker sessions
_thread_local = threading.local()


def create_session() -> object:
    """
    Configures and returns a requests Session instance with retry handling,
    exponential backoff, and header defaults.
    """

    session = requests.Session()

    # Accept JSON response
    session.headers.update(DEFAULT_HEADERS)

    retry_strategy = Retry(
        total=3,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_FORCELIST,
        respect_retry_after_header=RETRY_RESPECT_RETRY_AFTER
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy
    )

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


def get_worker_session():
    """
    Retrieves or initializes a thread-local HTTP session to enable
    connection pooling across tasks on the same thread.
    """

    if not hasattr(_thread_local, "session"):
        _thread_local.session = create_session()

    return _thread_local.session


def get_json(session, url) -> dict:
    """
    Executes an HTTP GET request against a target URL and parses the JSON response.

    Handles connection errors, timeouts, non-200 HTTP statuses, and invalid JSON payloads.
    Returns parsed dictionary payload on success, or None on failure.
    """

    try:

        timeout = TIMEOUT

        response = session.get(
            url,
            timeout=timeout
        )

        response.raise_for_status()

        # Validate content type header prior to decoding JSON
        if "application/json" not in response.headers.get(
            "Content-Type",
            ""
        ):
            logger.warning(
                "Response is not JSON | url=%s",
                url
            )
            return None

        return response.json()

    except requests.exceptions.ConnectionError:

        logger.error(
            "Connection failed | url=%s",
            url
        )
        return None

    except requests.exceptions.Timeout:

        logger.error(
            "Request timed out after %s seconds | url=%s",
            timeout,
            url
        )
        return None

    except requests.exceptions.HTTPError as e:

        status = e.response.status_code

        logger.error(
            "HTTP Error %s | url=%s",
            status,
            url
        )

        return None

    except requests.exceptions.JSONDecodeError:

        logger.error(
            "Invalid JSON response | url=%s",
            url
        )
        return None

    except requests.exceptions.RequestException as e:

        logger.error(
            "Request failed | url=%s | error=%s",
            url,
            e
        )
        return None


def fetch_url(url):
    """
    Worker task for ThreadPoolExecutor. Fetches a single endpoint using
    a thread-local HTTP session.
    """

    session = get_worker_session()

    data = get_json(
        session,
        url
    )

    return url, data


def extract_resources(
    urls,
    logger,
    resource_name,
    max_workers=10
):
    """
    Executes concurrent HTTP GET requests across a collection of URLs using ThreadPoolExecutor.

    Args:
        urls (list[str]): List of target endpoint URLs.
        logger (Logger): Active logging instance.
        resource_name (str): Entity name for log contextualization.
        max_workers (int): Maximum thread pool concurrency limit.

    Returns:
        tuple[list[dict], list[str]]: Extracted records and failed endpoint URLs.
    """

    data_list = []
    failed_urls = []

    total = len(urls)

    if total == 0:
        return data_list, failed_urls

    logger.info(
        "%s extraction started | total=%s | workers=%s",
        resource_name,
        total,
        max_workers
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        # executor.map preserves deterministic output ordering
        results = executor.map(
            fetch_url,
            urls
        )

        for index, (url, data) in enumerate(
            results,
            start=1
        ):

            if data is None:

                failed_urls.append(url)

                logger.error(
                    "%s extraction failed | progress=%s/%s | url=%s",
                    resource_name,
                    index,
                    total,
                    url
                )

                continue

            data_list.append(data)

            # Emit log checkpoints every 100 records or at batch completion
            if (
                index % 100 == 0
                or index == total
            ):
                logger.info(
                    "%s extraction progress | "
                    "processed=%s/%s | success=%s | failed=%s",
                    resource_name,
                    index,
                    total,
                    len(data_list),
                    len(failed_urls)
                )

    logger.info(
        "%s extraction completed | success=%s | failed=%s",
        resource_name,
        len(data_list),
        len(failed_urls)
    )

    return data_list, failed_urls


def get_pokemon(session, logger) -> list:
    """
    Traverses API pagination pages sequentially to discover all Pokemon resource URLs.
    """

    url = BASE_URL

    pokemon_urls = []
    failed_pages = []

    while url:

        data = get_json(
            session,
            url
        )

        if data is None:

            logger.error(
                "Failed to extract Pokemon page | url=%s",
                url
            )

            failed_pages.append(url)

            break

        results = data.get(
            "results",
            []
        )

        pokemon_urls.extend(
            item["url"]
            for item in results
            if item.get("url")
        )

        url = data.get("next")

    logger.info(
        "Pokemon URL discovery completed | urls=%s | failed_pages=%s",
        len(pokemon_urls),
        len(failed_pages)
    )

    return pokemon_urls, failed_pages


def extract_pokemon(
    session,
    urls,
    logger
) -> list:
    """
    Concurrently extracts detailed Pokemon entities from provided endpoint URLs.
    """

    return extract_resources(
        urls,
        logger,
        resource_name="Pokemon",
        max_workers=10
    )


def extract_species(
    session,
    urls,
    logger
):
    """
    Concurrently extracts detailed species entities from provided endpoint URLs.
    """

    return extract_resources(
        urls,
        logger,
        resource_name="Species",
        max_workers=10
    )


def get_move(pokemon_data):
    """
    Parses extracted Pokemon payloads to collect and deduplicate target move URLs.
    """

    move_urls = set()

    for pokemon in pokemon_data:

        for item in pokemon.get("moves") or []:

            move_info = item.get(
                "move"
            ) or {}

            move_url = move_info.get(
                "url"
            )

            if move_url:
                move_urls.add(
                    move_url
                )

    return sorted(move_urls)


def extract_moves(
    session,
    urls,
    logger
):
    """
    Concurrently extracts move entities from provided endpoint URLs.
    """

    return extract_resources(
        urls,
        logger,
        resource_name="Moves",
        max_workers=10
    )