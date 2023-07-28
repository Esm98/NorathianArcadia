# Game Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
FPS = 60

# Player Constants
PLAYER_SIZE = 50
PLAYER_HEALTH = 100
PLAYER_SPEED = 3
PLAYER_ATTACK = 10
PLAYER_DEFENSE = 10

# Sword Constants
SWORD_SIZE = 25
SWORD_LIFETIME = 10  # Number of frames the sword stays on screen

# Enemy Constants
ENEMY_SIZE = 50
ENEMY_SPEED = 3
ENEMY_SPAWN_RATE = 100  # The smaller this number, the more often enemies will spawn
PATROL_LIMIT = 50
# Drop Constants
DROP_SIZE = 15
LOOT = ['gold', 'xp', 'greaves', 'boots', 'breastplate', 'vambracers', 'gauntlets', 'helmet', 'weapon']

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255,255,0)
BLUE = (0,0,255)


PLAYER_SPRITESHEETS = {
    '': "defaultChar.png",
    'helmet': 'H.png',
    'chestPlate': 'C.png',
    'legs':'L.png',
    'arms':'A.png',
    'longSword':'S.png',
    ','.join(sorted(['helmet', 'chestPlate'])): 'HC.png',
    ','.join(sorted(['helmet', 'arms'])): 'HA.png',
    ','.join(sorted(['helmet', 'legs'])): 'HL.png',
    ','.join(sorted(['helmet', 'longSword'])): 'HS.png',
    ','.join(sorted(['chestPlate', 'arms'])): 'CA.png',
    ','.join(sorted(['chestPlate', 'legs'])): 'CL.png',
    ','.join(sorted(['chestPlate', 'longSword'])): 'CS.png',
    ','.join(sorted(['arms', 'legs'])): 'AL.png',
    ','.join(sorted(['arms', 'longSword'])): 'AS.png',
    ','.join(sorted(['legs', 'longSword'])): 'LS.png',
    ','.join(sorted(['helmet', 'chestPlate', 'arms'])): 'HCA.png',
    ','.join(sorted(['helmet', 'chestPlate', 'legs'])): 'HCL.png',
    ','.join(sorted(['helmet', 'chestPlate', 'longSword'])): 'HCS.png',
    ','.join(sorted(['helmet', 'arms', 'legs'])): 'HAL.png',
    ','.join(sorted(['helmet', 'arms', 'longSword'])): 'HAS.png',
    ','.join(sorted(['helmet', 'legs', 'longSword'])): 'HLS.png',
    ','.join(sorted(['chestPlate', 'arms', 'legs'])): 'CAL.png',
    ','.join(sorted(['chestPlate', 'arms', 'longSword'])): 'CAS.png',
    ','.join(sorted(['chestPlate', 'legs', 'longSword'])): 'CLS.png',
    ','.join(sorted(['arms', 'legs', 'longSword'])): 'ALS.png',
    ','.join(sorted(['helmet', 'chestPlate', 'arms', 'legs'])): 'HCAL.png',
    ','.join(sorted(['helmet', 'chestPlate', 'arms', 'longSword'])): 'HCAS.png',
    ','.join(sorted(['helmet', 'chestPlate', 'legs', 'longSword'])): 'HCLS.png',
    ','.join(sorted(['helmet', 'arms', 'legs', 'longSword'])): 'HALS.png',
    ','.join(sorted(['chestPlate', 'arms', 'legs', 'longSword'])): 'CALS.png',
    ','.join(sorted(['helmet', 'chestPlate', 'arms', 'legs', 'longSword'])): 'HCALS.png',

    # Add more combinations here as needed
}
