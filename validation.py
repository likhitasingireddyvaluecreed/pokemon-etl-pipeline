"""
Validation layer for the Pokémon ETL pipeline.

Validation ensures that data is structurally and logically valid
before it becomes part of the processed layer.
"""

from config import (
    ALLOWED_BATTLE_STYLES,
    ALLOWED_SPECIAL_STATUSES,
    SPEED_PERCENTILE_MAX,
    SPEED_PERCENTILE_MIN,
    VALIDATION_NUMERIC_COLUMNS,
    POKEMON_REQUIRED_COLS,
    SPECIES_REQUIRED_COLS,
    SPECIES_NON_NEGATIVE_COLS,
)


def validate_required_columns(
    df,
    required_columns
):

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing required columns: "
            f"{missing_columns}"
        )


def validate_pokemon_ids(df):

    if df["pokemon_id"].isna().any():

        raise ValueError(
            "Missing Pokémon IDs"
        )

    if (
        df["pokemon_id"] <= 0
    ).any():

        raise ValueError(
            "Invalid Pokémon ID found"
        )

    if (
        df["pokemon_id"]
        .duplicated()
        .any()
    ):

        raise ValueError(
            "Duplicate Pokémon IDs found"
        )


def validate_species_ids(df):

    if df["species_id"].isna().any():

        raise ValueError(
            "Missing Species IDs"
        )

    if (
        df["species_id"] <= 0
    ).any():

        raise ValueError(
            "Invalid Species ID found"
        )

    if (
        df["species_id"]
        .duplicated()
        .any()
    ):

        raise ValueError(
            "Duplicate Species IDs found"
        )


def validate_pokemon_species_ids(df):

    if df["species_id"].isna().any():

        raise ValueError(
            "Missing Species IDs in Pokémon table"
        )

    if (
        df["species_id"] <= 0
    ).any():

        raise ValueError(
            "Invalid Species ID found in Pokémon table"
        )


def validate_pokemon_names(df):

    if df["pokemon_name"].isna().any():

        raise ValueError(
            "Missing Pokémon names"
        )

    if (
        df["pokemon_name"]
        .str.strip()
        .eq("")
        .any()
    ):

        raise ValueError(
            "Empty Pokémon names found"
        )


def validate_numeric_values(df):

    columns = VALIDATION_NUMERIC_COLUMNS

    for column in columns:

        values = df[column].dropna()

        if (values < 0).any():

            raise ValueError(
                f"Negative value found "
                f"in {column}"
            )


def validate_species_numeric_values(df):

    columns = SPECIES_NON_NEGATIVE_COLS

    for column in columns:

        values = df[column].dropna()

        if (values < 0).any():

            raise ValueError(
                f"Negative value found "
                f"in {column}"
            )


def validate_total_stats(df):

    expected = (
        df["hp"] +
        df["attack"] +
        df["defense"] +
        df["special_attack"] +
        df["special_defense"] +
        df["speed"]
    )

    if not (
        df["total_base_stats"]
        .equals(expected)
    ):

        raise ValueError(
            "Incorrect total_base_stats values"
        )


def validate_speed_percentile(df):

    if (
        (df["speed_percentile"] < SPEED_PERCENTILE_MIN) |
        (df["speed_percentile"] > SPEED_PERCENTILE_MAX)
    ).any():

        raise ValueError(
            "Invalid speed percentile"
        )


def validate_battle_style(df):

    allowed = ALLOWED_BATTLE_STYLES

    invalid = (
        set(df["battle_style"]) -
        allowed
    )

    if invalid:

        raise ValueError(
            f"Invalid battle styles: "
            f"{invalid}"
        )


def validate_special_status(df):

    allowed = ALLOWED_SPECIAL_STATUSES

    invalid = (
        set(df["special_status"]) -
        allowed
    )

    if invalid:

        raise ValueError(
            f"Invalid special statuses: "
            f"{invalid}"
        )


def validate_foreign_keys(
    pokemon_df,
    types_df,
    abilities_df,
    species_df
):

    pokemon_ids = set(
        pokemon_df["pokemon_id"]
    )

    species_ids = set(
        species_df["species_id"]
    )

    pokemon_species_ids = set(
        pokemon_df["species_id"]
    )

    type_ids = set(
        types_df["pokemon_id"]
    )

    ability_ids = set(
        abilities_df["pokemon_id"]
    )

    # Pokémon → Species

    if not pokemon_species_ids.issubset(
        species_ids
    ):

        raise ValueError(
            "Pokemon table contains "
            "unknown Species IDs"
        )

    # Types → Pokémon

    if not type_ids.issubset(
        pokemon_ids
    ):

        raise ValueError(
            "Type table contains "
            "unknown Pokémon IDs"
        )

    # Abilities → Pokémon

    if not ability_ids.issubset(
        pokemon_ids
    ):

        raise ValueError(
            "Ability table contains "
            "unknown Pokémon IDs"
        )


def validate_gender_rate(df):

    valid_values = set(range(-1, 9))

    invalid = (
        set(df["gender_rate"].dropna()) -
        valid_values
    )

    if invalid:

        raise ValueError(
            f"Invalid gender_rate values: "
            f"{invalid}"
        )


def validate_data(
    df,
    species_df
):

    print("Running data validation...")

    # validate Pokémon structure

    validate_required_columns(
        df,
        POKEMON_REQUIRED_COLS
    )

    # validate Species structure

    validate_required_columns(
        species_df,
        SPECIES_REQUIRED_COLS
    )

    # validate Pokémon IDs

    validate_pokemon_ids(df)

    # validate Species IDs

    validate_species_ids(species_df)

    # validate Pokémon → Species IDs

    validate_pokemon_species_ids(df)

    # validate Pokémon names

    validate_pokemon_names(df)

    # validate Pokémon numeric values

    validate_numeric_values(df)

    # validate Species numeric values

    validate_species_numeric_values(
        species_df
    )

    validate_gender_rate(
    species_df
    )

    # validate derived Pokémon values

    validate_total_stats(df)

    validate_speed_percentile(df)

    validate_battle_style(df)

    # special status belongs to Species

    validate_special_status(
        species_df
    )

    print(
        "Main Pokémon and Species "
        "validation passed."
    )


def validate_all(
    pokemon_df,
    types_df,
    abilities_df,
    species_df
):

    validate_data(
        pokemon_df,
        species_df
    )

    validate_foreign_keys(
        pokemon_df,
        types_df,
        abilities_df,
        species_df
    )

    print(
        "All dataset relationships "
        "validated successfully."
    )