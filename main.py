import pygame
# from PIL import Image
import random

clock = pygame.time.Clock()
pygame.init()

WIDTH = 1280
HEIGHT = 720        # Constants
CLOUD_WIDTH = 162
CLOUD_HEIGHT = 62

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # creates window
pygame.display.set_caption("2D Game")          # sets up screen size and captions it
background = pygame.image.load("images/CombinedBlue.png").convert()
background = pygame.transform.scale(background, (1280, 720))

objects = []

PInputR = 0
PInputL = 0
PInputU = 0    # initializes the booleans for player input
PInputD = 0
GameOver = False
HighScore = 0
Collision = False

XBound = (0, 1280)


class Object:
    def __init__(self, x, y, width, height, image, debug=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height     # Creates object class for us to use when making player sprite
        self.image = image
        self.velocity = [0, 0]
        self.initial_x = x
        self.initial_y = y

        objects.append(self)   # adds new objects to object list

        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.spritelist = ["Wcycle/SteamWalk1.png", "Wcycle/SteamWalk2.png", "Wcycle/SteamWalk3.png", "Wcycle/SteamWalk4.png", "Wcycle/SteamWalk5.png", "Wcycle/SteamWalk6.png"]
        self.frame_timer = 0
        
    def draw_thingy(self, picture):
        screen.blit(picture, (self.x, self.y))   # The draw function but for objects

    def update_thingy(self, picture, CloudSpeed):   # Update function for objects
        self.x += CloudSpeed
        self.draw_thingy(picture)


class Player(Object):
    def __init__(self, x, y, width, height, image, debug):
        super().__init__(x, y, width, height, image, debug)
        # Player class, made from Object class

    def gravity(self):
        # If player not touching cloud, gravity pulls character down
        # If player falls to bottom, stop their fall + KILL YOURSELF

        if check_collisions(Sam, Cloud1):  # if on cloud, don't move downwards
            self.velocity[1] = 0
            Collision = True
            # print("Potato")
        else:
            self.velocity[1] = 2   # Constant speed that the player falls down
            Collision = False

    def change_direction(self):
        if self.velocity[0] < 0:      # boolean for which direction character is facing
            self.flipX = True
        elif self.velocity[0] > 0:
            self.flipX = False

    def set_velocity(self, xr, xl, xu):
        self.velocity[0] = (xr - xl) * 3    # got rid of the y-axis movement to make space for jumping

    def update(self):
        self.set_velocity(PInputR, PInputL, PInputU)
        self.gravity()  # calls gravity before updating
        self.x += self.velocity[0]
        self.y += self.velocity[1]   # updates player position + redraws character
        self.x = max(XBound[0], min(self.x, XBound[1] - self.width))
        self.draw_player()
        

    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y

    def draw_player(self):
        image = pygame.image.load(self.spritelist[self.frame])      # loads image from animation sprite list
        # image = pygame.transform.scale(sprite, (self.width, self.height))

        self.change_direction()   # updates which direction player's facing
        
        image = pygame.transform.flip(image, self.flipX, False)    # flips the image if in left direction
        screen.blit(image, (self.x, self.y)) 

        if self.velocity[0] == 0:
            self.frame = 0    # If the player isn't moving set character to first sprite (resting image)
            return
        
        self.frame_timer += 1   

        if self.frame_timer < 10:   # basically the frame rate for the animation
            return
        self.frame += 1
        if self.frame >= len(self.spritelist):    # restarts the animation if the cycle is complete
            self.frame = 0

        self.frame_timer = 0


def check_collisions(obj1, obj2):
    x1, y1 = obj1.x, obj1.y     # gets the current center position of both objects
    x2, y2 = obj2.x, obj2.y
    w1, h1 = obj1.width, obj1.height
    w2, h2 = obj2.width, obj2.height
    if x1 + w1 >= x2 and x1 <= x2 + w2:    #If player in same x boundary as the clouds width
        if y1 + h1 <= y2 + 2 and y1 + h1 >= y2 - 2:   #If player bottom equal to top of cloud and player top is higher
            return True
        else:
            return False
    else:
        return False   # if not, then return False

# objects

Sam = Player(640, 100, 31, 41, "Wcycle/SteamWalk1.png", debug=True)
Cumulonimbus = pygame.transform.scale(pygame.image.load("images/cloud.png"), (CLOUD_WIDTH, CLOUD_HEIGHT))  #correctly sized cloud
Cloud1 = Object(1200, random.randint(10, 600), CLOUD_WIDTH, CLOUD_HEIGHT, Cumulonimbus, debug=True)
# Cloud2 = Object(1200, random.randint(10, 600), 485, 186, Cumulonimbus)   #Creates four clouds that will loop
# Cloud3 = Object(1200, random.randint(10, 600), 485, 186, Cumulonimbus)
# Cloud4 = Object(1200, random.randint(10, 600), 485, 186, Cumulonimbus)

objects.pop(0)

while GameOver == False:
    screen.blit(background, (0, 0))   # refreshes background before player movement

    # '''
    # This code below resets the position to the initial position.
    # This is used for debugging and testing.
    
    if Sam.y > HEIGHT:
        Sam.reset_position()
    # '''

    for event in pygame.event.get():
        # Key up or down
        if event.type == pygame.QUIT:  # closes window, if user exits game
            pygame.quit()
            SystemExit()
        elif event.type == pygame.KEYDOWN:   # If user presses down on key, acknowledges the input
            if event.key == pygame.K_RIGHT:
                PInputR = 1
            elif event.key == pygame.K_LEFT:
                PInputL = 1
            elif event.key == pygame.K_UP:
                PInputU = 1
            elif event.key == pygame.K_DOWN:
                PInputD = 1
        elif event.type == pygame.KEYUP:     # If user lets go of key, stops player movement in that direction
            if event.key == pygame.K_RIGHT:
                PInputR = 0
            elif event.key == pygame.K_LEFT:
                PInputL = 0
            elif event.key == pygame.K_UP:
                PInputU = 0
            elif event.key == pygame.K_DOWN:
                PInputD = 0

    Player.update(Sam)      # calls Player then updates them + draws

    Object.update_thingy(Cloud1, Cumulonimbus, random.randint(-3, -2))   # Spawns in the clouds and loops them
    if Cloud1.x < -10:
        Cloud1 = Object(1200, random.randint(10, 600), CLOUD_WIDTH, CLOUD_HEIGHT, Cumulonimbus, debug=True)  # when they get off screen
    # Object.update_thingy(Cloud2, Cumulonimbus, random.randint(-2, -1))
    # if Cloud2.x < -10:
        # Cloud2 = Object(1200, random.randint(10, 600), 485, 186, Cumulonimbus)
    # Object.update_thingy(Cloud3, Cumulonimbus, random.randint(-3, -1))
    # if Cloud3.x < -10:
        # Cloud3 = Object(1200, random.randint(10, 600), 485, 186, Cumulonimbus)
    # Object.update_thingy(Cloud4, Cumulonimbus, random.randint(-4, -2))
    # if Cloud4.x < -10:
        # Cloud4 = Object(1200, random.randint(10, 600), 485, 186, Cumulonimbus)

    clock.tick(70)    # caps it from refreshing more than 70 times a second
    pygame.display.update()    # updates changes in sprites

print("Game Over")
