import discord
import asyncio
import mysql.connector
 
async def register(message, db):
    channel = message.channel
    author = message.author
    tokens = message.content.split(' ')

    if(len(tokens) != 3):
        await channel.send('8!register usage: 8!register <tag> <code>')
        return
    # consider switching to regex for efficiency
    elif(not tokens[2].lower().startswith('sw-')):
        await channel.send('Note: Switch code should look like SW-####-####-####')
        return

    tag = tokens[1]
    code = tokens[2]

    query = 'SELECT count(1) FROM player WHERE discord_id = {}'.format(author.id)
    cursor = db.cursor()

    cursor.execute(query)

    if(cursor.fetchone()[0] >  0):
        await channel.send('{}, you\'re already registered, silly!'.format(author.mention))
        return

    cursor.fetchall()
    cursor.close()
    cursor = db.cursor()

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
        await channel.send('Registered {.author.mention}!'.format(msg))
    except asyncio.TimeoutError:
        await channel.send('Time ran out to confirm. Try again, {}.'.format(author.mention))

async def player_list(message, db):
    channel = message.channel
    cursor = db.cursor()
    cursor.execute('SELECT discord_id, switch_tag, switch_code FROM player')
    
    txt = 'Players in server:\n\n'

    for row in cursor:
        # TODO: guild is optional? maybe in PMs?
        txt += '{}\'s tag: {} and code: {}\n'.format(message.guild.get_member(int(row[0])).display_name, row[1], row[2])

    await channel.send(txt)

async def olimar_is_cool(message, db):
    channel = message.channel
    author = message.author
    await author.edit(nick="Dumb Idiot")
    await channel.send('You reap what you sow.')