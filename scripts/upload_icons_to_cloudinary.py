import cloudinary.uploader
import json
import os
import sys
from sb_constants import TEST_MODE, BASE_DIR

from google.cloud import secretmanager

client = secretmanager.SecretManagerServiceClient()
path = client.secret_version_path("discord-smashbot", "super_secret_smashbot_dev_config" if TEST_MODE else "super_secret_smashbot_prod_config", "latest")
NSA_IS_WATCHING = ujson.loads(client.access_secret_version(path).payload.data.decode("utf-8"))


for f in os.listdir(BASE_DIR + "/../img"):
    cloudinary.uploader.upload(BASE_DIR + "/../img/" + f,
        folder="smash_icons",
        overwrite=True,
        public_id=os.path.splitext(f)[0],
        api_key=NSA_IS_WATCHING["cloudinary_key"],
        api_secret=NSA_IS_WATCHING["cloudinary_secret"],
        cloud_name=NSA_IS_WATCHING["cloudinary_name"])
