import pygame       
''' can't name my file as pygame.. because than it wont work
Pygame is a 2D graphics library that lets you make lil games '''

#PYGAME just keeps drawing stuff on the screen, if we manually dont remove it

import os
pygame.font.init()
pygame.mixer.init()

WIDTH , HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) #telling pygame to make new window of specified width and height
'''
(WIDTH, HEIGHT) is a tuple
'''
#It's good conventions to define all constant values in CAPS

pygame.display.set_caption('First Game!') 
#this will change the game name from its default *pygame* to our choice of name

#In RGB, (255,255,255) represents White color
WHITE = (255,255,255) #Is a tuple
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW =(255,255,0)

SCORE_FONT = pygame.font.SysFont('franklingothicmedium', 15)
WINNER_FONT = pygame.font.SysFont('franklingothicmedium', 70)

BORDER = pygame.Rect(WIDTH//2 -2, 0, 4, HEIGHT)
#                   (   x   , y, w,     h  )  for x we do width/2 -5 instead of 450 directly cuz we want the border to be in middle ie 5 on left of 450 and 5 on right of 450

BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets/Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets/Grenade+1.mp3'))

VELOCITY = 5 #speed at which the players would move
BULLET_VEL = 10 #speed at which bullets will travel
MAX_BULLETS = 3 #Numer of max bullets each player has!

FPS = 60 #frames per second, we use it so our game runs at same speed on all devices : defines at what speed our game can be updated at!
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40



#Now we are going to create events
YELL_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT + 2
'''
The [+ number] part above represents different events
different number means different events
and same number means same event

[pygame.USEREVENT] is some number or some ID

The complete statement assigns a unique ID to the events
'''

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")), (WIDTH,HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_yellow.png")) #these are surfaces
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_red.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) #scaling down the spaceships sizes to be appropriate for our game
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)



def draw_window(red, yellow, red_bullets, yellow_bullets, red_score, yellow_score):
    #WINDOW.fill(BLACK)  :used to fill the screen with specific color
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, WHITE, BORDER) #(where to draw, color of the fig, what to draw)


    red_score_txt = SCORE_FONT.render("Score: " + str(red_score), 1, WHITE)
    yellow_score_txt = SCORE_FONT.render("Score: " + str(yellow_score), 1, WHITE)

    WINDOW.blit(red_score_txt, (WIDTH - red_score_txt.get_width() - 10, 8))
    # we do -10 , 10 so that its 10 from right and left wall respectively at the top right side

    WINDOW.blit(yellow_score_txt, (10, 8))
    # we do 10 , 10 so that its 10 from right and left wall respectively at the top left side


    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x , yellow.y)) #blit is used to draw surfaces on the screen, providing an initial location 
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullets in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullets)

    for bullets in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullets)

    pygame.display.update() #in pygame we need to *manually update* for the recent things we drew to be displayed on the screen   



def yellow_moves(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #to move LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width - 17 < BORDER.x: #to move RIGHT
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #to move UPWARD
        yellow.y -= VELOCITY 
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15: #to move DOWNWARD
        yellow.y += VELOCITY   



def red_moves(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #to move LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width - 17 < WIDTH: #to move RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: #to move UPWARD
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15: #to move DOWNWARD
        red.y += VELOCITY



def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL #to move it to right
        if red.colliderect(bullet): 
            '''it checks if the rectangle representing our red ship has collided with rectangle representing our yellow's bullet
                [only works for rectangular areas]'''
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #to move it to left
        if yellow.colliderect(bullet): 
            pygame.event.post(pygame.event.Event(YELL_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_txt = WINNER_FONT.render(text, 1, BLACK)
    WINDOW.blit(draw_txt,(WIDTH/2 - draw_txt.get_width() /2, HEIGHT/2 - draw_txt.get_height()/2))
    d_txt = WINNER_FONT.render(text, 1, RED)
    WINDOW.blit(d_txt,(WIDTH/2 - draw_txt.get_width() /2 +1, HEIGHT/2 - draw_txt.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(650, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) #defines initial position of shapeships
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = [] #is a list
    yellow_bullets = []

    #These represent scores when the game started, whoever gets hit, points will be deducted and atlast the player with zero points losses
    red_score = 10
    yellow_score = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #This will control the speed of while loop to 60 times per second
        #makes the game consistent on different computers
        for event in pygame.event.get(): #what we are doing here is passing different events in this queue
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: #KEYDOWN is an event in python
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    #for left player we need our bullets to go towards right
                    bullet = pygame.Rect(yellow.x + yellow.width - 17, yellow.y + yellow.height//2 - 2, 7, 5)
                    #here we do two slashes to divide so we get an integer output, had we done one slash it would give float value which is not acceptable when creating new rectangle in pygame 
                    ''' while defining position of the bullet, we take                                 |  |
                        x coodinate as [yellow.x + yellow.width]                                    width height (of bullet)
                                           |            |
                  (top left x coordinate of ship)  (to which we add the size of the ship so it shoots bullets from it right end)

                        and y coordinate as [yellow.y + yellow.height/2] as this would give
                                                |              |
                      (Top left y coordinate of ship)    (adding this would make bullets shoot from the middle of the ship)
                    '''
                    yellow_bullets.append(bullet) #adds objects to the end of the list
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 7, 5)
                    #here we dont add the width of the ship to the x coordinate as the ship is facing towards left!!
                    red_bullets.append(bullet)
                    #for right player we need our bullets to go towards left
                    BULLET_FIRE_SOUND.play()
        
            if event.type == RED_HIT:
                red_score -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELL_HIT:
                yellow_score -= 1
                BULLET_HIT_SOUND.play()

        winner_declaration = ""
        if red_score <= 0:
            winner_declaration = "Yellow WON!"

        if yellow_score <= 0:
            winner_declaration = "Red WON!"

        if winner_declaration != "":
            draw_winner(winner_declaration)
            break


        keys_pressed = pygame.key.get_pressed()
        yellow_moves(keys_pressed, yellow)
        red_moves(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red) 
        '''This function handles bullets taking in the input 
                > yellow ship's bullets
                > red ship's bullets
                > yellow ship
                > red ship

            what it does is 
            > handle bullet collides
            > handle how bullets move around the screen
            > remove bullets when they get off the screen or collide with the character
        '''
        draw_window(red, yellow, red_bullets, yellow_bullets, red_score, yellow_score)

    main()
    ''' pygame.quit() #when the user clicks cross, the game quits
    #quit is also an event in python    '''

if __name__ == "__main__": 
    main()     

''' this will make sure to only run the game when we run this file directly
    and not if this file is imported from somewhere else'''