-- Stores who is registered in which servers (relationship between player and guild (no table currently))

CREATE TABLE player.guild_member
(
    id SERIAL PRIMARY KEY,
    player_discord_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    FOREIGN KEY (player_discord_id)
        REFERENCES player.player(discord_id)
);