#===============================================================================
#Modules being imported
#===============================================================================

import pygame 

#===============================================================================
#game state saving function 
#===============================================================================

def save_state(player, level_data):
    with open('game_state.txt', 'w') as file:
        file.write(f'Player Health: {player.health}\n')
        file.write(f'Player Ammo: {player.ammo}\n')
        file.write(f'Player Plasma Grenades: {player.plasma_grenades}\n')
        file.write(f'Level Data:\n')
        for row in level_data:
            file.write(','.join(map(str, row)) + '\n')
        print('Game state saved')