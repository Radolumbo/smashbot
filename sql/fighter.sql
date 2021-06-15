CREATE TABLE fighter.fighter
(
    id SERIAL  PRIMARY KEY,
    name VARCHAR(255) NULL,
    weight INT NULL,
    echo_of_id INT NULL
);

INSERT INTO fighter.fighter
    (name)
SELECT
   'Mario'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mario')
UNION ALL
    SELECT 'Donkey Kong'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Donkey Kong')
UNION ALL
    SELECT 'Link'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Link')
UNION ALL
    SELECT 'Samus'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Samus')
UNION ALL
    SELECT 'Dark Samus'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Dark Samus')
UNION ALL
    SELECT 'Yoshi'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Yoshi')
UNION ALL
    SELECT 'Kirby'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Kirby')
UNION ALL
    SELECT 'Fox'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Fox')
UNION ALL
    SELECT 'Pikachu'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Pikachu')
UNION ALL
    SELECT 'Luigi'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Luigi')
UNION ALL
    SELECT 'Ness'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ness')
UNION ALL
    SELECT 'Captain Falcon'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Captain Falcon')
UNION ALL
    SELECT 'Jigglypuff'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Jigglypuff')
UNION ALL
    SELECT 'Peach'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Peach')
UNION ALL
    SELECT 'Daisy'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Daisy')
UNION ALL
    SELECT 'Bowser'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Bowser')
UNION ALL
    SELECT 'Ice Climbers'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ice Climbers')
UNION ALL
    SELECT 'Sheik'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Sheik')
UNION ALL
    SELECT 'Zelda'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Zelda')
UNION ALL
    SELECT 'Dr. Mario'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Dr. Mario')
UNION ALL
    SELECT 'Pichu'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Pichu')
UNION ALL
    SELECT 'Falco'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Falco')
UNION ALL
    SELECT 'Marth'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Marth')
UNION ALL
    SELECT 'Lucina'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Lucina')
UNION ALL
    SELECT 'Young Link'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Young Link')
UNION ALL
    SELECT 'Ganondorf'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ganondorf')
UNION ALL
    SELECT 'Mewtwo'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mewtwo')
UNION ALL
    SELECT 'Roy'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Roy')
UNION ALL
    SELECT 'Chrom'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Chrom')
UNION ALL
    SELECT 'Mr. Game & Watch'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mr. Game & Watch')
UNION ALL
    SELECT 'Meta Knight'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Meta Knight')
UNION ALL
    SELECT 'Pit'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Pit')
UNION ALL
    SELECT 'Dark Pit'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Dark Pit')
UNION ALL
    SELECT 'Zero Suit Samus'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Zero Suit Samus')
UNION ALL
    SELECT 'Wario'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Wario')
UNION ALL
    SELECT 'Snake'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Snake')
UNION ALL
    SELECT 'Ike'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ike')
UNION ALL
    SELECT 'Pokémon Trainer'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Pokémon Trainer')
UNION ALL
    SELECT 'Diddy Kong'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Diddy Kong')
UNION ALL
    SELECT 'Lucas'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Lucas')
UNION ALL
    SELECT 'Sonic'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Sonic')
UNION ALL
    SELECT 'King Dedede'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'King Dedede')
UNION ALL
    SELECT 'Olimar'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Olimar')
UNION ALL
    SELECT 'Lucario'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Lucario')
UNION ALL
    SELECT 'R.O.B.'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'R.O.B.')
UNION ALL
    SELECT 'Toon Link'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Toon Link')
UNION ALL
    SELECT 'Wolf'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Wolf')
UNION ALL
    SELECT 'Villager'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Villager')
UNION ALL
    SELECT 'Mega Man'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mega Man')
UNION ALL
    SELECT 'Wii Fit Trainer'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Wii Fit Trainer')
UNION ALL
    SELECT 'Rosalina & Luma'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Rosalina & Luma')
UNION ALL
    SELECT 'Little Mac'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Little Mac')
UNION ALL
    SELECT 'Greninja'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Greninja')
UNION ALL
    SELECT 'Mii Brawler'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mii Brawler')
UNION ALL
    SELECT 'Mii Swordfighter'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mii Swordfighter')
UNION ALL
    SELECT 'Mii Gunner'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Mii Gunner')
UNION ALL
    SELECT 'Palutena'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Palutena')
UNION ALL
    SELECT 'Pac-Man'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Pac-Man')
UNION ALL
    SELECT 'Robin'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Robin')
UNION ALL
    SELECT 'Shulk'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Shulk')
UNION ALL
    SELECT 'Bowser Jr.'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Bowser Jr.')
UNION ALL
    SELECT 'Duck Hunt'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Duck Hunt')
UNION ALL
    SELECT 'Ryu'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ryu')
UNION ALL
    SELECT 'Ken'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ken')
UNION ALL
    SELECT 'Cloud'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Cloud')
UNION ALL
    SELECT 'Corrin'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Corrin')
UNION ALL
    SELECT 'Bayonetta'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Bayonetta')
UNION ALL
    SELECT 'Inkling'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Inkling')
UNION ALL
    SELECT 'Ridley'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Ridley')
UNION ALL
    SELECT 'Simon'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Simon')
UNION ALL
    SELECT 'Richter'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Richter')
UNION ALL
    SELECT 'King K. Rool'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'King K. Rool')
UNION ALL
    SELECT 'Isabelle'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Isabelle')
UNION ALL
    SELECT 'Incineroar'
    WHERE NOT EXISTS (SELECT 1 FROM fighter.fighter WHERE name = 'Incineroar');

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Dark Samus' AND
    f2.name = 'Samus';

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Daisy' AND
    f2.name = 'Peach';

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Lucina' AND
    f2.name = 'Marth';

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Chrom' AND
    f2.name = 'Roy';

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Dark Pit' AND
    f2.name = 'Pit';

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Ken' AND
    f2.name = 'Ryu';

UPDATE fighter.fighter f1
SET
    echo_of_id = f2.id
FROM
    fighter.fighter f2
WHERE
    f1.name = 'Richter' AND
    f2.name = 'Simon';
