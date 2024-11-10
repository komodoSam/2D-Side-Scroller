import pygame
pygame.init()
vec = pygame.math.Vector2     #sets up vectors for later physics (Gravity and friction stuff)
clock = pygame.time.Clock()

accel = 0.5
friction = -0.1

screen = pygame.display.set_mode((1280,720))   #creates window
pygame.display.set_caption("2D Game")          #sets up screen size and captions it


PInputR = 0
PInputL = 0
PInputU = 0    #initializes the booleans for player input
PInputD = 0
P_PositionX = 640    #starts player in middle of the screen (for now)
P_PositionY = 360
PlayerVelocity = [0, 0]   #velocity vector, using a list

Dumbass = pygame.image.load('SteamMan.png').convert()    #imports sprite for character
screen.blit(Dumbass,(P_PositionX,P_PositionY))

def check_keys(key, value):
    R = L = U = D = 0
    if key == pygame.K_RIGHT:
        R = value
    elif key == pygame.K_LEFT:
        L = value
    elif key == pygame.K_UP:
        U = value
    elif key == pygame.K_DOWN:
        D = value
    return R, L, U, D

while True:

    screen.fill((0, 0, 240))   #refreshes background before player movement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  #closes window, if user exits game
            pygame.quit()
            SystemExit()
        elif event.type == pygame.KEYDOWN:
            PInputR, PInputL, PInputU, PInputD = check_keys(event.key, 1)
        elif event.type == pygame.KEYUP:
            PInputR, PInputL, PInputU, PInputD = check_keys(event.key, 0)
    

    P_PositionX += (PInputR - PInputL) * 5
    P_PositionY += (PInputD - PInputU) * 5


    pygame.draw.rect(screen, (0, 0, 0), (P_PositionX, P_PositionY, 100, 50)) #starts the character in middle of screen

    clock.tick(60)    #caps it from refreshing more than 60 times a second
    pygame.display.update()    #updates changes in sprites
