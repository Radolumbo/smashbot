import discord
from sb_constants import embed_color

async def send_profile(channel, db, user):
    cursor = db.cursor()
    cursor.execute('''
        SELECT
            switch_tag, switch_code
        FROM player p  
        INNER JOIN guild_member g
            ON p.discord_id = g.player_discord_id
        WHERE g.guild_id = {} AND p.discord_id = {}'''.format(channel.guild.id, user.id))

    row = cursor.fetchone()
        
    embed = discord.Embed(color=embed_color)
    embed.set_author(name = user.display_name, icon_url=user.avatar_url)
    embed.add_field(name='Switch Tag', value=row[0], inline=True)
    embed.add_field(name='Switch Code', value=row[1], inline=True)

    await channel.send(embed=embed)