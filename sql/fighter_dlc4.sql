INSERT INTO fighter.fighter
    (name)
SELECT
    'Banjo & Kazooie'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Banjo & Kazooie');
