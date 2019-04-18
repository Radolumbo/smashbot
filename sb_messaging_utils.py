import discord
from sb_constants import embed_color

async def send_profile(channel, db, user):
    cursor = db.cursor()
    query= '''
        SELECT
            switch_tag, switch_code
        FROM 
            player p  
        INNER JOIN 
            guild_member g
        ON 
            p.discord_id = g.player_discord_id
        WHERE 
            g.guild_id = %s 
        AND 
            p.discord_id = %s'''

    cursor.execute(query, (channel.guild.id, user.id))
    row = cursor.fetchone()
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

    for i in range(0, len(rows)):
        name = rows[i][1]
        # not last row
        if(i < len(rows) - 1):
            fighters_string += name + ', '
        # last row
        elif(len(rows) > 1):
            fighters_string += ' and ' + name
        # only row
        else:
            fighters_string += name

        
    embed = discord.Embed(color=embed_color)
    embed.set_author(name = user.display_name, icon_url=user.avatar_url)
    embed.add_field(name='Switch Tag', value=tag, inline=True)
    embed.add_field(name='Switch Code', value=code, inline=True)
    
    # If any fighters were found
    if(len(rows) > 0):
        embed.add_field(name='Fighters', value=fighters_string, inline=False)

    await channel.send(embed=embed)