-- 4/29/2019 -- Adding support for "Pockets" + costumes
ALTER TABLE player.player_fighter ADD COLUMN is_pocket      BOOLEAN DEFAULT FALSE;
ALTER TABLE player.player_fighter ADD COLUMN costume_number INT DEFAULT 0; 