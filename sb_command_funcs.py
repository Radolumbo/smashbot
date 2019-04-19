import discord
import asyncio
import mysql.connector

import sb_messaging_utils as msg_utils
from sb_messaging_utils import embed_color
from sb_db_utils import is_registered
from sb_other_utils import find_fighter, fighter_icon_url

help_commands = '''\
8!register <switch_tag> <switch_code>
8!update <tag|code> <value>
8!playerlist
8!profile <optional_mention>
8!whois
8!iplay [add|remove] <fighter>
8!whoplays <fighter>\
'''
help_descriptions = '''\
Register in player list
Update profile attributes
List players in server
View profile of self or mention
Lookup player by switch tag
Add/remove a fighter to/from your repertoire
Find players in this server who use a fighter\
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
            player_discord_id = %s AND 
            guild_id = %s'''
    cursor.execute(query, (author.id, channel.guild.id))
    if(cursor.fetchone()[0] > 0):
        await channel.send('{}, you\'re already registered in this channel, silly!'.format(author.mention))
        return

    # See if user has been registered at all
    is_reg = is_registered(db, author.id)

    # Tokenize input
    tokens = message.content.split(' ')

    # First time registration, wrong number of arguments
    if(not is_reg and len(tokens) != 3):
        await channel.send('8!register usage: 8!register <swich_tag> <switch_code>')
        return
    # First time registration, wrong switch code format
    #TODO: use regex to enforce more rigid structure
    elif(not is_reg and not tokens[2].lower().startswith('sw-')):
        await channel.send('Note: Switch code should look like SW-####-####-####')
        return
    # First time registration, correct input
    elif(not is_reg):
        tag = tokens[1]
        code = tokens[2].upper()
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
            msg = await client.wait_for('message', check=check, timeout=15)
            
            if(msg.content.lower() != 'y' and msg.content.lower() != 'yes' \
                 and msg.content.lower() != '8!y'  and msg.content.lower() != '8!yes'):
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

