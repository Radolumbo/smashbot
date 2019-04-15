CREATE TABLE player_fighter
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_discord_id BIGINT NOT NULL,
    fighter_id INT NOT NULL,
    is_main BIT DEFAULT 0,
    is_true_main BIT DEFAULT 0,
    FOREIGN KEY (player_discord_id)
        REFERENCES player(discord_id),
    FOREIGN KEY (fighter_id)
        REFERENCES fighter(id)
); 