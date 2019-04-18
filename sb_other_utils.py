from fuzzywuzzy import fuzz, process

from sb_db_utils import get_fighter_names

def find_fighter(db, test_fighter_string):
    fighter_names = get_fighter_names(db)
    # Use fuzzy wuzzy to find most likely fighter match
    fighter_name, confidence = process.extractOne(test_fighter_string, fighter_names, scorer=fuzz.token_sort_ratio)
    return (fighter_name, confidence)