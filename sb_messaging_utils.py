import discord

from sb_constants import embed_color, DB_ERROR_MSG
from sb_other_utils import create_stitched_image, delete_image, fighter_amalgam_url
import sb_db.errors as dberr

async def send_profile(channel, db_acc, user):
    params = {"discord_id": user.id}
    rows = None
    try:
        rows = db_acc.execute('''
            SELECT
                switch_tag, switch_code
            FROM 
                player.player p
            WHERE 
                p.discord_id = %(discord_id)s''',
            params
        )
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(user.mention))
        raise

    if rows is None or len(rows) == 0:
        await channel.send('{} hasn\'t registered yet. Tell them to get on it! (8!register)'.format(user.display_name))
        return
    prof_rec = rows[0]
    tag = prof_rec["switch_tag"]
    code = prof_rec["switch_code"]

    rows = None
    # get list of fighters used
    try:
        rows = db_acc.execute('''
            SELECT
                f.id,
                f.name,
                pf.is_main,
                pf.is_true_main,
                pf.is_pocket,
                pf.costume_number
            FROM 
                fighter.fighter f
            INNER JOIN 
                player.player_fighter pf
            ON 
                pf.fighter_id = f.id
            WHERE 
                pf.player_discord_id = %(discord_id)s
            ORDER BY
                CASE WHEN pf.is_true_main THEN 1 ELSE 0 END DESC,
                CASE WHEN pf.is_main THEN 1 ELSE 0 END DESC,
                CASE WHEN pf.is_pocket THEN 1 ELSE 0 END DESC,
                f.name''', 
            {
                "discord_id": user.id
            }
        )
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(user.mention))
        raise

    fighters = [
        {
            "name": row["name"],
            "is_main": row["is_main"],
            "is_true_main": row["is_true_main"],
            "is_pocket": row["is_pocket"],
            "costume_number": row["costume_number"]
        }
        for row in rows
    ]
        
    embed = discord.Embed(color=embed_color)
    embed.set_author(name = user.display_name, icon_url=user.avatar_url)
    embed.add_field(name='Switch Tag', value=tag, inline=True)
    embed.add_field(name='Switch Code', value=code, inline=True)
    
    # If any fighters were found
    if(len(rows) > 0):
        try:
            #embed.add_field(name='Fighters', value=' ', inline=False)
            amalgam_url = create_stitched_image(fighters)
            embed.set_image(url=amalgam_url)
            embed.set_footer(text='Green "M" means "main"; Red "P" means "pocket"')
        # If creating the image fails, still post the profile just without the image
        except Exception as e:
            print(e)

    await channel.send(embed=embed)