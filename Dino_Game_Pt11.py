# Import necessary modules
import random
import pygame
from pygame.locals import *
import time
import sys

# Initialize Pygame
pygame.init()

class Dino():

  def __init__(self):
    self.Img = pygame.image.load("sprites/dino_.png")
    self.WIDTH, self.HEIGHT = 44, 48
    self.Img = pygame.transform.scale(self.Img, (self.WIDTH, self.HEIGHT))

    self.image = self.Img

    self.x = 20
    self.y = 170

    # Gravity
    self.g = -0.25
    self.up = 7

    # Instance of time
    self.t = 0

    self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)

    self.runImg1 = pygame.image.load("sprites/dino_1.png")
    self.runImg2 = pygame.image.load("sprites/dino_2.png")
    self.runImg1 = pygame.transform.scale(self.runImg1, (self.WIDTH, self.HEIGHT))
    self.runImg2 = pygame.transform.scale(self.runImg2, (self.WIDTH, self.HEIGHT))

    self.duck1 = pygame.image.load("sprites/dino_ducking1.png")
    self.duck2 = pygame.image.load("sprites/dino_ducking2.png")
    self.duck1 = pygame.transform.scale(self.duck1, (self.WIDTH + 15, self.HEIGHT))
    self.duck2 = pygame.transform.scale(self.duck2, (self.WIDTH + 15, self.HEIGHT))

    self.is_ducking = False

    self.runImgs = [self.runImg1, self.runImg2]
    self.duckImgs = [self.duck1, self.duck2]

    self.jump_sound = pygame.mixer.Sound("./sounds/jump.wav")
    self.count = 0
    self.jumping = False

  def jump(self):
    self.y -= self.up
    self.jumping = True
    self.jump_sound.play()

  def update(self):
    # Check if dino is jumping
    if self.y < 170:
      # Newton First Law of Motion: Vf = Vi + at
      self.up = self.up + self.g * self.t
      self.y -= self.up
      self.t += 0.12

    # Check if the jump is complete and resetting all variables
    if self.y > 170:
      self.y = 170
      self.t = 0
      self.up = 7
      self.jumping = False

    if self.is_ducking:
      self.hitbox = pygame.Rect(self.x + 5, self.y + 20, self.WIDTH + 12, self.HEIGHT - 20)
      self.image = self.duckImgs[self.count % 2]
      self.count += 0.2
    elif self.jumping:
      self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 15, self.HEIGHT - 5)
      self.image = self.Img
    else:
      self.hitbox = pygame.Rect(self.x + 5, self.y, self.WIDTH - 17, self.HEIGHT - 5)
      self.image = self.runImgs[int(self.count) % 2] # type: ignore
      self.count += 0.15

  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))
    # # Drawing a RED rectangle around Dino
    # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

class Ptera():

  def __init__(self):
    self.width, self.height = 50, 40
    self.im1 = pygame.image.load("sprites/ptera1.png")
    self.im2 = pygame.image.load("sprites/ptera2.png")

    self.im1 = pygame.transform.scale(self.im1, (self.width, self.height))
    self.im2 = pygame.transform.scale(self.im2, (self.width, self.height))

    self.flaps = [self.im1, self.im2]

    self.altitudes = [175, 150, 110]
    self.x = random.randint(750, 1000)
    self.y = random.choice(self.altitudes)

    self.speed = 5
    self.count = 0
    self.is_ptera = True
    self.is_cactus = False

    self.hitbox = (self.x, self.y + 10, self.width, self.height - 12)

  def update(self):
    self.image = self.flaps[int(self.count) % 2 ]
    self.count += 0.1

    self.x -= self.speed

    if self.x < 50:
      self.allowed = True

    self.hitbox = pygame.Rect(self.x, self.y + 10, self.width, self.height - 10)

  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))
    # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


class Cactus():

  def __init__(self):
    self.image0 = pygame.image.load("sprites/cacti-small.png")
    self.image1 = pygame.image.load("sprites/cacti-big.png")
    self.width0 = 45
    self.width1 = 65
    self.height = 45

    self.image0 = pygame.transform.scale(self.image0, (self.width0, self.height))
    self.image1 = pygame.transform.scale(self.image1, (self.width1, self.height))

    self.is_cactus = True
    self.is_ptera = False

    self.image, self.width = random.choice([[self.image0, self.width0], [self.image1, self.width1]])

    self.x = random.randint(720, 1000)
    self.y = 175
    self.speed = 4

    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

  def update(self):
    self.x -= self.speed
    self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))


class Ground():

  # Configuring the attributes of the ground object
  def __init__(self):
    self.ground_length = 1202
    self.image1 = pygame.image.load("sprites/ground.png")
    self.image1_x = 0
    self.image1_y = 200

    self.image2 = pygame.image.load("sprites/ground.png")
    self.image2_x = self.image1_x + self.ground_length
    self.image2_y = self.image1_y

    self.speed = 4

  # Draw the ground object on screen
  def draw(self, screen):
    screen.blit(self.image1, (self.image1_x, self.image1_y))
    screen.blit(self.image2, (self.image2_x, self.image2_y))

  # Update the image of the ground object
  def update(self):
    self.image1_x -= self.speed
    self.image2_x -= self.speed

    if self.image1_x + self.ground_length < 0:
      self.image1_x = self.image2_x + self.ground_length
    if self.image2_x + self.ground_length < 0:
      self.image2_x = self.image1_x + self.ground_length


