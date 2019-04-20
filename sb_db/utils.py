def is_registered(db_acc, discord_id):
    return db_acc.execute('''
        SELECT 
            COUNT(1) as registered
        FROM 
            player 
        WHERE 
            discord_id = %(discord_id)s''',
        {
            "discord_id": discord_id
        }
    )[0]["registered"] > 0

def get_fighter_names(db_acc):
    data = db_acc.execute('''
        SELECT 
            name
        FROM 
            fighter''',
        {}
    )
    fighter_names = [data[i]["name"] for i in range(0,len(data))]
    
    return fighter_names