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
WHERE
    name = 'Donkey Kong' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'DK');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'G&W'
FROM fighter.fighter
WHERE
    name = 'Mr. Game & Watch' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'G&W');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'GnW'
FROM fighter.fighter
WHERE
    name = 'Mr. Game & Watch' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'GnW');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'ZSS'
FROM fighter.fighter
WHERE
    name = 'Zero Suit Samus' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'ZSS');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Banjo'
FROM fighter.fighter
WHERE
    name = 'Banjo & Kazooie' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Banjo');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'K. Rool'
FROM fighter.fighter
WHERE
    name = 'King K. Rool' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'K. Rool');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Bayo'
FROM fighter.fighter
WHERE
    name = 'Bayonetta' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Bayo');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Rosalina'
FROM fighter.fighter
WHERE
    name = 'Rosalina & Luma' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Rosalina');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'ROB'
FROM fighter.fighter
WHERE
    name = 'R.O.B.' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'ROB');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Dedede'
FROM fighter.fighter
WHERE
    name = 'King Dedede' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Dedede');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'PT'
FROM fighter.fighter
WHERE
    name = 'Pokémon Trainer' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'PT');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Ganon'
FROM fighter.fighter
WHERE
    name = 'Ganondorf' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Ganon');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Doc'
FROM fighter.fighter
WHERE
    name = 'Dr. Mario' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Doc');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Sans'
FROM fighter.fighter
WHERE
    name = 'Mii Gunner' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Sans');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Trainer'
FROM fighter.fighter
WHERE
    name = 'Pokémon Trainer' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Trainer');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Rosa'
FROM fighter.fighter
WHERE
    name = 'Rosalina & Luma' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Rosa');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'DDD'
FROM fighter.fighter
WHERE
    name = 'King Dedede' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'DDD');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'GW'
FROM fighter.fighter
WHERE
    name = 'Mr. Game & Watch' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'GW');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Daddy'
FROM fighter.fighter
WHERE
    name = 'Ganondorf' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Daddy');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Pika'
FROM fighter.fighter
WHERE
    name = 'Pikachu' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Pika');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Cuphead'
FROM fighter.fighter
WHERE
    name = 'Mii Gunner' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Cuphead');
