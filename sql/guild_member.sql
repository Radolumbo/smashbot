-- Stores who is registered in which servers (relationship between player and guild (no table currently))

CREATE TABLE guild_member
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_discord_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    FOREIGN KEY (player_discord_id)
        REFERENCES player(discord_id)
);