INSERT INTO fighter.fighter
    (name)
SELECT
    'Piranha Plant'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Piranha Plant');
