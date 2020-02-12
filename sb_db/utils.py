from sb_constants import DB_ERROR_MSG
import sb_db.errors as dberr

async def is_registered(db_acc, discord_id, channel):
    try: 
        return db_acc.execute('''
            SELECT 
                COUNT(1) as registered
            FROM 
                player.player 
            WHERE 
                discord_id = %(discord_id)s''',
            {
                "discord_id": discord_id
            }
        )[0]["registered"] > 0
    except dberr.Error as e:
        print(e)
        # TODO: add user name
        await channel.send(DB_ERROR_MSG.format("Unknown"))
        raise

async def get_fighter_names(db_acc, channel):
    try:
        data = db_acc.execute('''
            SELECT 
                name AS alias,
                name
            FROM 
                fighter.fighter
            UNION ALL
            SELECT
                fa.alias,
                f.name
            FROM
                fighter.fighter_alias fa
            INNER JOIN
                fighter.fighter f
                ON f.id = fa.fighter_id''',
            {}
        )

        fighter_names = {data[i]["alias"]:data[i]["name"] for i in range(0,len(data))}
        
        return fighter_names
    except dberr.Error as e:
        print(e)
        #TODO: add user name
        await channel.send(DB_ERROR_MSG.format("Unknown"))
        raise