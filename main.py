import pygame, random
from classes import Block

pygame.init()

screen_width = 640
screen_height = 480
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rhy's Shitty Platformer")

## Colour palette ##
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (200, 0, 255)

running = False
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

platformSpeed = 3

maxJumpHeight = 250 # Calculated from Block.jump() function and fixed accel. of 0.2

player = Block(purple, 60, 60, 0)
player.rect.x = 150
player.rect.y = 340

platform1 = Block(green, 160, 40, platformSpeed)
platform1.rect.x = 130
platform1.rect.y = 400
platform1.first = True

platform2 = Block(green, 160, 40, platformSpeed)
platform2.rect.x = 480
platform2.rect.y = random.randint(screen_height//3, screen_height)

sprites = pygame.sprite.Group()
sprites.add(player)
sprites.add(platform1)
sprites.add(platform2)

# platforms = pygame.sprite.Group()
# platforms.add(platform1)
# platforms.add(platform2)

platforms = [platform1, platform2]
debug = False
score = 0
started = False

# Game over screen
endScreen = pygame.Surface((screen_width, screen_height))
endScreen.fill(white)
endText = font.render('Game over!', 1, black)

# Welcome screen loop
welcome = True
while welcome:
    # welcome events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            welcome = False
        elif event.type==pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False
                welcome = False
            elif event.key == pygame.K_RETURN:
                welcome = False
                running = True
    
    # rendering
    screen.fill(white)
    introText1 = font.render('Welcome to my shitty platformer.', 1, black)
    introText2 = font.render('Press Space to jump.', 1, black)
    introText3 = font.render('Press Enter to begin.', 1, black)
    screen.blits(blit_sequence=((introText1, (130, 195)), (introText2, (198, 225)), (introText3, (195, 255))))
    pygame.display.flip()
    
    clock.tick(60)
    
# Main loop
while running:        
    ## MAIN GAME LOOP ##
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type==pygame.KEYDOWN:
            if event.key == pygame.K_x:
                running = False
            elif event.key == pygame.K_d:
                debug = not debug
    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if player.landed == True:
            player.jump()
            
    ## GAME LOGIC ##
    for platform in platforms:
        platform.moveLeft(platformSpeed)
        if platform.rect.x + platform.width <= 0:
            # Get the index of the current platform
            index = platforms.index(platform)
            # Get the other platform based on the index
            other_platform = platforms[(index + 1) % len(platforms)]
    
            # Determine the height range for respawning the current platform based on the other platform's position
            max_height = other_platform.rect.y - maxJumpHeight
    
            # Calculate the new height for the current platform within the allowed range
            new_height = random.randint(max(screen_height//3, max_height), screen_height - platform.height)
    
            # Move the current platform to the far right side of the screen and set its new height
            platform.rect.x = screen_width
            platform.rect.y = new_height
            platform.counted = False
            platform.first = False
    
    player.moveUp(player.speed)
    if player.landed == True:
        player.speed = 0
    else:
        player.speed -= 0.2            
    
    # Collision detection
    for platform in platforms:
        if player.rect.colliderect(platform.rect):
            player.landed = True
            player.rect.y = platform.rect.y - (player.height - 1)
            if not platform.counted:
                score += 1
                platform.counted = True
            
        if platform.rect.right < 150:
            player.landed = False
            
    screen.fill(white)
    sprites.draw(screen)
    
    ## SCORE DISPLAY ##
    scoreDisplay = font.render(f'Score: {score - 1}', 1, (0, 0 ,0))
    screen.blit(scoreDisplay, (500, 50))
            
    ## LOSE CONDITION ##
    if player.rect.y >= screen_height:
        screen.blits(blit_sequence=((endScreen, (0, 0)), (endText, (253, 211)), (scoreDisplay, (266, 245))))
        
    ## DEBUG INFO ##
    debug_landed = font.render(f'Landed: {player.landed}', 1, (0, 0, 0))
    debug_speed = font.render(f'Player speed: {player.speed}', 1, (0, 0, 0))
    
    if debug == True:    
        screen.blit(debug_landed, (10, 50))
        screen.blit(debug_speed, (10, 75))
    
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()