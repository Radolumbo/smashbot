INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Alex'
FROM fighter.fighter
WHERE name = 'Steve';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Enderman'
FROM fighter.fighter
WHERE name = 'Steve';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Zombie'
FROM fighter.fighter
WHERE name = 'Steve';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Minecraft'
FROM fighter.fighter
WHERE name = 'Steve';