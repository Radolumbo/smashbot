INSERT INTO fighter.fighter_alias(fighter_id, alias)
SELECT
    id,
    'Seph'
FROM fighter.fighter
WHERE name = 'Sephiroth';