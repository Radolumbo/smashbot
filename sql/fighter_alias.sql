-- Stores alternative ways to refer to fighters
use smashdb;

CREATE TABLE fighter_alias
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    fighter_id int NOT NULL,
    alias NVARCHAR(255) NULL,
    FOREIGN KEY (fighter_id)
        REFERENCES fighter(id)
);

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'DK'
FROM fighter
WHERE name = 'Donkey Kong';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'G&W'
FROM fighter
WHERE name = 'Mr. Game & Watch';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'GnW'
FROM fighter
WHERE name = 'Mr. Game & Watch';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'ZSS'
FROM fighter
WHERE name = 'Zero Suit Samus';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Banjo'
FROM fighter
WHERE name = 'Banjo & Kazooie';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'K. Rool'
FROM fighter
WHERE name = 'King K. Rool';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Bayo'
FROM fighter
WHERE name = 'Bayonetta';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Rosalina'
FROM fighter
WHERE name = 'Rosalina & Luma';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'ROB'
FROM fighter
WHERE name = 'R.O.B.';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Dedede'
FROM fighter
WHERE name = 'King Dedede';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'PT'
FROM fighter
WHERE name = 'Pokémon Trainer';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Ganon'
FROM fighter
WHERE name = 'Ganondorf';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Doc'
FROM fighter
WHERE name = 'Dr. Mario';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Sans'
FROM fighter
WHERE name = 'Mii Gunner';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Trainer'
FROM fighter
WHERE name = 'Pokémon Trainer';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Rosa'
FROM fighter
WHERE name = 'Rosalina & Luma';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'DDD'
FROM fighter
WHERE name = 'King Dedede';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'GW'
FROM fighter
WHERE name = 'Mr. Game & Watch';

INSERT INTO fighter_alias(fighter_id, alias)
SELECT
    id,
    'Daddy'
FROM fighter
WHERE name = 'Ganondorf';