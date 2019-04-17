import discord
import asyncio
import mysql.connector
import sb_messaging_utils as msg_utils
from sb_messaging_utils import embed_color

help_commands = '''\
8!register
8!playerlist
8!profile
8!whois\
'''
help_descriptions = '''\
Register in player list
List players in server
View profile of player
Lookup player by switch tag\
'''
async def help(client, message, db):
    channel = message.channel
    author = message.author

    embed = discord.Embed(color=embed_color)
    embed.set_author(name='Help Text')
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name='Command', value=help_commands, inline=True)
    embed.add_field(name='Description', value=help_descriptions, inline=True)

    await channel.send(embed = embed)

async def register(client, message, db):
    channel = message.channel
    author = message.author
    cursor = db.cursor()

    # Verify user hasn't registered for this server
    query = '''
        SELECT 
            COUNT(1) 
        FROM 
            guild_member
        WHERE 
            player_discord_id = %s 
        AND 
            guild_id = %s'''
    cursor.execute(query, (author.id, channel.guild.id))
    if(cursor.fetchone()[0] > 0):
        await channel.send('{}, you\'re already registered in this channel, silly!'.format(author.mention))
        return

    # See if user has been registered at all
    query = '''
        SELECT 
            COUNT(1) 
        FROM 
            player 
        WHERE 
            discord_id = %s'''
    cursor.execute(query, (author.id))
    is_registered = (cursor.fetchone()[0] > 0)

    # Tokenize input
    tokens = message.content.split(' ')

    # First time registration, wrong number of arguments
    if(not is_registered and len(tokens) != 3):
        await channel.send('8!register usage: 8!register <swich_tag> <switch_code>')
        return
    # First time registration, wrong switch code format
    #TODO: consider switching to regex for efficiency
    elif(not is_registered and not tokens[2].lower().startswith('sw-')):
        await channel.send('Note: Switch code should look like SW-####-####-####')
        return
    # First time registration, correct input
    elif(not is_registered):
        tag = tokens[1]
        code = tokens[2]
        query = '''
            INSERT INTO 
                player (discord_id, switch_tag, switch_code) 
            VALUES
                 (%s,%s,%s)'''
        await channel.send('Registering {} as {} with Switch code {}. Is this good? (Y/N)' \
            .format(author.mention, tag, code))

        def check(m):
            return m.author == author and m.channel == channel
        try:
            msg = await client.wait_for('message', check=check, timeout=10)
            
            if(msg.content.lower() != 'y' and msg.content.lower() != 'yes'):
                await channel.send('Not registering {}.'.format(author.mention))
                return
            
            cursor.execute(query, (author.id, tag, code))    
            db.commit()
            await channel.send('Registered {.author.mention} in the player database!'.format(msg))
        except asyncio.TimeoutError:
            await channel.send('Time ran out to confirm. Try again, {}.'.format(author.mention))
            return
    
    # Already registered or just registered, add them to this channel
    query = '''
        INSERT INTO 
            guild_member (player_discord_id, guild_id) 
        VALUES 
            (%s,%s)'''
    cursor.execute(query, (author.id, channel.guild.id))
    db.commit()
    await channel.send('Registered {.author.mention} in this server!'.format(message))

async def player_list(client, message, db):
    channel = message.channel
    author = message.author
    cursor = db.cursor()
    query = '''
        SELECT 
            discord_id, switch_tag, switch_code 
        FROM 
            player p 
        INNER JOIN 
            guild_member g 
        ON 
            p.discord_id = g.player_discord_id 
        WHERE 
            g.guild_id=%s'''
    cursor.execute(query, (channel.guild.id,))
    
    names = ''
    tags = ''
    codes = ''

    for row in cursor:
        # TODO: guild is optional? maybe in PMs?
        #names += '{:<20}{:<22}\n'.format(message.guild.get_member(int(row[0])).display_name[:20], row[2])
        names += '{}\n'.format(message.guild.get_member(int(row[0])).display_name)
        #tags += '{}\n'.format(row[1])
        codes += '{}\n'.format(row[2])

    embed = discord.Embed(color=embed_color)
    embed.set_author(name='Players in {}'.format(message.guild))
    embed.set_thumbnail(url=channel.guild.icon_url)
    #embed.add_field(name='{:<45}{:<17}'.format('Name', 'Switch Code'), value='```{}```'.format(names), inline=True)
    embed.add_field(name='Name', value=names, inline=True)
    embed.add_field(name='Switch Code', value=codes, inline=True)

    await channel.send(embed=embed)

async def profile(client, message, db):
    channel = message.channel
    author = message.author

    if len(message.mentions) != 1:
        await channel.send('8!profile usage: 8!profile @mention')
        return

    mention = message.mentions[0]

    await msg_utils.send_profile(channel, db, mention)

async def who_is(client, message, db):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens) != 2:
        await channel.send('8!whois usage: 8!whois <switch_tag>')
        return

    lookup = tokens[1]

    cursor = db.cursor()
    query = '''
        SELECT 
            discord_id 
        FROM
            player p 
        INNER JOIN 
            guild_member g 
        ON 
            p.discord_id = g.player_discord_id 
        WHERE 
            g.guild_id=%s
        AND 
            p.switch_tag=%s'''
    cursor.execute(query, (channel.guild.id, lookup))
    count = 0
    await channel.send('I found the following profiles matching the Switch tag {}:'.format(lookup))
    for row in cursor:
        user = message.guild.get_member(int(row[0]))
        await msg_utils.send_profile(channel, db, user)
        count += 1
        return
    
    if(count == 0):
        await channel.send('None found.')

async def i_play(client, message, db):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens < 2):
        await channel.send('8!iplay usage: 8!whois <character>')

    query = '''
        SELECT 
            discord_id 
        FROM
            player p 
        INNER JOIN 
            guild_member g 
        ON 
            p.discord_id = g.player_discord_id 
        WHERE 
            g.guild_id=%s
        AND 
            p.switch_tag=%s'''



async def olimar_is_cool(client, message, db):
    channel = message.channel
    author = message.author
    await author.edit(nick="Dumb Idiot")
    await channel.send('You reap what you sow.')