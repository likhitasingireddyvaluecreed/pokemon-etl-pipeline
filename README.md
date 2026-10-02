# PokeAPI Data Extraction and ETL Pipeline

This project is an ETL pipeline built using the PokeAPI dataset.

The main purpose of this project was to extract Pokémon data from an API, store the raw data, transform and validate it, load the processed data into DuckDB, and then retrieve some useful information using SQL queries.

---

## Dataset Used

The dataset used in this project is from **PokeAPI**.

The main API data used was:

* Pokémon data
* Pokémon species data
* Pokémon moves data

The raw data is kept separately from the processed data.

---

## Database Chosen

I used **DuckDB** as the database for the processed data.

The main database file is:

```text
pokemon_processed.duckdb
```

The processed tables are stored inside the:

```text
processed
```

schema.

DLT is used for loading the transformed data into DuckDB.

---

## Schema Design

The processed database contains the following tables:

```text
pokemon
pokemon_types
pokemon_abilities
pokemon_species
pokemon_varieties
types
abilities
moves
pokemon_moves
```

### Main Pokémon table

The `pokemon` table contains the main Pokémon information such as:

* Pokémon ID
* Pokémon name
* Height
* Weight
* Base experience
* HP
* Attack
* Defense
* Special Attack
* Special Defense
* Speed

It also contains the derived attributes created during transformation.

These include:

* `total_base_stats`
* `offensive_power`
* `defensive_power`
* `speed_percentile`
* `battle_style`
* `stat_specialization`
* `size_class`
* `special_status`


---

## Primary Keys

Primary keys are supplied to DLT while loading the processed data.

The keys used are:

| Table             | Primary Key                              |
| ----------------- | ---------------------------------------- |
| pokemon           | `pokemon_id`                             |
| pokemon_types     | `pokemon_id`, `type_name`                |
| pokemon_abilities | `pokemon_id`, `ability_name`             |
| pokemon_species   | `pokemon_id`                             |
| pokemon_varieties | `species_id`, `pokemon_id`               |
| types             | `type_name`                              |
| abilities         | `ability_name`                           |
| moves             | `move_id`                                |
| pokemon_moves     | `pokemon_id`, `move_id`, `version_group` |

These keys are mainly used by DLT for the merge/upsert behavior.

### Foreign Keys

The tables have columns that represent relationships between the datasets, for example:

```text
pokemon_types.pokemon_id
pokemon_abilities.pokemon_id
pokemon_moves.pokemon_id
pokemon_moves.move_id
pokemon_varieties.species_id
```

However, I did **not** explicitly create foreign-key constraints in DuckDB.

---

## Loading Strategy


The raw API data is first saved separately as Parquet.

The transformed DataFrames are then passed to DLT.

DLT uses:

```text
pipeline_name = pokemon_processed
destination = duckdb
dataset_name = processed
```

The processed data is loaded into the `processed` schema.

The loading uses batch-style DataFrame data rather than inserting every record individually.

---

## DLT

DLT is responsible for running the database loading process.

The project does not manually perform one SQL `INSERT` for every Pokémon.

The transformed DataFrames are passed to DLT, which handles the loading into DuckDB.

For retrieval, a DuckDB cursor is used to execute SQL queries and fetch the results.

---

## Idempotency Approach

DLT is configured with:

```python
write_disposition="merge"
```

and primary keys are provided for each resource.

For example:

```python
pokemon_id
```

is used as the key for the Pokémon table.

For relationship tables, composite keys are used.

This means that when the pipeline runs again, records with the same primary key can be merged instead of simply creating duplicate records.

The idempotency is therefore handled mainly at the **database loading stage through DLT merge behavior**.

---

##  Failure Scenario Tested

One failure scenario that was tested was a problem during Pokémon extraction.

The extraction function keeps track of failed URLs separately:

```text
failed_urls
```

If an individual API request fails, the URL is added to the failed list and the pipeline continues processing the remaining Pokémon instead of stopping immediately.

---

##  Schema Documentation

The project also generates schema documentation from the actual DuckDB database.

The generated files are:

```text
schema.txt
schema.sql
```

`schema.txt` contains a readable view of the tables.

`schema.sql` contains `CREATE TABLE` statements generated from the current processed database schema.

---

## Data Retrieval

The project has a `retrieve.py` file that uses a DuckDB cursor to run SQL queries against:

```text
processed.pokemon
```

Some of the analysis performed includes:

* Top 10 Pokémon by total base stats
* Top 10 Pokémon by offensive power
* Top 10 Pokémon by defensive power
* Top 10 fastest Pokémon
* Pokémon count by special status

The results are displayed in the terminal and also saved into:

```text
retrieve.txt
```

---

## 13. Important Assumptions

A few assumptions made in this project are:

* PokeAPI is the source of the Pokémon, species, and move data.
* The Pokémon ID is treated as the unique identifier for Pokémon records.
* Composite keys are used for relationship tables where one column alone is not enough to identify a record.
* The processed data is stored in DuckDB under the `processed` schema.
* DLT merge behavior is used for idempotent database loading.

---

## 14. Project Flow

The final project flow is:

```text
             PokeAPI
                |
                v
          Data Extraction
                |
                v
          Raw Parquet Data
                |
                v
       Pandas Transformations
                |
                v
          Data Validation
                |
                v
             DLT
                |
                v
          DuckDB Database
                |
                v
          SQL Retrieval
                |
                v
          retrieve.txt
```
