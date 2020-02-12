import discord
import asyncio

import sb_messaging_utils as msg_utils
from sb_constants import embed_color, DB_ERROR_MSG, base_url
from sb_db.utils import is_registered
from sb_other_utils import find_fighter, fighter_icon_url, find_users_in_guild_by_name, find_users_in_guild_by_switch_tag, random_snarky_comment, create_stitched_image
import sb_db.errors as dberr
import random

help_commands = '''\
8!register switch_tag switch_code
8!update tag|code value
8!playerlist
8!profile @mention|discord_name|switch_tag
8!whois @mention|discord_name|switch_tag
8!imain|ipocket|iplay add|remove fighter
8!remove fighter
8!whoplays fighter
8!fighter fighter
8!hmu
8!nothx
8!letsplay
8!coinflip\
'''
help_descriptions = '''\
Register in player list
Update profile attributes
List players in server
View profile of user (omit to view self)
Same as profile
Add/remove a fighter to/from your repertoire
Removes a fighter from your repertoire
Find players in this server who use a fighter
View details/costumes for a fighter
Marks you as looking for a match
Marks you as not looking for a match
Pings everyone looking for a match
Self-explanatory\
'''
async def help(client, message, db_acc):
    channel = message.channel
    author = message.author

    embed = discord.Embed(color=embed_color)
    embed.set_author(name='Help Text')
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name='Command', value=help_commands, inline=True)
    embed.add_field(name='Description', value=help_descriptions, inline=True)
    if not isinstance(channel, discord.DMChannel):
        embed.set_footer(text='Don\'t clutter your channel!  DM me to run commands.')
    await channel.send(embed = embed)
    

async def register(client, message, db_acc):
    channel = message.channel
    author = message.author
    record = None
    # Verify user hasn't registered for this server
    try:
        record = db_acc.execute('''
            SELECT 
                COUNT(1) AS registered
            FROM 
                player.guild_member
            WHERE 
                player_discord_id = %(discord_id)s AND 
                guild_id = %(guild_id)s''',
            {
                "discord_id": author.id,
                "guild_id": channel.guild.id
            }
        )[0]
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(author.mention))
        raise

    if(record["registered"] > 0):
        await channel.send('{}, you\'re already registered in this channel, silly!'.format(author.mention))
        return

    # See if user has been registered at all
    is_reg = await is_registered(db_acc, author.id, channel)

    # Tokenize input
    tokens = message.content.split(' ')

    # First time registration, wrong number of arguments
    if(not is_reg and len(tokens) != 3):
        await channel.send('8!register usage: 8!register switch_tag switch_code')
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

            try:
                db_acc.execute_update('''
                    INSERT INTO 
                        player.player (discord_id, switch_tag, switch_code) 
                    VALUES
                        (%(discord_id)s, %(tag)s, %(code)s)''',
                    {
                        "discord_id": author.id,
                        "tag": tag,
                        "code": code
                    }
                )
            except dberr.Error as e:
                print(e)
                await channel.send(DB_ERROR_MSG.format(author.mention))
                raise
            await channel.send('Registered {.author.mention} in the player database!'.format(msg))
            if not isinstance(channel, discord.DMChannel):
                await channel.send('Try DMing me to set up the rest of your profile!')
        except asyncio.TimeoutError:
            await channel.send('Time ran out to confirm. Try again, {}.'.format(author.mention))
            return
    
    # Already registered or just registered, add them to this channel
    try:
        db_acc.execute_update('''
            INSERT INTO 
                player.guild_member (player_discord_id, guild_id) 
            VALUES 
                (%(discord_id)s, %(guild_id)s)''',
            {
                "discord_id": author.id,
                "guild_id": channel.guild.id
            }
        )
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(author.mention))
        raise
    await channel.send('Registered {.author.mention} in this server!'.format(message))

