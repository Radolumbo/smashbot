import cloudinary.uploader
import json
import os
import sys
from sb_constants import SECRET_CONFIG_FILE, TEST_MODE

NSA_IS_WATCHING = {}

with open(SECRET_CONFIG_FILE) as json_file:  
    NSA_IS_WATCHING = json.load(json_file)



for f in os.listdir(BASE_DIR + "/../img"):
    cloudinary.uploader.upload(BASE_DIR + "/../img/" + f,
        folder="smash_icons",
        overwrite=True,
        public_id=os.path.splitext(f)[0],
        api_key=NSA_IS_WATCHING["cloudinary_key"],
        api_secret=NSA_IS_WATCHING["cloudinary_secret"],
        cloud_name=NSA_IS_WATCHING["cloudinary_name"])
