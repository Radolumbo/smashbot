CREATE TABLE player.player
(
    id SERIAL PRIMARY KEY,
    discord_id BIGINT UNIQUE NOT NULL,
    switch_tag VARCHAR(255) NULL,
    switch_code VARCHAR(25) NULL
);

CREATE UNIQUE INDEX idx_player_discord_id ON player.player(discord_id);