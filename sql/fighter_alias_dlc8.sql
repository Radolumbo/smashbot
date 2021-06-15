INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Alex'
FROM fighter.fighter
WHERE
    name = 'Steve' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Alex');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Enderman'
FROM fighter.fighter
WHERE
    name = 'Steve' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Enderman');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Zombie'
FROM fighter.fighter
WHERE
    name = 'Steve' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Zombie');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Minecraft'
FROM fighter.fighter
WHERE
    name = 'Steve' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Minecraft');
