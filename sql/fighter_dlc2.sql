INSERT INTO fighter.fighter
    (name)
SELECT
    'Joker'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Joker');
