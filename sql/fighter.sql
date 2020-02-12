CREATE TABLE fighter.fighter
(
    id SERIAL  PRIMARY KEY,
    name VARCHAR(255) NULL, 
    weight INT NULL,
    echo_of_id INT NULL
);

INSERT INTO fighter.fighter
    (name)
VALUES
    ('Mario'), 
    ('Donkey Kong'), 
    ('Link'), 
    ('Samus'), 
    ('Dark Samus'), 
    ('Yoshi'), 
    ('Kirby'), 
    ('Fox'), 
    ('Pikachu'), 
    ('Luigi'), 
    ('Ness'), 
    ('Captain Falcon'), 
    ('Jigglypuff'), 
    ('Peach'), 
    ('Daisy'), 
    ('Bowser'), 
    ('Ice Climbers'), 
    ('Sheik'), 
    ('Zelda'), 
    ('Dr. Mario'), 
    ('Pichu'), 
    ('Falco'), 
    ('Marth'), 
    ('Lucina'), 
    ('Young Link'), 
    ('Ganondorf'), 
    ('Mewtwo'), 
    ('Roy'), 
    ('Chrom'), 
    ('Mr. Game & Watch'), 
    ('Meta Knight'), 
    ('Pit'), 
    ('Dark Pit'), 
    ('Zero Suit Samus'), 
    ('Wario'), 
    ('Snake'), 
    ('Ike'), 
    ('Pokémon Trainer'), 
    ('Diddy Kong'), 
    ('Lucas'), 
    ('Sonic'), 
    ('King Dedede'), 
    ('Olimar'), 
    ('Lucario'), 
    ('R.O.B.'), 
    ('Toon Link'), 
    ('Wolf'), 
    ('Villager'), 
    ('Mega Man'), 
    ('Wii Fit Trainer'), 
    ('Rosalina & Luma'), 
    ('Little Mac'), 
    ('Greninja'), 
    ('Mii Brawler'), 
    ('Mii Swordfighter'), 
    ('Mii Gunner'), 
    ('Palutena'), 
    ('Pac-Man'), 
    ('Robin'), 
    ('Shulk'), 
    ('Bowser Jr.'), 
    ('Duck Hunt'), 
    ('Ryu'), 
    ('Ken'), 
    ('Cloud'), 
    ('Corrin'), 
    ('Bayonetta'), 
    ('Inkling'), 
    ('Ridley'), 
    ('Simon'), 
    ('Richter'), 
    ('King K. Rool'), 
    ('Isabelle'), 
    ('Incineroar');

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