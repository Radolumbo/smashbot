import sys

embed_color = 0x562906
base_url = 'https://res.cloudinary.com/du9xmm6rh/image/upload/'
# "v1" assumes that the image was uploaded before Tuesday, May 17, 2033 11:33:20 PM GMT-04:00 DST
base_icon_url = base_url + 'v1/smash_icons/'


DB_ERROR_MSG = "Something went wrong with the database. Please try again, {}."

# return codes
RC_SUCCESS = 0
RC_CHANNEL_ONLY = 1
RC_COMMAND_DNE = 2
RC_OTHER = -1 

TEST_MODE = len(sys.argv) > 1 and (sys.argv[1] == "-t" or sys.argv[1] == "--test")

BASE_DIR = '.' if TEST_MODE else '/bin/smashbot'

SNARKY_IPLAY_RESPONSES = [
    "Because, of course you do.",
    "Am I supposed to be impressed?",
    "I'm actually a little impressed.",
    "Can you even hold a controller?",
    "Riding the bandwagon, I see.",
    "I mean, I guess that's a character in this game.",
    "Really, of everyone you could have picked?",
    "Wouldn't have been my choice.",
    "Cool!",
    "Wowie!",
    "Look out chat, we got a badass over here.",
    "Your mother would be so proud.",
    "Honestly, you might as well just pick random.",
    "It's what Sakurai would have wanted.",
    "Great, another one.",
    "Nice choice!",
    "No comment.",
    "You always did strike me as a good decision-maker.",
    "**NOTICE**: Your account has been flagged for lameness.",
    "Keep that up, and I'll have to ban you.",
    "I'd love to see it in action!"
]