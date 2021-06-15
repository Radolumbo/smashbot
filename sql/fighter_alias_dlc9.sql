INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Seph'
FROM fighter.fighter
WHERE
    name = 'Sephiroth' AND
    NOT EXISTS (SELECT 1 FROM fighter.fighter_alias WHERE alias = 'Seph');