class Cloud():

  # Configuring the attributes of the cloud object
  def __init__(self):
    self.image = pygame.image.load("sprites/cloud.png")
    self.WIDTH, self.HEIGHT = 70, 40
    self.image = pygame.transform.scale(self.image, (self.WIDTH, self.HEIGHT))

    self.speed = 1
    self.x = 600
    self.y = 50

  # Update the cloud object on screen
  def update(self):
    self.x -= self.speed

    if self.x < -self.WIDTH:
      self.x = 600
      self.y = random.randint(10, 100)

  # Draw the cloud object on screen
  def draw(self, screen):
    screen.blit(self.image, (self.x, self.y))


# Define the game function
def game():

  # Set the screen size and create a Pygame window
  screen = pygame.display.set_mode((700, 250))

  # Set up the Pygame clock for timing
  clock = pygame.time.Clock()

  # Set up the Pygame font for displaying text
  font = pygame.font.Font("freesansbold.ttf", 20)

  # Load game sounds (not used in this example)
  check_point = pygame.mixer.Sound("./sounds/checkPoint.wav")
  death_sound = pygame.mixer.Sound("./sounds/die.mp3")

  # Load game images and set game icon and caption
  dino_icon = pygame.image.load("sprites/dino_.png")
  pygame.display.set_icon(dino_icon)
  pygame.display.set_caption("Dino Run")
  game_over = pygame.image.load("sprites/game_over.png")
  replay_button = pygame.image.load("sprites/replay_button.png")
  logo = pygame.image.load("sprites/logo.png")

  # Set a color for the screen background (not used in this example)
  grey = (240, 240, 240)

  # Create ground using ground class
  ground = Ground()
  ground.draw(screen)
  ground.update()

  # Create clouds using cloud class
  cloud = Cloud()
  cloud.draw(screen)
  cloud.update()

  # Creating obstacles using obstacles class
  obstacles = [Cactus()]
  obstacle_start = time.time()
  minimum_time = 1.5

  running = False
  # play_game = True
  dead = False
  high_score_value = 0
  FPS = 85

  # Creating a dino
  dino = Dino()

  # Update the display screen of whole game
  pygame.display.update()

  # Set up the game loop
  while True:
    if not dead:
      screen.fill(grey)
      ground.draw(screen)
      screen.blit(dino.image, (dino.x, dino.y))
      screen.blit(logo, (200, 70))

    pygame.display.update()

    # Check for Pygame events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # If the user clicks the X button, exit the game
        # running = False
        pygame.quit()
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          running = True
          ground = Ground()
          dino = Dino()
          obstacles = [Cactus()]
          obstacle_start = time.time()
          dead = False
          score_value = 0

    while running:
      clock.tick(FPS)
      score = font.render("Score: " + str(score_value), True, (200, 200, 200))
      score_value += 0.25
      high_score_value = max(high_score_value, score_value)
      high_score = font.render("High Score: " + str(high_score_value), True, (200, 200, 200))
      screen.fill(grey)

      # Event Handling
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          # If the user clicks the X button, exit the game
          # running = False
          pygame.quit()
          sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            dino.jump()
          elif event.type == pygame.K_DOWN:
            dino.is_ducking = True
        elif event.type == pygame.KEYUP:
          if event.key == pygame.K_DOWN:
            dino.is_ducking = False

      ground.update()
      ground.draw(screen)

      cloud.update()
      cloud.draw(screen)

      dino.update()
      dino.draw(screen)

      for obstacle in obstacles:
        if obstacle.is_cactus:
          obstacle.speed = ground.speed
        elif obstacle.is_ptera:
          obstacle.speed = ground.speed + 1

        obstacle.update()
        obstacle.draw(screen)

      screen.blit(score, (550, 30))
      screen.blit(high_score, (350, 30))

      if time.time() - obstacle_start > minimum_time + random.randrange(0, 30) / 10:
        obstacle_start = time.time()

        if score_value > 100:
          ptera_probability = random.random()
          if ptera_probability > 0.5:
            obstacles.append(Ptera())
            obstacles[-1].speed = ground.speed + 1
          else:
            obstacles.append(Cactus())
            obstacles[-1].speed = ground.speed
        else:
            obstacles.append(Cactus())
            obstacles[-1].speed = ground.speed

      if score_value > 0 and score_value % 100 == 0 and score_value % 3 == 0:
        ground.speed += 0.25
        for obstacle in obstacles:
          if obstacle.is_cactus:
            obstacle.speed = ground.speed
          elif obstacle.is_ptera:
            obstacle.speed = ground.speed + 1

      if score_value > 1 and score_value % 100 == 0:
        check_point.play()

      if dino.hitbox.colliderect(obstacles[0].hitbox):
        death_sound.play()
        dead = True
        screen.blit(game_over, (170, 70))
        screen.blit(replay_button, (340, 100))

      if obstacles[0].x < -30:
        obstacles.pop(0)
        if obstacles == []:
          obstacles.append(Cactus())
          obstacle_start = time.time()

      pygame.display.update()

      if dead:
        del dino
        del ground
        del obstacles
        running = False

# Call the game function to start the game
game()
