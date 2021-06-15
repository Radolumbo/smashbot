INSERT INTO fighter.fighter
    (name)
SELECT
    'Terry'
WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Terry');
