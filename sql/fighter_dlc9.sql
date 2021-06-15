INSERT INTO fighter.fighter
    (name)
SELECT
    'Sephiroth'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Sephiroth');
