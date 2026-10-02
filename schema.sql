CREATE TABLE moves (

            move_id INTEGER PRIMARY KEY,

            move_name TEXT NOT NULL,

            move_type TEXT,

            power INTEGER,

            accuracy INTEGER,

            pp INTEGER,

            priority INTEGER,

            damage_class TEXT,

            generation TEXT
        );

CREATE TABLE pokemon (

            pokemon_id INTEGER PRIMARY KEY,

            name TEXT NOT NULL,

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

            size_class TEXT
        );

CREATE TABLE pokemon_abilities (

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
        );

CREATE TABLE pokemon_moves (

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
        );

CREATE TABLE pokemon_species (

            pokemon_id INTEGER PRIMARY KEY,

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

            special_status TEXT,

            FOREIGN KEY (pokemon_id)
                REFERENCES pokemon(pokemon_id)
        );

CREATE TABLE pokemon_types (

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
        );
