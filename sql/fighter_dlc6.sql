INSERT INTO fighter.fighter
    (name)
SELECT
    'Byleth'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Byleth');
