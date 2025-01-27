
def compare_pokemon(pokemon_target, pokemon_guess):
    shared_attributes = {}
    for key in ["type1", "type2", "generation", "is_legendary"]:
        if pokemon_target.get(key) == pokemon_guess.get(key):
            shared_attributes[key] = pokemon_target[key]
    return shared_attributes