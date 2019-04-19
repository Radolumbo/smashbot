import discord

from sb_constants import embed_color
from sb_other_utils import create_stitched_image, delete_image, fighter_amalgam_url


async def send_profile(channel, db, user):
    cursor = db.cursor()
    
    params = {"discord_id": user.id}
    query= '''
        SELECT
            switch_tag, switch_code
        FROM 
            player p
        WHERE 
            p.discord_id = %(discord_id)s'''

    cursor.execute(query, params)
    row = cursor.fetchone()

    if row is None:
        await channel.send('That user hasn\'t registered yet. Get on it, {}! (8!register)'.format(user.mention))
        return

    tag = row[0]
    code = row[1]

    # get list of fighters used
    query= '''
        SELECT
            f.id, name
        FROM 
            fighter f
        INNER JOIN 
            player_fighter pf
        ON 
            pf.fighter_id = f.id
        WHERE 
            pf.player_discord_id = %(discord_id)s'''

    cursor.execute(query, {"discord_id": user.id})
    rows = cursor.fetchall()
    fighters_string = ''

    fighter_names = [row[1] for row in rows]
        
    embed = discord.Embed(color=embed_color)
    embed.set_author(name = user.display_name, icon_url=user.avatar_url)
    embed.add_field(name='Switch Tag', value=tag, inline=True)
    embed.add_field(name='Switch Code', value=code, inline=True)
    
    # If any fighters were found
    if(len(rows) > 0):
        #embed.add_field(name='Fighters', value=' ', inline=False)
        amalgam_name = create_stitched_image(fighter_names)
        embed.set_image(url=fighter_amalgam_url(amalgam_name))

    await channel.send(embed=embed)