import sqlite3
import logging
import pandas as pd
from config import DATABASE_PATH 
logger = logging.getLogger(__name__)


DATABASE_PATH = DATABASE_PATH


# database connection

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    logger.info(
        "Connecting to SQLite database | database=%s",
        DATABASE_PATH
    )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    # enable foreign key enforcement
    conn.execute(
        "PRAGMA foreign_keys = ON"
    )

    return conn


# create database tables

def create_tables(conn):
    """
    Create all normalized database tables.
    """

    cursor = conn.cursor()

    logger.info(
        "Creating SQLite database tables"
    )

    # pokemon table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon (

            pokemon_id INTEGER PRIMARY KEY,

            species_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            form_name TEXT,

            is_default_form INTEGER,

            height_m REAL CHECK (
                height_m >= 0
            ),

            weight_kg REAL CHECK (
                weight_kg >= 0
            ),

            base_experience INTEGER CHECK (
                base_experience IS NULL
                OR base_experience >= 0
            ),

            hp INTEGER CHECK (
                hp IS NULL OR hp >= 0
            ),

            attack INTEGER CHECK (
                attack IS NULL OR attack >= 0
            ),

            defense INTEGER CHECK (
                defense IS NULL OR defense >= 0
            ),

            special_attack INTEGER CHECK (
                special_attack IS NULL
                OR special_attack >= 0
            ),

            special_defense INTEGER CHECK (
                special_defense IS NULL
                OR special_defense >= 0
            ),

            speed INTEGER CHECK (
                speed IS NULL OR speed >= 0
            ),

            total_base_stats INTEGER,

            offensive_power INTEGER,

            defensive_power INTEGER,

            speed_percentile REAL,

            battle_style TEXT,

            stat_specialization TEXT,

            size_class TEXT,

            FOREIGN KEY (species_id)
            REFERENCES pokemon_species(species_id)
        )
        """
    )

    # pokemon species table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon_species (

            species_id INTEGER PRIMARY KEY,

            pokemon_category TEXT,

            generation TEXT,

            color TEXT,

            shape TEXT,

            habitat TEXT,

            capture_rate INTEGER CHECK (
                capture_rate IS NULL
                OR capture_rate >= 0
            ),

            base_happiness INTEGER CHECK (
                base_happiness IS NULL
                OR base_happiness >= 0
            ),

            growth_rate TEXT,

            gender_rate INTEGER,

            hatch_counter INTEGER CHECK (
                hatch_counter IS NULL
                OR hatch_counter >= 0
            ),

            egg_group_1 TEXT,

            egg_group_2 TEXT,

            is_baby INTEGER,

            is_legendary INTEGER,

            is_mythical INTEGER,

            special_status TEXT
        )
        """
    )

    # pokemon types table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon_types (

            pokemon_id INTEGER NOT NULL,

            type_name TEXT NOT NULL,

            slot INTEGER NOT NULL,

            PRIMARY KEY (
                pokemon_id,
                slot
            ),

            UNIQUE (
                pokemon_id,
                type_name
            ),

            FOREIGN KEY (pokemon_id)
                REFERENCES pokemon(pokemon_id)
        )
        """
    )

    # pokemon abilities table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon_abilities (

            pokemon_id INTEGER NOT NULL,

            ability_name TEXT NOT NULL,

            slot INTEGER NOT NULL,

            is_hidden INTEGER NOT NULL,

            PRIMARY KEY (
                pokemon_id,
                slot
            ),

            UNIQUE (
                pokemon_id,
                ability_name
            ),

            FOREIGN KEY (pokemon_id)
                REFERENCES pokemon(pokemon_id)
        )
        """
    )

    # moves table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS moves (

            move_id INTEGER PRIMARY KEY,

            move_name TEXT NOT NULL,

            move_type TEXT,

            power INTEGER,

            accuracy INTEGER,

            pp INTEGER,

            priority INTEGER,

            damage_class TEXT,

            generation TEXT
        )
        """
    )

    # pokemon moves table

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pokemon_moves (

            pokemon_id INTEGER NOT NULL,

            move_id INTEGER NOT NULL,

            learn_method TEXT NOT NULL,

            level_learned_at INTEGER NOT NULL,

            version_group TEXT NOT NULL,

            PRIMARY KEY (
                pokemon_id,
                move_id,
                learn_method,
                level_learned_at,
                version_group
            ),

            FOREIGN KEY (pokemon_id)
                REFERENCES pokemon(pokemon_id),

            FOREIGN KEY (move_id)
                REFERENCES moves(move_id)
        )
        """
    )

    logger.info(
        "SQLite database tables created successfully"
    )


