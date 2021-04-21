INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Pyra'
FROM fighter.fighter
WHERE name = 'Pyra/Mythra';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Mythra'
FROM fighter.fighter
WHERE name = 'Pyra/Mythra';

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Booba'
FROM fighter.fighter
WHERE name = 'Pyra/Mythra';