async def update(client, message, db_acc):
    channel = message.channel
    author = message.author

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
    try:
        db_acc.execute_update('''
            UPDATE player
                ''' + update_stmt + '''
            WHERE 
                discord_id = %(discord_id)s''',
            {
                "val": val,
                "discord_id": author.id
            }
        )
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(author.mention))
        raise

    await channel.send('Updated {}\'s profile.'.format(author.mention))  

async def player_list(client, message, db_acc):
    channel = message.channel
    author = message.author
    rows = None

    try:
        rows = db_acc.execute('''
            SELECT 
                discord_id, switch_tag, switch_code 
            FROM 
                player.player p 
            INNER JOIN 
                player.guild_member g
                ON p.discord_id = g.player_discord_id 
            WHERE 
                g.guild_id=%(guild_id)s''',
            {
                "guild_id": channel.guild.id
            }
        )
    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(author.mention))
        raise
    
    names = ''
    tags = ''
    codes = ''

    for row in rows:
        # TODO: guild is optional? maybe in PMs?
        #names += '{:<20}{:<22}\n'.format(message.guild.get_member(int(row[0])).display_name[:20], row[2])
        names += '{}\n'.format(message.guild.get_member(int(row["discord_id"])).display_name)
        #tags += '{}\n'.format(row[1])
        codes += '{}\n'.format(row["switch_code"])

    embed = discord.Embed(color=embed_color)
    embed.set_author(name='Players in {}'.format(message.guild))
    embed.set_thumbnail(url=channel.guild.icon_url)
    #embed.add_field(name='{:<45}{:<17}'.format('Name', 'Switch Code'), value='```{}```'.format(names), inline=True)
    embed.add_field(name='Name', value=names, inline=True)
    embed.add_field(name='Switch Code', value=codes, inline=True)

    await channel.send(embed=embed)

async def profile(client, message, db_acc):
    channel = message.channel
    author = message.author

    mention = None

    tokens = message.content.split(' ')
    
    # default to self, make sure no other args passed in
    if len(message.mentions) == 0 and len(tokens) == 1:
        mention = author
    elif len(message.mentions) == 1:
        mention = message.mentions[0]
    elif len(tokens) >= 2:
        await profile_no_mention(client, message, db_acc)
        return
    else:
        # Show whois or profile based on what they wrote
        await channel.send('8!' + tokens[0] + ' usage: 8!' + tokens[0] + ' @mention|discord_name|switch_tag')
        return
    await msg_utils.send_profile(channel, db_acc, mention)

async def profile_no_mention(client, message, db_acc):
    channel = message.channel
    author = message.author

    await channel.send('No mention included, looking up by Discord name...')
    

    tokens = message.content.split(' ')

    if len(tokens) < 2:
        await channel.send('8!whois usage: 8!whois <tag>')
        return

    lookup = ' '.join(tokens[1:])

    # Look up by discord tag
    id_list = await find_users_in_guild_by_name(db_acc, message, lookup, 80)

    await channel.send('I found the following users in this server matching the name {}:'.format(lookup))
    if len(id_list) == 0:
        await channel.send('None found.')


    for id in id_list:
        user = message.guild.get_member(id)
        await msg_utils.send_profile(channel, db_acc, user)

        
    sent_message = await channel.send('*Please click the magnifying glass to search by Switch tag instead*')
    await sent_message.add_reaction("🔎")

    def check(reaction, user):
        return user == message.author and reaction.message.id == sent_message.id and str(reaction.emoji) == '🔎'

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
    # remove reaction on timeout, so user doesn't think they can still click it
    except asyncio.TimeoutError:
        await sent_message.remove_reaction("🔎", client.user)
    else:
        await channel.send('Searching by Switch tag...')

        id_list = await find_users_in_guild_by_switch_tag(db_acc, message, lookup, 80)

        await channel.send('I found the following profiles matching the Switch tag {}:'.format(lookup))
        if(len(id_list) == 0):
            await channel.send('None found.')

        for id in id_list:
            user = message.guild.get_member(id)
            await msg_utils.send_profile(channel, db_acc, user)