# value cleaning

def _clean_value(value):
    """
    Convert pandas NaN/NA values into Python None.

    Python None becomes SQL NULL in SQLite.
    """

    if pd.isna(value):
        return None

    return value


def _prepare_rows(df, columns):
    """
    Convert DataFrame rows into tuples suitable
    for executemany().
    """

    rows = []

    for row in df[columns].itertuples(
        index=False,
        name=None
    ):

        cleaned_row = tuple(
            _clean_value(value)
            for value in row
        )

        rows.append(
            cleaned_row
        )

    return rows


# load species data

def _load_species(cursor, df):

    columns = [
        "species_id",
        "pokemon_category",
        "generation",
        "color",
        "shape",
        "habitat",
        "capture_rate",
        "base_happiness",
        "growth_rate",
        "gender_rate",
        "hatch_counter",
        "egg_group_1",
        "egg_group_2",
        "is_baby",
        "is_legendary",
        "is_mythical",
        "special_status"
    ]

    rows = _prepare_rows(
        df,
        columns
    )

    cursor.executemany(
        """
        INSERT INTO pokemon_species (

            species_id,
            pokemon_category,
            generation,
            color,
            shape,
            habitat,
            capture_rate,
            base_happiness,
            growth_rate,
            gender_rate,
            hatch_counter,
            egg_group_1,
            egg_group_2,
            is_baby,
            is_legendary,
            is_mythical,
            special_status

        )

        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?
        )

        ON CONFLICT(species_id)
        DO UPDATE SET

            pokemon_category =
                excluded.pokemon_category,

            generation =
                excluded.generation,

            color =
                excluded.color,

            shape =
                excluded.shape,

            habitat =
                excluded.habitat,

            capture_rate =
                excluded.capture_rate,

            base_happiness =
                excluded.base_happiness,

            growth_rate =
                excluded.growth_rate,

            gender_rate =
                excluded.gender_rate,

            hatch_counter =
                excluded.hatch_counter,

            egg_group_1 =
                excluded.egg_group_1,

            egg_group_2 =
                excluded.egg_group_2,

            is_baby =
                excluded.is_baby,

            is_legendary =
                excluded.is_legendary,

            is_mythical =
                excluded.is_mythical,

            special_status =
                excluded.special_status
        """,
        rows
    )


# load pokemon data

def _load_pokemon(cursor, df):

    columns = [
        "pokemon_id",
        "species_id",
        "pokemon_name",
        "form_name",
        "is_default_form",
        "height_m",
        "weight_kg",
        "base_experience",
        "hp",
        "attack",
        "defense",
        "special_attack",
        "special_defense",
        "speed",
        "total_base_stats",
        "offensive_power",
        "defensive_power",
        "speed_percentile",
        "battle_style",
        "stat_specialization",
        "size_class"
    ]

    rows = _prepare_rows(
        df,
        columns
    )

    cursor.executemany(
        """
        INSERT INTO pokemon (

            pokemon_id,
            species_id,
            name,
            form_name,
            is_default_form,
            height_m,
            weight_kg,
            base_experience,
            hp,
            attack,
            defense,
            special_attack,
            special_defense,
            speed,
            total_base_stats,
            offensive_power,
            defensive_power,
            speed_percentile,
            battle_style,
            stat_specialization,
            size_class

        )

        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )

        ON CONFLICT(pokemon_id)
        DO UPDATE SET

            species_id = excluded.species_id,

            name = excluded.name,

            form_name = excluded.form_name,

            is_default_form =excluded.is_default_form,

            height_m = excluded.height_m,

            weight_kg = excluded.weight_kg,

            base_experience = excluded.base_experience,

            hp = excluded.hp,

            attack = excluded.attack,

            defense = excluded.defense,

            special_attack = excluded.special_attack,

            special_defense = excluded.special_defense,

            speed = excluded.speed,

            total_base_stats =
                excluded.total_base_stats,

            offensive_power =
                excluded.offensive_power,

            defensive_power =
                excluded.defensive_power,

            speed_percentile =
                excluded.speed_percentile,

            battle_style =
                excluded.battle_style,

            stat_specialization =
                excluded.stat_specialization,

            size_class =
                excluded.size_class
        """,
        rows
    )



# load pokemon type relationship

