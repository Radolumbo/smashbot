from fuzzywuzzy import fuzz, process
import re
import sys
import random
import os
import string
import numpy as np
import json
import cloudinary
import cloudinary.uploader
import json

from PIL import Image, ImageDraw, ImageFont

from sb_db.utils import get_fighter_names
import sb_db.errors as dberr
from sb_constants import base_icon_url, DB_ERROR_MSG, TEST_MODE, BASE_DIR, SNARKY_IPLAY_RESPONSES

from google.cloud import secretmanager
import discord

client = secretmanager.SecretManagerServiceClient()
path = client.secret_version_path("discord-smashbot", "super_secret_smashbot_dev_config" if TEST_MODE else "super_secret_smashbot_prod_config", "latest")
response = client.access_secret_version(request={"name": path})
NSA_IS_WATCHING = json.loads(response.payload.data.decode("utf-8"))


cloudinary.config(
  cloud_name = NSA_IS_WATCHING["cloudinary_name"],
  api_key = NSA_IS_WATCHING["cloudinary_key"],
  api_secret = NSA_IS_WATCHING["cloudinary_secret"]
)

def get_bot_user(client: discord.Client):
    assert client.user is not None
    return client.user

async def find_users_in_guild_by_switch_tag(db_acc, message, test_user_string, confidence_threshold):
    try:
        rows = db_acc.execute('''
            SELECT
                switch_tag,
                discord_id
            FROM
                player.player p
            INNER JOIN
                player.guild_member g
                ON p.discord_id = g.player_discord_id
            WHERE
                g.guild_id=%(guild_id)s''',
            {
                "guild_id": message.guild.id
            }
        )
    except dberr.Error as e:
        print(e)
        await message.channel.send(DB_ERROR_MSG.format(message.author.mention))
        raise

    member_dict = {}
    for row in rows:
        member_dict[row["switch_tag"]] = row["discord_id"]

    confidence_list = process.extract(test_user_string, member_dict.keys(), scorer=fuzz.token_sort_ratio)
    return_list = []

    found_exact = False
    for item in confidence_list:
        tag, confidence = item[0], item[1]
        if tag == test_user_string:
            found_exact = True
            return_list.append(member_dict[tag])
        elif not found_exact and confidence > confidence_threshold:
            return_list.append(member_dict[tag])

    return return_list

async def find_users_in_guild_by_name(db_acc, message, test_user_string, confidence_threshold):
    member_dict = {}
    for m in message.guild.members:
        member_dict[m.display_name] = m.id

    confidence_list = process.extract(test_user_string, member_dict.keys(), scorer=fuzz.token_sort_ratio)
    return_list = []

    found_exact = False
    for item in confidence_list:
        name, confidence = item[0], item[1]
        if name == test_user_string:
            found_exact = True
            return_list.append(member_dict[name])
        elif not found_exact and confidence > confidence_threshold:
            return_list.append(member_dict[name])

    return return_list

async def find_fighter(db_acc, channel, test_fighter_string):
    alias_to_name = await get_fighter_names(db_acc, channel)
    # Use fuzzy wuzzy to find most likely fighter match
    result = process.extractOne(test_fighter_string, alias_to_name.keys(), scorer=fuzz.token_sort_ratio)
    if result is None:
        return (None, 0)
    fighter_alias, confidence = result[0], result[1]
    return (alias_to_name[fighter_alias], confidence)

def fighter_icon_url(fighter_name, idx=0):
    return base_icon_url + re.sub('[^A-Za-z]', '', fighter_name) + str(idx) + '.png'

def fighter_amalgam_url(amalgam_name):
    return base_icon_url + 'amalgams/' + amalgam_name + '.png'

def create_stitched_image(fighters):
    fighter_img_paths = [BASE_DIR + '/img/' + re.sub('[^A-Za-z]', '', fighter["name"]) + str(fighter["costume_number"]) + '.png' for fighter in fighters]
    images = [Image.open(im) for im in fighter_img_paths]

    font18 = ImageFont.truetype(BASE_DIR + '/font/Roboto-Bold.ttf', size=18)
    font22 = ImageFont.truetype(BASE_DIR + '/font/Roboto-Bold.ttf', size=22)

    for i in range(0, len(fighters)):
        image = images[i]
        fighter = fighters[i]
        draw = ImageDraw.Draw(image)
        message = ''
        color = 'rgb(0, 0, 0)' # black color

        # Draw in black for an outline first,
        # then draw in color
        if fighter.get("is_true_main", False):
            message = "M"
            draw.text((0, 0), message, fill=color, font=font22)
            color = 'rgb(0, 255, 255)'
            draw.text((2, 2), message, fill=color, font=font18)
        elif fighter.get("is_main", False):
            message = "M"
            draw.text((0, 0), message, fill=color, font=font22)
            color = 'rgb(0, 255, 0)'
            draw.text((2, 2), message, fill=color, font=font18)
        elif fighter.get("is_pocket", False):
            message = "P"
            draw.text((0, 0), message, fill=color, font=font22)
            color = 'rgb(255, 0, 0)'
            draw.text((2, 2), message, fill=color, font=font18)


    img_merge = np.hstack([np.asarray( i.resize((30,30),Image.Resampling.LANCZOS) ) for i in images ])
    new_img = Image.fromarray(img_merge)

    # randomly generate file name
    # to avoid conflicts of writing to same file
    temp_file_name = BASE_DIR + '/img/tmp/' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)) + '.png'
    new_img.save(temp_file_name)

    # create cloudinary file name for this combination of characters
    # so we can reuse/overwrite it without wasting space
    amalgam_name = ''
    for fighter in fighters:
        amalgam_name += re.sub('[^A-Za-z]', '', fighter["name"]) + str(fighter["costume_number"])
        if fighter.get("is_true_main", False):
            amalgam_name += "TRUE"
        elif fighter.get("is_main", False):
            amalgam_name += "MAIN"
        elif fighter.get("is_pocket", False):
            amalgam_name += "POCK"

    res = cloudinary.uploader.upload(temp_file_name,
        folder="smash_icons/amalgams",
        overwrite=True,
        public_id=amalgam_name)

    delete_image(temp_file_name)

    return res["url"]

def delete_image(file_path):
    os.remove(file_path)

def random_snarky_comment():
    num = random.randint(0, len(SNARKY_IPLAY_RESPONSES) - 1)
    return SNARKY_IPLAY_RESPONSES[num]
