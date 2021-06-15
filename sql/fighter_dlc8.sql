INSERT INTO fighter.fighter
    (name)
SELECT
    'Steve'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Steve');
