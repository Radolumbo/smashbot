import cloudinary.uploader
import json
import os
import sys

TEST_MODE = len(sys.argv) > 1 and (sys.argv[1] == "-t" or sys.argv[1] == "--test")

SECRET_CONFIG_FILE = './super_secret_config.' + ('test' if TEST_MODE else 'prod') + '.json'

NSA_IS_WATCHING = {}

with open(SECRET_CONFIG_FILE) as json_file:  
    NSA_IS_WATCHING = json.load(json_file)



for f in os.listdir("../img"):
    cloudinary.uploader.upload("../img/" + f,
        folder="smash_icons",
        overwrite=True,
        public_id=os.path.splitext(f)[0],
        api_key=NSA_IS_WATCHING["cloudinary_key"],
        api_secret=NSA_IS_WATCHING["cloudinary_secret"],
        cloud_name=NSA_IS_WATCHING["cloudinary_name"])
