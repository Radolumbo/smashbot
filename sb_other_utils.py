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

from PIL import Image

from sb_db.utils import get_fighter_names
from sb_constants import base_icon_url

SECRET_CONFIG_FILE = './super_secret_config.json'

NSA_IS_WATCHING = {}

with open(SECRET_CONFIG_FILE) as json_file:  
    NSA_IS_WATCHING = json.load(json_file)

cloudinary.config( 
  cloud_name = NSA_IS_WATCHING["cloudinary_name"], 
  api_key = NSA_IS_WATCHING["cloudinary_key"], 
  api_secret = NSA_IS_WATCHING["cloudinary_secret"] 
)

async def find_fighter(db, test_fighter_string):
    fighter_names = await get_fighter_names(db)
    # Use fuzzy wuzzy to find most likely fighter match
    fighter_name, confidence = process.extractOne(test_fighter_string, fighter_names, scorer=fuzz.token_sort_ratio)
    return (fighter_name, confidence)

def fighter_icon_url(fighter_name):
    return base_icon_url + re.sub('[^A-Za-z]', '', fighter_name) + '0' + '.png'

def fighter_amalgam_url(amalgam_name):
    return base_icon_url + 'amalgams/' + amalgam_name + '.png'

def create_stitched_image(fighter_names):
    fighter_img_paths = ['./img/' + re.sub('[^A-Za-z]', '', fighter_name) + '0' + '.png' for fighter_name in fighter_names]
    images = [Image.open(im) for im in fighter_img_paths]

    img_merge = np.hstack([np.asarray( i.resize((20,20),Image.ANTIALIAS) ) for i in images ])
    new_img = Image.fromarray(img_merge)

    # randomly generate file name
    # to avoid conflicts of writing to same file 
    temp_file_name = './img/tmp/' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)) + '.png'
    new_img.save(temp_file_name)
    
    # create cloudinary file name for this combination of characters
    # so we can reuse/overwrite it without wasting space
    # sort fighter names so it's always in the same order
    amalgam_name = ''.join(sorted(re.sub('[^A-Za-z]', '', fighter_name) for fighter_name in fighter_names))

    cloudinary.uploader.upload(temp_file_name,
        folder="smash_icons/amalgams",
        overwrite=True,
        public_id=amalgam_name)

    delete_image(temp_file_name)

    return amalgam_name

def delete_image(file_path):
    os.remove(file_path)
    