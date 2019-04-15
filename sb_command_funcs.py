import discord
import asyncio
import mysql.connector
 
async def register(client, message, db):
    channel = message.channel
    author = message.author
    cursor = db.cursor()

    # Verify user hasn't registered for this server
    query = 'SELECT COUNT(1) FROM guild_member WHERE player_discord_id = {} AND guild_id = {}'.format(author.id, channel.guild.id)
    cursor.execute(query)
    if(cursor.fetchone()[0] > 0):
        await channel.send('{}, you\'re already registered in this channel, silly!'.format(author.mention))
        return

    # See if user has been registered at all
    query = 'SELECT COUNT(1) FROM player WHERE discord_id = {}'.format(author.id)
    cursor.execute(query)
    is_registered = (cursor.fetchone()[0] > 0)

    # Tokenize input
    tokens = message.content.split(' ')

    # First time registration, wrong number of arguments
    if(not is_registered and len(tokens) != 3):
        await channel.send('8!register usage: 8!register <tag> <code>')
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

        #TODO: VERY UNSAFE. SANITIZE INPUT.
        query = 'INSERT INTO player (discord_id, switch_tag, switch_code) VALUES ({},\'{}\',\'{}\')' \
            .format(author.id, tag, code)

        await channel.send('Registering {} as {} with Switch code {}. Is this good? (Y/N)' \
            .format(author.mention, tag, code))

        def check(m):
            return m.author == author and m.channel == channel
        try:
            msg = await client.wait_for('message', check=check, timeout=10)
            
            if(msg.content.lower() != 'y' and msg.content.lower() != 'yes'):
                await channel.send('Not registering {}.'.format(author.mention))
                return
            
            cursor.execute(query)    
            db.commit()
            await channel.send('Registered {.author.mention} in the player database!'.format(msg))
        except asyncio.TimeoutError:
            await channel.send('Time ran out to confirm. Try again, {}.'.format(author.mention))
            return
    
    # Already registered or just registered, add them to this channel
    query = 'INSERT INTO guild_member (player_discord_id, guild_id) VALUES ({},{})' \
            .format(author.id, channel.guild.id)
    cursor.execute(query)
    db.commit()
    await channel.send('Registered {.author.mention} in this server!'.format(message))

async def player_list(client, message, db):
    channel = message.channel
    cursor = db.cursor()
    cursor.execute('''
        SELECT
            discord_id, switch_tag, switch_code
        FROM player p  
        INNER JOIN guild_member g
            ON p.discord_id = g.player_discord_id
        WHERE g.guild_id = {}'''.format(channel.guild.id))
    
    txt = 'Players in server:\n\n'

    for row in cursor:
        # TODO: guild is optional? maybe in PMs?
        txt += '{}\'s tag: {} and code: {}\n'.format(message.guild.get_member(int(row[0])).display_name, row[1], row[2])

    await channel.send(txt)

async def olimar_is_cool(client, message, db):
    channel = message.channel
    author = message.author
    await author.edit(nick="Dumb Idiot")
    await channel.send('You reap what you sow.')