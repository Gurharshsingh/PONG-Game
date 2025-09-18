import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1200,800))

pygame.display.set_caption("Pong trial")

#colors
white = (255,255,255)
d_grey = (26,26,26)
magenta = (255,0,255)
yellow = (255,255,0)
red = (255,0,0)
green = (0,255,0)
l_grey = (77,77,77)
cyan = (0,255,255)


clock = pygame.time.Clock()
fps = 60

game_font = pygame.font.SysFont("Luckiest Guy Regular",40)

player_score = 0
opponent_score = 0

#Game objects

paddle_width = 15
paddle_height = 100

player_x = 50
player_y = (screen.get_height()/2) -(paddle_height/2)
opponent_x = screen.get_width() - 50 - paddle_width
opponent_y = (screen.get_height() / 2) - (paddle_height / 2)

ball_size =20

ball_x = (screen.get_width() / 2) - (ball_size / 2)
ball_y = (screen.get_height() / 2) - (ball_size / 2)

#object creation

player_paddle = pygame.Rect(player_x, player_y, paddle_width, paddle_height)
opponent_paddle = pygame.Rect(opponent_x, opponent_y, paddle_width, paddle_height)
ball = pygame.Rect(ball_x, ball_y, ball_size, ball_size)
#paddle speed
player_speed = 0
p_speed=0
opponent_speed = 0

#ball speed
ball_speed_x = 7
ball_speed_y = 7
#start button

button_width = 200
button_height = 50
button_x = (screen.get_width()/ 2  - button_width /2)
button_y = (screen.get_height()*0.75 - button_height/2)

start_button = pygame.Rect(button_x, button_y, button_width, button_height)

difficulty_button_width = 200
difficulty_button_height = 50
medium_button_x = (screen.get_width()/2 - difficulty_button_width/2)
medium_button_y = (screen.get_height()*0.5 - difficulty_button_height/2)
 
hard_button_x = (screen.get_width()/2 - difficulty_button_width/2 + 220)
hard_button_y = (screen.get_height()*0.5 - difficulty_button_height/2)

easy_button_x = (screen.get_width()/2 - difficulty_button_width/2 - 220)
easy_button_y = (screen.get_height()*0.5 - difficulty_button_height/2)

medium_button = pygame.Rect(medium_button_x, medium_button_y, difficulty_button_width, difficulty_button_height)
hard_button = pygame.Rect(hard_button_x, hard_button_y, difficulty_button_width, difficulty_button_height)
easy_button = pygame.Rect(easy_button_x, easy_button_y, difficulty_button_width, difficulty_button_height)

game_state = "start"
difficulty = "medium"
#start Screen
def start_screen():
    screen.fill(d_grey)

    pygame.draw.rect(screen, green, easy_button, 2,border_radius=20)
    easy_text = game_font.render("Easy", True, green)
    easy_text_rect = easy_text.get_rect(center=easy_button.center)
    screen.blit(easy_text, easy_text_rect)

    pygame.draw.rect(screen, yellow, medium_button, 2,border_radius=20)
    medium_text = game_font.render("Medium", True, yellow)
    medium_text_rect = medium_text.get_rect(center=medium_button.center)
    screen.blit(medium_text, medium_text_rect)

    pygame.draw.rect(screen, red, hard_button,2, border_radius=20)
    hard_text = game_font.render("Hard", True, red)
    hard_text_rect = hard_text.get_rect(center=hard_button.center)
    screen.blit(hard_text, hard_text_rect)

    pygame.draw.rect(screen, l_grey, start_button, border_radius=20)
    start_text = game_font.render("Play", True, d_grey)
    text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, text_rect)


    game_text = game_font.render("PONG GAME", True, l_grey)
    screen.blit(game_text, (screen.get_width()/2 - game_text.get_width()/2, screen.get_height()*0.25))
    pygame.display.flip()


#main loop
running  = True
while running:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "start":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if easy_button.collidepoint(event.pos):
                    difficulty = "easy"
                    ball_speed_x = 7
                    ball_speed_y = 7
                    p_speed = 7
                     
                elif hard_button.collidepoint(event.pos):
                    difficulty = "hard"
                    ball_speed_x = 12
                    ball_speed_y = 12
                    p_speed = 12
                elif medium_button.collidepoint(event.pos):
                    difficulty = "medium"
                    ball_speed_x = 10
                    ball_speed_y = 10
                    p_speed = 10

                if start_button.collidepoint(event.pos):
                    game_state = "playing"

        elif game_state == "playing": 
            #key presses
            if event.type == pygame.KEYDOWN:
            #leftplayer
                if event.key == pygame.K_s:
                    player_speed = p_speed
                if event.key ==pygame.K_w:
                    player_speed = -p_speed
            
            

            if event.type == pygame.KEYUP:
            #leftplayer
                if event.key == pygame.K_s or event.key == pygame.K_w:
                    player_speed = 0

    #Game Logic

    if game_state == 'start':
        start_screen()

    elif game_state =='playing':
        #ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y
    
        #paddle movement
        player_paddle.y += player_speed


        # AI for opponent paddle
        if difficulty == 'easy':
            if opponent_paddle.centery < ball.centery:
                opponent_paddle.y += 7
            if opponent_paddle.centery > ball.centery:
                opponent_paddle.y -= 7
        elif difficulty == 'medium':
            if opponent_paddle.centery < ball.centery:
                opponent_paddle.y += 10
            if opponent_paddle.centery > ball.centery:
                opponent_paddle.y -= 10
        elif difficulty == "hard":
            if opponent_paddle.centery < ball.centery:
                opponent_paddle.y += 12
            if opponent_paddle.centery > ball.centery:
                opponent_paddle.y -= 12

        #wall collision(t/b)
        if ball.top <= 0 or ball.bottom >= screen.get_height():
            ball_speed_y *= -1

        #paddle collision (l/r)
        if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
            ball_speed_x *= -1

        #scoring
        if ball.left <= 0:
            opponent_score += 1
            ball.x = (screen.get_width() / 2) - (ball_size / 2)
            ball.y = (screen.get_height() / 2) - (ball_size / 2)
            ball_speed_x *= -1

        if ball.right > screen.get_width():
            player_score += 1
            ball.x = (screen.get_width() / 2) - (ball_size / 2)
            ball.y = (screen.get_height() / 2) - (ball_size / 2)
            ball_speed_x *= -1

        #drawing
        screen.fill(d_grey)
        pygame.draw.rect(screen, l_grey,player_paddle, border_radius=15)
        pygame.draw.rect(screen, l_grey, opponent_paddle, border_radius=15)
        pygame.draw.circle(screen, white, (ball.x + ball_size/2, ball.y + ball_size/2), ball_size/2)

        #scores display
        player_score_text = game_font.render(str(player_score),True,white)
        opponent_score_text = game_font.render(str(opponent_score),True,white)
        screen.blit(player_score_text,(screen.get_width()/4, 20))
        screen.blit(opponent_score_text,(screen.get_width()* 0.75, 20 ))

        pygame.display.flip()

    
    clock.tick(fps)

pygame.quit()
sys.exit()