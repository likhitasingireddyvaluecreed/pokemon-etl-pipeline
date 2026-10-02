# Base API endpoint URL
BASE_URL = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit=20"

# Request timeout in seconds
TIMEOUT = 10  # Seconds to wait before timing out a request

# HTTP Headers
DEFAULT_HEADERS = {
    "Accept": "application/json"
}


# Total number of retries before giving up on a request
RETRY_TOTAL = 3

# Exponential backoff factor (wait time = backoff_factor * (2 ^ (retry_number - 1)))
# Example: 2 -> 2s, 4s, 8s
RETRY_BACKOFF_FACTOR = 2

# HTTP status codes that trigger an automatic retry
RETRY_STATUS_FORCELIST = [429, 500, 501, 502, 503]

# Whether to respect the 'Retry-After' header sent by the server
RETRY_RESPECT_RETRY_AFTER = True

# Base stat names expected in the primary Pokémon schema
STAT_COLUMNS = [
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
]

# Numeric columns for type enforcement during cleaning
NUMERIC_COLUMNS = [
    "pokemon_id",
    "height_m",
    "weight_kg",
    "base_experience",
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
]

# Categorical columns to apply default fallback values
CATEGORICAL_COLUMNS = [
    "pokemon_name",
]

# Default string replacement for missing categorical values
DEFAULT_CATEGORICAL_FILL = "Unknown"

# Path to SQLite database file
DATABASE_PATH = "pokemon.db"

# Directory where raw landing Parquet files are stored
RAW_DIR = "raw"

# Compression algorithm for Parquet files ('snappy', 'gzip', 'zstd', 'none')
PARQUET_COMPRESSION = "snappy"

# Default primary key used across raw API payload dictionaries
DEFAULT_PRIMARY_KEY = "id"


#log file
LOG_FILE="logs/pipeline.log"

# Required columns for primary Pokémon DataFrame validation
VALIDATION_REQUIRED_COLUMNS = [
    "pokemon_id",
    "pokemon_name",
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
    "size_class",
    "special_status",
]

# Numeric columns to check for non-negative values
VALIDATION_NUMERIC_COLUMNS = [
    "height_m",
    "weight_kg",
    "base_experience",
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
]

# Allowed categorical values for validation
ALLOWED_BATTLE_STYLES = {"Offensive", "Defensive", "Balanced"}
ALLOWED_SPECIAL_STATUSES = {"Normal", "Baby", "Legendary", "Mythical"}

# Speed percentile boundaries
SPEED_PERCENTILE_MIN = 0
SPEED_PERCENTILE_MAX = 100

# Parquet resource filenames required for loading raw data
RESOURCE_POKEMON = "pokemon"
RESOURCE_SPECIES = "species"
RESOURCE_MOVES = "moves"

# Validation columns for primary Pokémon DataFrame
POKEMON_REQUIRED_COLS = [
    "pokemon_id",
    "pokemon_name",
    "height_m",
    "weight_kg",
    "base_experience",
]

POKEMON_NON_NEGATIVE_COLS = [
    "pokemon_id",
    "height_m",
    "weight_kg",
    "base_experience",
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
]

# Validation columns for Species DataFrame
SPECIES_REQUIRED_COLS = [
    "pokemon_id",
    "pokemon_category",
    "generation",
]