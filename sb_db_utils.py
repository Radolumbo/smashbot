def is_registered(db, discord_id):
    cursor = db.cursor()
    query = '''
        SELECT 
            COUNT(1) 
        FROM 
            player 
        WHERE 
            discord_id = %(discord_id)s'''
    cursor.execute(query, {"discord_id": discord_id})
    return (cursor.fetchone()[0] > 0)

def get_fighter_names(db):
    cursor = db.cursor()
    query = '''
        SELECT 
            name
        FROM 
            fighter'''
    cursor.execute(query)
    data = cursor.fetchall()
    fighter_names = [data[i][0] for i in range(0,len(data))]
    
    return fighter_names