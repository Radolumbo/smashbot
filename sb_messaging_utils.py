import discord

from sb_constants import embed_color, DB_ERROR_MSG
from sb_other_utils import create_stitched_image, delete_image, fighter_amalgam_url
import sb_db.errors as dberr

async def send_profile(channel, db_acc, user):
    params = {"discord_id": user.id}
    row = None
    try:
        row = db_acc.execute('''
            SELECT
                switch_tag, switch_code
            FROM 
                player p
            WHERE 
                p.discord_id = %(discord_id)s''',
            params
        )[0]
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(user.id))
        raise

    if row is None:
        await channel.send('That user hasn\'t registered yet. Get on it, {}! (8!register)'.format(user.mention))
        return

    tag = row["switch_tag"]
    code = row["switch_code"]

    rows = None
    # get list of fighters used
    try:
        rows = db_acc.execute('''
            SELECT
                f.id, name
            FROM 
                fighter f
            INNER JOIN 
                player_fighter pf
            ON 
                pf.fighter_id = f.id
            WHERE 
                pf.player_discord_id = %(discord_id)s''',
            {
                "discord_id": user.id
            }
        )
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(user.id))
        raise

    fighters_string = ''

    fighter_names = [row["name"] for row in rows]
        
    embed = discord.Embed(color=embed_color)
    embed.set_author(name = user.display_name, icon_url=user.avatar_url)
    embed.add_field(name='Switch Tag', value=tag, inline=True)
    embed.add_field(name='Switch Code', value=code, inline=True)
    
    # If any fighters were found
    if(len(rows) > 0):
        try:
            #embed.add_field(name='Fighters', value=' ', inline=False)
            amalgam_name = create_stitched_image(fighter_names)
            embed.set_image(url=fighter_amalgam_url(amalgam_name))
        # If creating the image fails, still post the profile just without the image
        except Exception as e:
            print(e)

    await channel.send(embed=embed)