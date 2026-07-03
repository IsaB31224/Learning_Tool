from db.database import get_character_name 
from shared.hashmap import hash_formula #linking files 

def input_index_calc (character_name): #converting character name to index value

    index=hash_formula(character_name)

    return index


