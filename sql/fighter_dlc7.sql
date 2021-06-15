INSERT INTO fighter.fighter
    (name)
SELECT
    'Min Min'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Min Min');
