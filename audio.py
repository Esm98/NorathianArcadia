import pygame

# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Set the path to the .wav file
audio_file_path = 'E:/gameMusic/NGGYU.wav'

# Load the .wav file
audio = pygame.mixer.Sound(audio_file_path)

# Play the audio
audio.play()

# Wait for the audio to finish playing
while pygame.mixer.get_busy():
    continue
