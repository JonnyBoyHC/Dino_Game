# Import necessary modules
import random
import pygame
from pygame.locals import *
import time
import sys

# Initialize Pygame
pygame.init()

class Ground():
  def __init__(self):
    self.ground_length = 1202
    self.image1 = pygame.image.load("sprites/ground.png")
    self.image1_x = 0
    self.image1_y = 200

    self.image2 = pygame.image.load("sprites/ground.png")
    self.image2_x = self.image1_x + self.ground_length
    self.image2_y = self.image1_y

    self.speed = 4

  def draw(self, screen):
    screen.blit(self.image1, (self.image1_x, self.image1_y))
    screen.blit(self.image2, (self.image2_x, self.image2_y))

  def update(self):
    self.image1_x -= self.speed
    self.image2_x -= self.speed

    if self.image1_x + self.ground_length < 0:
      self.image1_x = self.image2_x + self.ground_length
    if self.image2_x + self.ground_length < 0:
      self.image2_x = self.image1_x + self.ground_length

# Define the game function
def game():

  # Set the screen size and create a Pygame window
  screen = pygame.display.set_mode((700, 250))

  # Set up the Pygame clock for timing
  clock = pygame.time.Clock()

  # Set up the Pygame font for displaying text
  font = pygame.font.Font("freesansbold.ttf", 20)

  # Load game sounds (not used in this example)
  # check_point = pygame.mixer.Sound("checkPoint.wav")
  # death_sound = pygame.mixer.Sound("die.wav")

  # Load game images and set game icon and caption
  dino_icon = pygame.image.load("sprites/dino_.png")
  pygame.display.set_icon(dino_icon)
  pygame.display.set_caption("Dino Run")
  game_over = pygame.image.load("sprites/game_over.png")
  replay_button = pygame.image.load("sprites/replay_button.png")
  logo = pygame.image.load("sprites/logo.png")

  # Set a color for the screen background (not used in this example)
  grey = (240, 240, 240)

  ground = Ground()
  ground.draw(screen)
  ground.update()

  pygame.display.update()

  # Set up the game loop
  running = True
  while running:
    # Check for Pygame events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # If the user clicks the X button, exit the game
        running = False
        pygame.quit()
        sys.exit()

# Call the game function to start the game
game()
