CREATE TABLE player
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_id BIGINT UNIQUE NOT NULL,
    switch_tag NVARCHAR(255) NULL,
    switch_code NVARCHAR(25) NULL
);

CREATE UNIQUE INDEX idx_player_discord_id ON player(discord_id);