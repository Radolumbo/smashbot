-- Stores who mains which characters (relationship between player and fighter)

CREATE TABLE player.player_fighter
(
    id SERIAL PRIMARY KEY,
    player_discord_id BIGINT NOT NULL,
    fighter_id INT NOT NULL,
    is_main BOOLEAN DEFAULT FALSE,
    is_true_main BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (player_discord_id)
        REFERENCES player.player(discord_id),
    FOREIGN KEY (fighter_id)
        REFERENCES fighter.fighter(id),
    UNIQUE (player_discord_id, fighter_id)
); 