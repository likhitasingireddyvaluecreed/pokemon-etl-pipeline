import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = BASE_DIR / "pokemon.db"
SCHEMA_FILE = BASE_DIR / "schema.txt"
SQL_SCHEMA_FILE = BASE_DIR / "schema.sql"


# --------------------------------------------------
# Generate schema
# --------------------------------------------------

def generate_schema():

    connection = sqlite3.connect(DATABASE_FILE)

    try:

        logger.info(
            "Connected to SQLite database | database=%s",
            DATABASE_FILE
        )

        # Enable foreign-key information
        connection.execute("PRAGMA foreign_keys = ON")

        # --------------------------------------------------
        # Get tables
        # --------------------------------------------------

        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        ).fetchall()

        print("\nAVAILABLE TABLES:")

        for table in tables:
            print(table[0])

        if not tables:

            logger.warning(
                "No tables found in SQLite database"
            )

            return

        schema_output = []
        sql_output = []

        # --------------------------------------------------
        # Process every table
        # --------------------------------------------------

        for table in tables:

            table_name = table[0]

            # ----------------------------------------------
            # Table information
            # ----------------------------------------------

            columns = connection.execute(
                f'PRAGMA table_info("{table_name}")'
            ).fetchall()

            foreign_keys = connection.execute(
                f'PRAGMA foreign_key_list("{table_name}")'
            ).fetchall()

            # ----------------------------------------------
            # Text schema
            # ----------------------------------------------

            schema_output.append("")
            schema_output.append("=" * 80)
            schema_output.append(f"TABLE: {table_name}")
            schema_output.append("=" * 80)

            schema_output.append(
                f"{'COLUMN':<30}"
                f"{'TYPE':<20}"
                f"{'NULLABLE':<12}"
                f"{'PRIMARY KEY'}"
            )

            schema_output.append("-" * 80)

            for column in columns:

                column_name = column[1]
                data_type = column[2]
                not_null = column[3]
                primary_key = column[5]

                nullable = (
                    "NO"
                    if not_null
                    else "YES"
                )

                schema_output.append(
                    f"{column_name:<30}"
                    f"{data_type:<20}"
                    f"{nullable:<12}"
                    f"{'YES' if primary_key else 'NO'}"
                )

            # ----------------------------------------------
            # Foreign keys
            # ----------------------------------------------

            if foreign_keys:

                schema_output.append("")
                schema_output.append("FOREIGN KEYS:")
                schema_output.append("-" * 40)

                for foreign_key in foreign_keys:

                    referenced_table = foreign_key[2]
                    column_name = foreign_key[3]
                    referenced_column = foreign_key[4]

                    schema_output.append(
                        f"{column_name} -> "
                        f"{referenced_table}."
                        f"{referenced_column}"
                    )

            # ----------------------------------------------
            # CREATE TABLE statement
            # ----------------------------------------------

            create_statement = connection.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = ?
                """,
                (table_name,)
            ).fetchone()

            if create_statement:

                sql_output.append(
                    create_statement[0] + ";"
                )

                sql_output.append("")

        # --------------------------------------------------
        # Create output
        # --------------------------------------------------

        schema_text = "\n".join(schema_output)
        schema_sql = "\n".join(sql_output)

        print("\n" + schema_text)

        # --------------------------------------------------
        # Save schema.txt
        # --------------------------------------------------

        with open(
            SCHEMA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(schema_text)

        # --------------------------------------------------
        # Save schema.sql
        # --------------------------------------------------

        with open(
            SQL_SCHEMA_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(schema_sql)

        logger.info(
            "Schema text saved successfully | file=%s",
            SCHEMA_FILE
        )

        logger.info(
            "Schema SQL saved successfully | file=%s",
            SQL_SCHEMA_FILE
        )

    except Exception as e:

        logger.exception(
            "Schema generation failed | error=%s",
            e
        )

        raise

    finally:

        connection.close()

        logger.info(
            "SQLite connection closed"
        )


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO
    )

    generate_schema()