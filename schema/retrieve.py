import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# project paths

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = BASE_DIR / "pokemon.db"
RETRIEVE_FILE = BASE_DIR / "retrieve.txt"


def retrieve_data():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    # store all output that will be written to retrieve.txt
    output = []

    try:

        logger.info(
            "Connected to SQLite database | database=%s",
            DATABASE_FILE
        )

        # show available tables

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
            """
        )

        tables = cursor.fetchall()

        print("\nAVAILABLE TABLES:")

        output.append("AVAILABLE TABLES:")
        output.append("=" * 70)

        for table in tables:

            print(table)
            output.append(str(table))


        # query 1
        # top 10 pokemon by total base stats

        cursor.execute(
            """
            SELECT
                pokemon_id,
                name,
                total_base_stats
            FROM pokemon
            ORDER BY total_base_stats DESC
            LIMIT 10
            """
        )

        records = cursor.fetchall()

        print("\nTOP 10 POKEMON BY TOTAL BASE STATS:")

        output.append("")
        output.append("TOP 10 POKEMON BY TOTAL BASE STATS:")
        output.append("=" * 70)

        for record in records:

            print(record)
            output.append(str(record))


        # query 2
        # top 10 pokemon by offensive power

        cursor.execute(
            """
            SELECT
                pokemon_id,
                name,
                offensive_power
            FROM pokemon
            ORDER BY offensive_power DESC
            LIMIT 10
            """
        )

        records = cursor.fetchall()

        print("\nTOP 10 POKEMON BY OFFENSIVE POWER:")

        output.append("")
        output.append("TOP 10 POKEMON BY OFFENSIVE POWER:")
        output.append("=" * 70)

        for record in records:

            print(record)
            output.append(str(record))


        # query 3
        # top 10 pokemon by defensive power

        cursor.execute(
            """
            SELECT
                pokemon_id,
                name,
                defensive_power
            FROM pokemon
            ORDER BY defensive_power DESC
            LIMIT 10
            """
        )

        records = cursor.fetchall()

        print("\nTOP 10 POKEMON BY DEFENSIVE POWER:")

        output.append("")
        output.append("TOP 10 POKEMON BY DEFENSIVE POWER:")
        output.append("=" * 70)

        for record in records:

            print(record)
            output.append(str(record))


        # query 4
        # fastest pokemon

        cursor.execute(
            """
            SELECT
                pokemon_id,
                name,
                speed,
                speed_percentile
            FROM pokemon
            ORDER BY speed DESC
            LIMIT 10
            """
        )

        records = cursor.fetchall()

        print("\nTOP 10 FASTEST POKEMON:")

        output.append("")
        output.append("TOP 10 FASTEST POKEMON:")
        output.append("=" * 70)

        for record in records:

            print(record)
            output.append(str(record))


        # query 5
        # pokemon count by special status

        cursor.execute(
            """
            SELECT
                special_status,
                COUNT(*) AS pokemon_count
            FROM pokemon_species
            GROUP BY special_status
            ORDER BY pokemon_count DESC
            """
        )

        records = cursor.fetchall()

        print("\nPOKEMON COUNT BY SPECIAL STATUS:")

        output.append("")
        output.append("POKEMON COUNT BY SPECIAL STATUS:")
        output.append("=" * 70)

        for record in records:

            print(record)
            output.append(str(record))


       # query 6
        # show pokemon species data

        cursor.execute(
            """
            SELECT
                species_id,
                pokemon_category,
                generation,
                color,
                shape,
                habitat,
                special_status
            FROM pokemon_species LIMIT 10
            """
        )

        records = cursor.fetchall()

        print("\nPOKEMON SPECIES DATA:")

        output.append("")
        output.append("POKEMON SPECIES DATA:")
        output.append("=" * 70)

        for record in records:

            print(record)
            output.append(str(record))



        # save retrieval output to txt file

        with open(
            RETRIEVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n".join(output)
            )

        logger.info(
            "Retrieval output saved successfully | file=%s",
            RETRIEVE_FILE
        )

        logger.info(
            "Data retrieval completed successfully"
        )


    except Exception as e:

        logger.exception(
            "Data retrieval failed | error=%s",
            e
        )

        raise


    finally:

        cursor.close()

        connection.close()

        logger.info(
            "Cursor and SQLite connection closed"
        )


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO
    )

    retrieve_data()