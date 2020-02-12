-- Stores alternative ways to refer to fighters

CREATE TABLE fighter.fighter_alias
(
    id SERIAL PRIMARY KEY,
    fighter_id int NOT NULL,
    alias VARCHAR(255) NULL,
    FOREIGN KEY (fighter_id)
        REFERENCES fighter.fighter(id)
);

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'DK'
FROM fighter.fighter
WHERE name = 'Donkey Kong';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'G&W'
FROM fighter.fighter
WHERE name = 'Mr. Game & Watch';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'GnW'
FROM fighter.fighter
WHERE name = 'Mr. Game & Watch';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'ZSS'
FROM fighter.fighter
WHERE name = 'Zero Suit Samus';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Banjo'
FROM fighter.fighter
WHERE name = 'Banjo & Kazooie';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'K. Rool'
FROM fighter.fighter
WHERE name = 'King K. Rool';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Bayo'
FROM fighter.fighter
WHERE name = 'Bayonetta';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Rosalina'
FROM fighter.fighter
WHERE name = 'Rosalina & Luma';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'ROB'
FROM fighter.fighter
WHERE name = 'R.O.B.';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Dedede'
FROM fighter.fighter
WHERE name = 'King Dedede';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'PT'
FROM fighter.fighter
WHERE name = 'Pokémon Trainer';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Ganon'
FROM fighter.fighter
WHERE name = 'Ganondorf';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Doc'
FROM fighter.fighter
WHERE name = 'Dr. Mario';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Sans'
FROM fighter.fighter
WHERE name = 'Mii Gunner';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Trainer'
FROM fighter.fighter
WHERE name = 'Pokémon Trainer';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Rosa'
FROM fighter.fighter
WHERE name = 'Rosalina & Luma';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'DDD'
FROM fighter.fighter
WHERE name = 'King Dedede';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'GW'
FROM fighter.fighter
WHERE name = 'Mr. Game & Watch';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Daddy'
FROM fighter.fighter
WHERE name = 'Ganondorf';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Pika'
FROM fighter.fighter
WHERE name = 'Pikachu';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Cuphead'
FROM fighter.fighter
WHERE name = 'Mii Gunner';