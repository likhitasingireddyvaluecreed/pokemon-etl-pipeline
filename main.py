import time
import sys

from extract import (
    create_session,
    get_pokemon,
    extract_pokemon,
    extract_species,
    get_move,
    extract_moves
)

from logger import setup_logger
from transform_runner import run_transformation
from load_raw import upsert_to_parquet

from load import (
    load_data_to_database,
)
from config import DEFAULT_PRIMARY_KEY


def main():
    """
    main file where extraction , transformation , load happens
    """

    #recording start time
    start_time = time.perf_counter()

    #setting up logger
    logger = setup_logger()

    session = None

    try:

        logger.info("=" * 70)
        logger.info("POKEMON ETL PIPELINE STARTED")
        logger.info("=" * 70)

        # SESSION creation
        session = create_session()

        # discovering pokemon dataset urls
        logger.info("Discovering Pokemon resources")
#============================= EXTRACTION ================================================================
        #from extract module getting pokemon urls
        pokemon_urls, failed_pages = get_pokemon(
            session,
            logger
        )

        logger.info(
            "Pokemon URLs discovered | count=%s",
            len(pokemon_urls)
        )

        # from extract module extracting pokemon deails from the url
        pokemon_data, failed_pokemon = extract_pokemon(
            session,
            pokemon_urls,
            logger
        )

        logger.info(
            "Pokemon extraction completed | success=%s | failed=%s",
            len(pokemon_data),
            len(failed_pokemon)
        )

        # saving the pokemon data into parquet (from load_raw module upsert_to_parquet function also ensure's idempotency)
        upsert_to_parquet(
            pokemon_data,
            "pokemon",
            primary_key=DEFAULT_PRIMARY_KEY
        )

        # discovering species data urls
        species_urls = list({
            pokemon["species"]["url"]
            for pokemon in pokemon_data
            if pokemon.get("species")
            and pokemon["species"].get("url")
        })

        logger.info(
            "Species resources discovered | count=%s",
            len(species_urls)
        )

        # from extract module we are extracting species data from the urls
        species_data, failed_species = extract_species(
            session,
            species_urls,
            logger
        )

        logger.info(
            "Species extraction completed | success=%s | failed=%s",
            len(species_data),
            len(failed_species)
        )

        # saving the pokemon species data into parquet (from load_raw module upsert_to_parquet function also ensure's idempotency)
        upsert_to_parquet(
            species_data,
            "species",
            primary_key=DEFAULT_PRIMARY_KEY
        )

        # from extract module get the move urls
        move_urls = get_move(
            pokemon_data
        )

        logger.info(
            "Move resources discovered | count=%s",
            len(move_urls)
        )

        # from extract module , extract move data from the move urls
        move_data, failed_moves = extract_moves(
            session,
            move_urls,
            logger
        )

        logger.info(
            "Move extraction completed | success=%s | failed=%s",
            len(move_data),
            len(failed_moves)
        )

        # saving the pokemon move data into parquet (from load_raw module upsert_to_parquet function also ensure's idempotency)
        upsert_to_parquet(
            move_data,
            "moves",
            primary_key=DEFAULT_PRIMARY_KEY
        )

#========================================= TRANSFORMATION ==================================================

        try:

            #from transformation_runner module get the run_transformation file where we store transformed data
            (
                pokemon_df,
                types_df,
                abilities_df,
                species_df,
                moves_df,
                pokemon_moves_df
            ) = run_transformation(
                logger
            )

            logger.info(
                "Transformation and validation completed successfully"
            )

        except Exception as e:

            logger.exception(
                "Transformation pipeline failed | error=%s",
                e
            )

            raise
#================================ LOADING ===================================================================

        logger.info(
            "Loading processed datasets into SQLite"
        )

        try:

            #load all processed data into sqlite database
            load_data_to_database(
                pokemon_df,
                types_df,
                abilities_df,
                species_df,
                moves_df,
                pokemon_moves_df
            )

            logger.info(
                "All processed datasets loaded into SQLite successfully"
            )

        except Exception as e:

            logger.exception(
                "SQLite loading failed | error=%s",
                e
            )

            raise

        # PIPELINE SUMMARY

        elapsed = time.perf_counter() - start_time

        logger.info("=" * 70)
        logger.info("PIPELINE COMPLETED")

        logger.info(
            "Pokemon | success=%s | failed=%s",
            len(pokemon_data),
            len(failed_pokemon)
        )

        logger.info(
            "Species | success=%s | failed=%s",
            len(species_data),
            len(failed_species)
        )

        logger.info(
            "Moves | success=%s | failed=%s",
            len(move_data),
            len(failed_moves)
        )

        logger.info(
            "Execution time = %.2f seconds",
            elapsed
        )

        logger.info("ETL pipeline completed successfully")
        logger.info("=" * 70)

        return True

    except Exception as e:

        elapsed = time.perf_counter() - start_time

        logger.exception(
            "Pipeline failed | error=%s",
            e
        )

        logger.info(
            "Pipeline execution time before failure = %.2f seconds",
            elapsed
        )

        logger.error("ETL pipeline failed")

        return False

    finally:

        if session is not None:
            session.close()

        logger.info("ETL pipeline execution finished")


if __name__ == "__main__":

    success = main()

    if not success:
        sys.exit(1)