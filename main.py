import pygame
pygame.init()
from PIL import Image
vec = pygame.math.Vector2     #sets up vectors for later physics (Gravity and friction stuff)
clock = pygame.time.Clock()


screen = pygame.display.set_mode((1280,720))   #creates window
pygame.display.set_caption("2D Game")          #sets up screen size and captions it
background = pygame.image.load("CombinedBlue.png").convert()
background = pygame.transform.scale(background, (1280, 720))

objects = []

PInputR = 0
PInputL = 0
PInputU = 0    #initializes the booleans for player input
PInputD = 0
GameOver = False
HighSchore = 0

class Object:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height     #Creates object class for us to use when making player sprite
        self.image = image
        self.velocity = [0, 0]

        objects.append(self)   #adds new objects to object list

        self.direction = 0
        self.flipX = False
        self.frame = 0
        self.spritelist = ["SteamWalk1.png", "SteamWalk2.png", "SteamWalk3.png", "SteamWalk4.png", "SteamWalk5.png", "SteamWalk6.png"]
        self.frame_timer = 0

    def change_direction(self):
        if self.velocity[0] < 0:      #boolean for which direction character is facing
            self.flipX = True
        elif self.velocity[0] > 0:
            self.flipX = False
    
    def set_velocity(self, xr, xl, yu, yd):
        self.velocity[0] = (xr - xl) * 3
        self.velocity[1] = (yd - yu) * 3
    
    def draw_self(self):
        sprite = pygame.image.load(self.spritelist[self.frame])      #loads image from animation sprite list
        image = pygame.transform.scale(sprite, (self.width, self.height))

        self.change_direction()   #updates which direction player's facing
        
        image = pygame.transform.flip(image, self.flipX, False)    #flips the image if in left direction
        screen.blit(image, (self.x, self.y)) 

        if self.velocity[0] == 0:
            self.frame = 0    #If the player isn't moving set character to first sprit (resting image)
            return
        
        self.frame_timer += 1   

        if self.frame_timer < 10:   #basically the frame rate for the animation 
            return
        self.frame += 1
        if self.frame >= len(self.spritelist):    #restarts the animation if the cycle is complete
            self.frame = 0

        self.frame_timer = 0

    def gravity(self):
        #If player not touching cloud, gravity pulls character down

        #If player falls to bottom, stop their fall + KILL YOURSELF
        if self.y < 700:
            self.velocity[1] += 3
        else:
            GameOver = True


    def update(self):
        self.set_velocity(PInputR, PInputL, PInputU, PInputD)
        self.gravity()  #calls gravity before updating
        self.x += self.velocity[0]
        self.y += self.velocity[1]   #updates player position + redraws character
        self.draw_self()


class Player(Object):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)   #Player class, made from Object class (being buggy rn)


#objects

Sam = Player(640, 100, 31, 41, "SteamMan.png")


#test_entity = Entity(600, 600, 50, 50, "SteamMan_walk.png", 5)


while GameOver == False:
    screen.blit(background, (0, 0))   #refreshes background before player movement

    for event in pygame.event.get():
        # Key up or down
        if event.type == pygame.QUIT:  #closes window, if user exits game
            pygame.quit()
            SystemExit()
        elif event.type == pygame.KEYDOWN:   #If user presses down on key, acknowledges the input
            if event.key == pygame.K_RIGHT:
                PInputR = 1
            elif event.key == pygame.K_LEFT:
                PInputL = 1
            elif event.key == pygame.K_UP:
                PInputU = 1
            elif event.key == pygame.K_DOWN:
                PInputD = 1
        elif event.type == pygame.KEYUP:     #If user lets go of key, stops player movement in that direction
            if event.key == pygame.K_RIGHT:
                PInputR = 0
            elif event.key == pygame.K_LEFT:
                PInputL = 0
            elif event.key == pygame.K_UP:
                PInputU = 0
            elif event.key == pygame.K_DOWN:
                PInputD = 0

    Player.update(Sam)      #calls Player then updates them + draws


    clock.tick(60)    #caps it from refreshing more than 60 times a second
    pygame.display.update()    #updates changes in sprites

print("Game Over")