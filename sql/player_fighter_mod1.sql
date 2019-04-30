-- 4/29/2019 -- Adding support for "Pockets" + costumes
ALTER TABLE player_fighter ADD COLUMN is_pocket      BIT DEFAULT 0;
ALTER TABLE player_fighter ADD COLUMN costume_number INT DEFAULT 0; 