async def update(client, message, db):
    channel = message.channel
    author = message.author
    cursor = db.cursor()

    # Tokenize input
    tokens = message.content.split(' ')

    if len(tokens) < 3:
        await channel.send('8!update usage: 8!update <tag|code> <value>')
        return

    update_stmt = "SET "
    val = None

    if(tokens[1].lower() == "tag"):
        update_stmt += "switch_tag = %(val)s"
        val = ' '.join(tokens[2:])
    elif(tokens[1].lower() == "code"):
        if(len(tokens) > 3 or not tokens[2].lower().startswith('sw-')):
            await channel.send('Note: Switch code should look like SW-####-####-####')
            return
        val = tokens[2]
        update_stmt += "switch_code = %(val)s"
    else:
        await channel.send('Not sure what you\'re trying to do. Remember: 8!update usage: 8!update <tag|code> <value>')
        return

    query= '''
        UPDATE player
            ''' + update_stmt + '''
        WHERE 
            discord_id = %(discord_id)s'''

    cursor.execute(query, {"val": val, "discord_id": author.id})
    db.commit()
    await channel.send('Updated {}\'s profile.'.format(author.mention))  

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
            ON p.discord_id = g.player_discord_id 
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

    mention = None

    tokens = message.content.split(' ')
    
    # default to self, make sure no other args passed in
    if len(message.mentions) == 0 and len(tokens) == 1:
        mention = author
    elif len(message.mentions) == 1:
        mention = message.mentions[0]
    else:
        await channel.send('8!profile usage: 8!profile @optional_mention')
        return

    

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
            ON p.discord_id = g.player_discord_id 
        WHERE 
            g.guild_id=%s AND 
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

    cursor = db.cursor()

    if len(tokens) < 2:
        await channel.send('8!iplay usage: 8!iplay [add|remove] <character>')
        return

    remove_fighter = False

    # Figure out where the fighter name starts
    # to determine between 8!iplay pit and 8!iplay remove/add pit
    fighter_name_start_idx = 1

    if(tokens[1].lower() == "add"):
        fighter_name_start_idx = 2
    elif(tokens[1].lower() == "remove"):    
        fighter_name_start_idx = 2
        remove_fighter = True

    # Assume everything after is the fighter name
    test_fighter_string = ' '.join(tokens[fighter_name_start_idx:])

    fighter_name, confidence = find_fighter(db, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        await channel.send('I\'m really not sure who {} is. Remember: 8!iplay usage: 8!iplay [add/remove] <character>'.format(test_fighter_string))
        return

    if(not is_registered(db, author.id)):
        await channel.send('Please register with 8!register first!')
        return
    
    # Removing that you play this character
    if(remove_fighter):
        try:
            query = '''
                DELETE FROM
                    player_fighter 
                WHERE 
                    player_discord_id = %s AND
                    fighter_id = (SELECT id FROM fighter WHERE name=%s)'''
            cursor.execute(query, (author.id, fighter_name))
            db.commit()
        except Exception as e:
            print(e)
            await channel.send('-bzzt- CRITICAL MAL -bzzt- FUNCT -bzzt- ION. Please try again.')
            return
        await channel.send('{} does not play {}, okay.'.format(author.mention, fighter_name))
    # Adding that you play this character   
    else:
        try:
            query = '''
                INSERT INTO
                    player_fighter (player_discord_id, fighter_id, is_main, is_true_main)
                SELECT 
                    %s,
                    id as fighter_id,
                    0,
                    0
                FROM
                    fighter
                WHERE 
                    name=%s'''
            cursor.execute(query, (author.id, fighter_name))
            db.commit()
        except mysql.connector.errors.IntegrityError as e:
            if(e.errno == mysql.connector.errorcode.ER_DUP_ENTRY):
                await channel.send('I already know you play {}, {}!'.format(fighter_name, author.mention))
            else:
                print(e)
                await channel.send('-bzzt- CRITICAL MAL -bzzt- FUNCT -bzzt- ION. Please try again.')
            return
        except Exception as e:
            print(e)
            await channel.send('-bzzt- CRITICAL MAL -bzzt- FUNCT -bzzt- ION. Please try again.')
            return
        
        await channel.send('Okay, noted that {} plays {}! Cool!'.format(author.mention, fighter_name))

async def who_plays(client, message, db):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    cursor = db.cursor()

    if len(tokens) < 2:
        await channel.send('8!whoplays usage: 8!whoplays <character>')
        return

    # Assume everything after is the fighter name
    test_fighter_string = ' '.join(tokens[1:])

    fighter_name, confidence = find_fighter(db, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        await channel.send('I\'m really not sure who {} is. Remember: 8!whoplays usage: 8!whoplays <character>'.format(test_fighter_string))
        return
    
    try:
        query = '''
            SELECT
                pf.player_discord_id
            FROM
                player_fighter pf
            INNER JOIN
                fighter f
                ON f.id = pf.fighter_id
            INNER JOIN
                guild_member gm
                ON gm.player_discord_id = pf.player_discord_id
            WHERE 
                f.name=%(fighter_name)s AND
                gm.guild_id = %(guild_id)s'''
        cursor.execute(query, {"fighter_name": fighter_name, "guild_id": channel.guild.id})

      #  msg = 'The following users play {}:\n\n'.format(fighter_name)
        msg = ''
        rows = cursor.fetchall()

        # Gross but cool list generators to concatenate user names
        users = [message.guild.get_member(int(row[0])) for row in rows]
        msg += ', '.join([user.display_name for user in users])

    except Exception as e:
        print(e)
        await channel.send('-bzzt- CRITICAL MAL -bzzt- FUNCT -bzzt- ION. Please try again.')
        return
    
    embed = discord.Embed(color=embed_color, description="No one." if msg == '' else msg)
    # Regex to remove ALL special characters from fighter name, then create url
    # Example: Pokemon Trainer becomes Pokmon Trainer due to special e
    embed.set_author(name = "{} Players".format(fighter_name), icon_url=fighter_icon_url(fighter_name))
    
    #embed.add_field(name='', value=tag, inline=True)
    await channel.send(embed=embed)

async def olimar_is_cool(client, message, db):
    channel = message.channel
    author = message.author
    await author.edit(nick="Dumb Idiot")
    await channel.send('You reap what you sow.')