def _load_pokemon_types(cursor, df):

    columns = [
        "pokemon_id",
        "type_name",
        "slot"
    ]

    rows = _prepare_rows(
        df,
        columns
    )

    cursor.executemany(
        """
        INSERT INTO pokemon_types (

            pokemon_id,
            type_name,
            slot

        )

        VALUES (?, ?, ?)

        ON CONFLICT(
            pokemon_id,
            slot
        )

        DO UPDATE SET

            type_name =
                excluded.type_name
        """,
        rows
    )


# load pokemon ability relationship

def _load_pokemon_abilities(cursor, df):

    columns = [
        "pokemon_id",
        "ability_name",
        "slot",
        "is_hidden"
    ]

    rows = _prepare_rows(
        df,
        columns
    )

    rows = [
        (
            pokemon_id,
            ability_name,
            slot,
            int(is_hidden)
            if is_hidden is not None
            else 0
        )

        for (
            pokemon_id,
            ability_name,
            slot,
            is_hidden
        ) in rows
    ]

    cursor.executemany(
        """
        INSERT INTO pokemon_abilities (

            pokemon_id,
            ability_name,
            slot,
            is_hidden

        )

        VALUES (?, ?, ?, ?)

        ON CONFLICT(
            pokemon_id,
            slot
        )

        DO UPDATE SET

            ability_name =
                excluded.ability_name,

            is_hidden =
                excluded.is_hidden
        """,
        rows
    )


# load moves data

def _load_moves(cursor, df):

    columns = [
        "move_id",
        "move_name",
        "move_type",
        "power",
        "accuracy",
        "pp",
        "priority",
        "damage_class",
        "generation"
    ]

    rows = _prepare_rows(
        df,
        columns
    )

    cursor.executemany(
        """
        INSERT INTO moves (

            move_id,
            move_name,
            move_type,
            power,
            accuracy,
            pp,
            priority,
            damage_class,
            generation

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(move_id)

        DO UPDATE SET

            move_name =
                excluded.move_name,

            move_type =
                excluded.move_type,

            power =
                excluded.power,

            accuracy =
                excluded.accuracy,

            pp =
                excluded.pp,

            priority =
                excluded.priority,

            damage_class =
                excluded.damage_class,

            generation =
                excluded.generation
        """,
        rows
    )


# load pokemon move relationship

def _load_pokemon_moves(cursor, df):

    columns = [
        "pokemon_id",
        "move_id",
        "learn_method",
        "level_learned_at",
        "version_group"
    ]

    rows = _prepare_rows(
        df,
        columns
    )

    cursor.executemany(
        """
        INSERT INTO pokemon_moves (

            pokemon_id,
            move_id,
            learn_method,
            level_learned_at,
            version_group

        )

        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(
            pokemon_id,
            move_id,
            learn_method,
            level_learned_at,
            version_group
        )

        DO NOTHING
        """,
        rows
    )


# main database loading function

def load_data_to_database(
    pokemon_df,
    types_df,
    abilities_df,
    species_df,
    moves_df,
    pokemon_moves_df
):
    """
    Load all transformed DataFrames into SQLite
    inside one transaction.

    If any table fails, the entire transaction
    is rolled back.
    """

    conn = None

    try:

        # database connection

        conn = get_connection()

        # create tables

        create_tables(conn)

        # create cursor

        cursor = conn.cursor()

        # start transaction

        conn.execute("BEGIN")

        logger.info(
            "Starting database loading transaction"
        )

        # load species data first because main pokemon table depend on it
        
        _load_species(
            cursor,
            species_df
        )
        
        # load pokemon 

        _load_pokemon(
            cursor,
            pokemon_df
        )

        

        # load type relationship

        _load_pokemon_types(
            cursor,
            types_df
        )

        # load ability relationship

        _load_pokemon_abilities(
            cursor,
            abilities_df
        )

        # load moves

        _load_moves(
            cursor,
            moves_df
        )

        # load pokemon move relationship

        _load_pokemon_moves(
            cursor,
            pokemon_moves_df
        )

        # commit transaction

        conn.commit()

        logger.info(
            "All data loaded successfully"
        )

    except Exception as e:

        # rollback transaction

        if conn is not None:

            conn.rollback()

        logger.exception(
            "Database loading failed | error=%s",
            e
        )

        raise

    finally:

        # close database connection

        if conn is not None:

            conn.close()

            logger.info(
                "SQLite connection closed"
            )