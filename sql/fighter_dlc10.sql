INSERT INTO fighter.fighter
    (name)
SELECT
    'Pyra/Mythra'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Pyra/Mythra');
