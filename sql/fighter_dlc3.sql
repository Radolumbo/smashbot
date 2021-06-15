INSERT INTO fighter.fighter
    (name)
SELECT
    'Hero'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Hero');
