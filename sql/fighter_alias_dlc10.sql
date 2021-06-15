INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Pyra'
FROM fighter.fighter
WHERE
    name = 'Pyra/Mythra' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Pyra');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Mythra'
FROM fighter.fighter
WHERE
    name = 'Pyra/Mythra' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Mythra');

INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Booba'
FROM fighter.fighter
WHERE
    name = 'Pyra/Mythra' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Booba');