async def i_dont_play(client, message, db_acc):
    tokens = message.content.split(' ')

    if len(tokens) < 2:
        if send_message:
            await channel.send('8!remove usage: 8!remove <character>')
        return

    message.content = tokens[0] + " remove " + ' '.join(tokens[1:])

    await i_play(client, message, db_acc)


# send_message is a little hacky, but a VERY convenient
# way to allow us to reuse "i play" to insert mains/pockets
# when 8!imain or 8!ipocket is used before 8!iplay without spamming
async def i_play(client, message, db_acc, send_message = True):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens) < 2:
        if send_message:
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

    fighter_name, confidence = await find_fighter(db_acc, channel, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        if send_message:
            await channel.send('I\'m really not sure who {} is. Remember: 8!iplay usage:' \
                           ' Check 8!help for command usage.'.format(test_fighter_string))
        return

    if(not await is_registered(db_acc, author.id, channel)):
        if send_message:
            await channel.send('Please register with 8!register first!')
        return
    
    # Removing that you play this character
    if(remove_fighter):
        try:
            db_acc.execute_update('''
                DELETE FROM
                    player.player_fighter 
                WHERE 
                    player_discord_id = %(discord_id)s AND
                    fighter_id = (SELECT id FROM fighter.fighter WHERE name=%(name)s)''',
                {
                    "discord_id": author.id,
                    "name": fighter_name
                }
            )
        except dberr.Error as e:
            print(e)
            if send_message:
                await channel.send(DB_ERROR_MSG.format(author.mention))
            raise
        if send_message:
            await channel.send('{} does not play {}, okay.'.format(author.mention, fighter_name))
    # Adding that you play this character   
    else:
        try:
            db_acc.execute_update('''
                INSERT INTO
                    player.player_fighter (player_discord_id, fighter_id, is_main, is_true_main)
                SELECT 
                    %(discord_id)s,
                    id as fighter_id,
                    false,
                    false
                FROM
                    fighter.fighter
                WHERE 
                    name=%(name)s''',
                {
                    "discord_id": author.id,
                    "name": fighter_name
                }
            )
        except dberr.UniqueViolation as e:
            if send_message:
                await channel.send('I already know you play {}, {}!'.format(fighter_name, author.mention))
            return
        except dberr.Error as e:
            print(e)
            if send_message:
                await channel.send(DB_ERROR_MSG.format(author.mention))
            raise
        
        if send_message:
            await channel.send('Okay, noted that {} plays {}. {}'.format(author.mention, fighter_name, random_snarky_comment()))

async def i_main(client, message, db_acc):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens) < 2:
        await channel.send('8!imain usage: 8!imain [add|remove] <character>')
        return

    remove_fighter = False

    # Figure out where the fighter name starts
    # to determine between 8!imain pit and 8!imain remove/add pit
    fighter_name_start_idx = 1

    if(tokens[1].lower() == "add"):
        fighter_name_start_idx = 2
    elif(tokens[1].lower() == "remove"):    
        fighter_name_start_idx = 2
        remove_fighter = True

    if not remove_fighter:
        # First add character, if necessary
        await i_play(client, message, db_acc, False)

    # Assume everything after is the fighter name
    test_fighter_string = ' '.join(tokens[fighter_name_start_idx:])
    fighter_name, confidence = await find_fighter(db_acc, channel, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        await channel.send('I\'m really not sure who {} is. Remember: 8!imain usage: 8!imain [add/remove] <character>'.format(test_fighter_string))
        return

    if(not await is_registered(db_acc, author.id, channel)):
        await channel.send('Please register with 8!register first!')
        return
    # Adding or removing that you main this character   
    else:
        try:
            db_acc.execute_update('''
                UPDATE
                    player.player_fighter
                SET
                    is_main      = %(set_main)s,
                    is_pocket    = IF(%(set_main)s = true, false, is_pocket),
                    is_true_main = IF(%(set_main)s = true, is_true_main, false)
                WHERE 
                    player_discord_id = %(discord_id)s AND
                    fighter_id = (SELECT id FROM fighter.fighter WHERE name=%(name)s)''',
                {
                    "discord_id": author.id,
                    "name": fighter_name,
                    "set_main": 0 if remove_fighter else 1
                }
            )
        except dberr.Error as e:
            print(e)
            await channel.send(DB_ERROR_MSG.format(author.mention))
            raise
        
        if remove_fighter: 
            await channel.send('{0} does not main {1}, okay. If you want ' \
                           'to remove this character entirely, use 8!iplay remove {1}'.format(author.mention, fighter_name))
        else:
            await channel.send('I see, so {} mains {}. {}'.format(author.mention, fighter_name, random_snarky_comment()))

async def i_pocket(client, message, db_acc):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens) < 2:
        await channel.send('8!ipocket usage: 8!ipocket [add|remove] <character>')
        return

    remove_fighter = False

    # Figure out where the fighter name starts
    # to determine between 8!ipocket pit and 8!ipocket remove/add pit
    fighter_name_start_idx = 1

    if(tokens[1].lower() == "add"):
        fighter_name_start_idx = 2
    elif(tokens[1].lower() == "remove"):    
        fighter_name_start_idx = 2
        remove_fighter = True

    if not remove_fighter:
        # First add character, if necessary
        await i_play(client, message, db_acc, False)

    # Assume everything after is the fighter name
    test_fighter_string = ' '.join(tokens[fighter_name_start_idx:])
    fighter_name, confidence = await find_fighter(db_acc, channel, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        await channel.send('I\'m really not sure who {} is. Remember: 8!ipocket usage: 8!ipocket [add/remove] <character>'.format(test_fighter_string))
        return

    if(not await is_registered(db_acc, author.id, channel)):
        await channel.send('Please register with 8!register first!')
        return
    # Adding or removing that you pocket this character   
    else:
        try:
            db_acc.execute_update('''
                UPDATE
                    player_fighter
                SET
                    is_main      = IF(%(set_pocket)s = true, false, is_main),
                    is_pocket    = %(set_pocket)s,
                    is_true_main = IF(%(set_pocket)s = true, false, is_true_main)
                WHERE 
                    player_discord_id = %(discord_id)s AND
                    fighter_id = (SELECT id FROM fighter.fighter WHERE name=%(name)s)''',
                {
                    "discord_id": author.id,
                    "name": fighter_name,
                    "set_pocket": 0 if remove_fighter else 1
                }
            )
        except dberr.Error as e:
            print(e)
            await channel.send(DB_ERROR_MSG.format(author.mention))
            raise
        
        if remove_fighter: 
            await channel.send('{0} no longer pockets {1}. If you want ' \
                           'to remove this character entirely, use 8!iplay remove {1}'.format(author.mention, fighter_name))
        else:
            await channel.send('I see, so {} pockets {}. {}'.format(author.mention, fighter_name, random_snarky_comment()))

async def who_plays(client, message, db_acc):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens) < 2:
        await channel.send('8!whoplays usage: 8!whoplays <character>')
        return

    # Assume everything after is the fighter name
    test_fighter_string = ' '.join(tokens[1:])

    fighter_name, confidence = await find_fighter(db_acc, channel, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        await channel.send('I\'m really not sure who {} is. Remember: 8!whoplays usage: 8!whoplays <character>'.format(test_fighter_string))
        return
    
    try:
        rows = db_acc.execute('''
            SELECT
                pf.player_discord_id as discord_id
            FROM
                player.player_fighter pf
            INNER JOIN
                fighter.fighter f
                ON f.id = pf.fighter_id
            INNER JOIN
                player.guild_member gm
                ON gm.player_discord_id = pf.player_discord_id
            WHERE 
                f.name=%(fighter_name)s AND
                gm.guild_id = %(guild_id)s''',
            {
                "fighter_name": fighter_name,
                "guild_id": channel.guild.id
            }
        )

      #  msg = 'The following users play {}:\n\n'.format(fighter_name)
        msg = ''

        # Gross but cool list generators to concatenate user names
        users = [message.guild.get_member(int(row["discord_id"])) for row in rows]
        msg += ', '.join([user.display_name for user in users])

    except dberr.Error as e:
        print(e)
        await channel.send(DB_ERROR_MSG.format(author.mention))
        raise
    
    embed = discord.Embed(color=embed_color, description="No one." if msg == '' else msg)
    # Regex to remove ALL special characters from fighter name, then create url
    # Example: Pokemon Trainer becomes Pokmon Trainer due to special e
    embed.set_author(name = "{} Players".format(fighter_name), icon_url=fighter_icon_url(fighter_name))
    
    #embed.add_field(name='', value=tag, inline=True)
    await channel.send(embed=embed)

async def fighter_info(client, message, db_acc):
    channel = message.channel
    author = message.author

    tokens = message.content.split(' ')

    if len(tokens) < 2:
        await channel.send('8!fighter usage: 8!fighter <character>')
        return

    # Assume everything after is the fighter name
    test_fighter_string = ' '.join(tokens[1:])

    fighter_name, confidence = await find_fighter(db_acc, channel, test_fighter_string)

    # Might want to fine tune this later, but 80 seems good
    if(confidence < 80):
        await channel.send('I\'m really not sure who {} is. Remember: 8!fighter usage: 8!fighter <character>'.format(test_fighter_string))
        return

    fighter_alts = [
        {
            "name": fighter_name,
            "costume_number": num
        }
        for num in range(0,8)
    ]
    
    amalgam_url = create_stitched_image(fighter_alts)

    embed = discord.Embed(color=embed_color, description="{} details...".format(fighter_name))
    embed.set_image(url=amalgam_url)
    # Regex to remove ALL special characters from fighter name, then create url
    # Example: Pokemon Trainer becomes Pokmon Trainer due to special e
    embed.set_author(name = "{}".format(fighter_name), icon_url=fighter_icon_url(fighter_name, 0))

    #embed.add_field(name='', value=tag, inline=True)
    await channel.send(embed=embed)

async def olimar_is_cool(client, message, db_acc):
    channel = message.channel
    author = message.author
    await author.edit(nick="Dumb Idiot")
    await channel.send('You reap what you sow.')

async def looking_for_match(client, message, db_acc):
    channel = message.channel
    author = message.author
    role = discord.utils.get(author.guild.roles, name="looking to smash")
    if role == None:
        await author.guild.create_role(name="looking to smash", mentionable=True)
        role = discord.utils.get(author.guild.roles, name="looking to smash")

    await author.add_roles(role)
    await channel.send('{} wants to be pinged for matches.'.format(author.mention))

# TODO: combine this with above function
async def not_looking_for_match(client, message, db_acc):
    channel = message.channel
    author = message.author
    role = discord.utils.get(author.guild.roles, name="looking to smash")
    if role == None:
        await author.guild.create_role(name="looking to smash", mentionable=True)
        role = discord.utils.get(author.guild.roles, name="looking to smash")

    await author.remove_roles(role)
    await channel.send('{} does not want to be pinged for matches.'.format(author.mention))

async def ping_match_lookers(client, message, db_acc):
    channel = message.channel
    author = message.author
    role = discord.utils.get(author.guild.roles, name="looking to smash")
    if role == None:
        await author.guild.create_role(name="looking to smash", mentionable=True)
        role = discord.utils.get(author.guild.roles, name="looking to smash")

    await channel.send('{} is looking for a match! Who is {}?'.format(author.mention, role.mention))

async def coin_flip(client, message, db_acc):
    channel = message.channel
    author = message.author

    flip = random.randint(0, 1)
    embed = discord.Embed(color=embed_color)
    embed.set_author(name = "Heads" if flip == 1 else "Tails", icon_url=client.user.avatar_url)
    embed.set_image(url=base_url + 'c_thumb,w_75,g_face/' + ("yoshisumhead.gif" if flip == 1 else "yoshisumtail.gif"))
    await channel.send(embed=embed)
