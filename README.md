# Pokémon Data Analytics ETL Pipeline

An end-to-end ETL pipeline built using Pokémon data from the [PokéAPI](https://pokeapi.co/).

The project extracts Pokémon, species, and move data, stores the raw responses in Parquet, transforms and validates the data, and loads the processed data into a normalized SQLite database.

## Technologies & Techniques

- **Python** — pipeline development
- **Requests** — API extraction
- **ThreadPoolExecutor** — parallel API requests
- **Pandas** — data transformation and analysis
- **PyArrow / Parquet** — raw data storage
- **SQLite** — processed data storage
- **SQL** — database queries
- **Pytest** — testing
- **Jupyter Notebook** — demonstrations and analysis
- **Binder** — browser-based project demo
- **Retry & backoff** — handling temporary API failures
- **Data validation** — checking data quality and relationships

## Architecture
See the architecture here: [![Architecture diagram](https://gitdiagram.com/diagram-badge.svg)](https://gitdiagram.com/likhitasingireddyvaluecreed/pokemon-etl-pipeline?utm_source=readme&utm_medium=badge)
```text
PokéAPI
   ↓
Extract
   ↓
Raw Parquet Files
   ↓
Transform & Clean
   ↓
Validate
   ↓
SQLite Database
   ↓
Analysis / Notebooks
```

The extraction layer uses parallel requests to reduce API extraction time. Raw data is preserved separately from the processed data so that transformations can be reproduced without repeatedly calling the API.

## Project Structure

```text
pokemon-etl/
│
├── notebooks/
├── raw/
├── logs/
├── schema/
│
├── config.py
├── extract.py
├── load_raw.py
├── transform.py
├── transform_runner.py
├── validation.py
├── load.py
├── main.py
├── schema.sql
├── requirements.txt
└── pokemon.db
```

## Setup & Running

Clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd pokemon-etl
pip install -r requirements.txt
```

Run the complete pipeline:

```bash
python main.py
```

The pipeline extracts the required API data, stores the raw data in Parquet, transforms and validates it, and loads the processed data into `pokemon.db`.

Configuration such as API settings, retry behaviour, database path, and transformation-related constants is maintained in `config.py`.

## Database

The processed data is stored in a normalized SQLite database containing:

- `pokemon_species`
- `pokemon`
- `pokemon_types`
- `pokemon_abilities`
- `moves`
- `pokemon_moves`

The complete database structure, keys, relationships, constraints, and example queries are demonstrated in:

```text
notebooks/database_walkthrough.ipynb
```

## Binder Demo

The project can be run interactively in the browser using **Binder**, without setting up the project locally.

Launch the repository through Binder and open:

```text
notebooks/project_demo.ipynb
```

The notebook provides an interactive environment for exploring the project and its processed data.

Additional notebooks demonstrate the individual stages of the pipeline:

```text
notebooks/extraction_demo.ipynb
notebooks/transformation_demo.ipynb
notebooks/database_walkthrough.ipynb
```
