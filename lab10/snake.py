import pygame
from pygame.math import Vector2
import datetime
import random
import psycopg2 
import pygame_menu

pygame.init()

conn = psycopg2.connect(
    host="localhost",
    database="snake",
    user="postgres",
    password="11556595"
)

cur = conn.cursor()

class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)] 
        self.eated = False 
        self.isDead = False 

    
    def drawingSnake(self):
        for block in self.body: 
            body_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size) 
            pygame.draw.rect(screen, (0 ,128 ,0), body_rect)
        snake_head = pygame.Rect(self.body[0].x * cell_size, self.body[0].y * cell_size, cell_size, cell_size)
        headTexture = pygame.image.load('snakehead.png')
        headTexture = pygame.transform.scale(headTexture, (40, 40))
        screen.blit(headTexture, snake_head)

    
    def snakeMoving(self):
        if self.eated == True: 
            body_copy = self.body[:] 
            body_copy.insert(0, body_copy[0] + direction) 
            self.body = body_copy[:] 
            self.eated = False
        else:
            body_copy = self.body[:-1] 
            body_copy.insert(0, body_copy[0] + direction) 
            self.body = body_copy[:]


class Fruit:
    def __init__(self):
        self.randomize() 
    
    def drawingFruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size) 
        self.food = pygame.image.load(f'food{self.randomFood}.png').convert_alpha() 
        self.food = pygame.transform.scale(self.food, (35, 35)) 
        
        screen.blit(self.food, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 2) 
        self.y = random.randint(0, cell_number - 2) 
        self.pos = Vector2(self.x, self.y)
        self.randomFood = random.randint(1, 3) 


class Game:
    def __init__(self):
        self.snake = Snake() 
        self.fruit = Fruit() 
        self.level = 1 
        self.score = 0 

    
    def update(self):
        self.snake.snakeMoving()
        self.checkCollision()
        
    def drawElements(self):
        self.snake.drawingSnake()
        self.fruit.drawingFruit()
        self.scoreDrawing()
    
    def checkCollision(self):
        if(self.fruit.pos == self.snake.body[0]): 
            self.snake.eated = True
            
            if(self.fruit.randomFood == 1):
                self.score += 1
            if(self.fruit.randomFood == 2):
                self.score += 2
            if(self.fruit.randomFood == 3):
                self.score += 3
            self.fruit.randomize() 
            self.levelAdding() 

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

        for block in wall_coordinates:
            if block == self.fruit.pos:
                self.fruit.randomize()
        

    def gameOver(self):
        if self.snake.body[0].x >= 19:
            return True
        if self.snake.body[0].x <= 0:
            return True
        if self.snake.body[0].y >= 19:
            return True
        if self.snake.body[0].y <= 0:
            return True
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                return True
            
        for block in wall_coordinates:
            if block == self.snake.body[0]:
                return True
        return False
    
    
   
    def levelAdding(self):
        global snake_speed
        if self.score // 3 > self.level:
            self.level += 1
            snake_speed -= 10
            pygame.time.set_timer(SCREEN_UPDATE, snake_speed) # increasing speed
    
    
    def scoreDrawing(self):
        score_text = "Score: " + str(self.score)
        score_surface = font.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect(center = (cell_size * cell_number - 150, 40))
        screen.blit(score_surface, score_rect)

        level_text = "Level: " + str(self.level)
        level_surface = font.render(level_text, True, (56, 74, 12))
        level_rect = level_surface.get_rect(center = (cell_size * cell_number - 150, 70))
        screen.blit(level_surface, level_rect)

    def spawingWalls(self):
        if(self.level >= 3):
            wall_coordinates.append(Vector2(9, 8))
            wall_coordinates.append(Vector2(9, 9))
            wall_coordinates.append(Vector2(9, 10))
            wall_coordinates.append(Vector2(9, 11))
            for wall in wall1:
                wall_rect = pygame.Rect(wall.x * cell_size, wall.y * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
        
        if(self.level >= 4):
            for wall in range(0, 20):
                wall_rect = pygame.Rect(0, wall * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(0, wall))
        if(self.level >= 5):
            for wall in range(0, 20):
                wall_rect = pygame.Rect(19 * cell_size, wall * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(19, wall))
        if(self.level >= 6):
            for wall in range(1, 4):
                wall_rect = pygame.Rect(wall * cell_size, 3 * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(wall, 3))
        if(self.level >= 7):
            for wall in range(1, 4):
                wall_rect = pygame.Rect(wall * cell_size, 10 * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(wall, 10))
        if(self.level >= 8):
            for wall in range(1, 4):
                wall_rect = pygame.Rect(wall * cell_size, 16 * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(wall, 16))
        if(self.level >= 9):
            for wall in range(16, 19):
                wall_rect = pygame.Rect(wall * cell_size, 3 * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(wall, 3))
        if(self.level >= 10):
            for wall in range(16, 19):
                wall_rect = pygame.Rect(wall * cell_size, 10 * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(wall, 10))
        if(self.level >= 11):
            for wall in range(16, 19):
                wall_rect = pygame.Rect(wall * cell_size, 16 * cell_size, cell_size, cell_size)
                screen.blit(wall_texture, wall_rect)
                wall_coordinates.append(Vector2(wall, 16))
                
        
    def pauseState(self):
        global isPause
        if isPause == False:
            pause_image = pygame.image.load('pause.png') 
            pause_rect = pause.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
            screen.blit(pause, pause_rect)
            pygame.display.flip()
            pygame.time.set_timer(SCREEN_UPDATE, 0)
            isPause = True
        else:
            pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
            isPause = False


clock = pygame.time.Clock()
cell_size = 40
cell_number = 20
direction = Vector2(1, 0) 
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number)) # creating screen with are 800x800 or 20x20 cells square
done = False


font = pygame.font.Font('font.ttf', 25) 

nowSeconds = int((datetime.datetime.now()).strftime("%S"))

game = Game() 
snake_speed = 150

wall1 = [Vector2(9, 8), Vector2(9, 9), Vector2(9, 10), Vector2(9, 11)]
wall_texture = pygame.image.load('cobble4040.png')
wall_coordinates = []
pause = pygame.image.load('/Users/Владелец/Desktop/q/lab10/pause.png')

isPause = False


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, snake_speed)


def name_checker(NAMEBOX):
    global user_name
    user_name = str(NAMEBOX.get_value())
    cnt = 0
    cur.execute(' SELECT * FROM snake_score ')
    data = cur.fetchall()

    for row in data:
        if user_name == str(row[1]):
            cnt += 1
    if cnt > 0:
        print(f'User with this name is already exist, the level of this user is: {int(row[2]) // 3}, please enter another name: \n')
    else: start_the_game()

def start_the_game():
    global done
    global direction
    global nowSeconds
    global seconds
    global user_name
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
           
            if(event.type == SCREEN_UPDATE):
                game.update()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game.pauseState()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if direction.x != -1:
                    direction = Vector2(1, 0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if direction.x != 1:
                    direction = Vector2(-1, 0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if direction.y != 1:
                    direction = Vector2(0, -1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if direction.y != -1:
                    direction = Vector2(0, 1)   
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                cur.execute(f''' INSERT INTO snake_score("username", "user_score") VALUES( '{user_name}', '{game.score}'); ''')

                conn.commit()
                cur.close()
                conn.close()
                done = True

        if(game.gameOver() == True):

            cur.execute(f''' INSERT INTO snake_score("username", "user_score") VALUES( '{user_name}', '{game.score}'); ''')

            conn.commit()
            cur.close()
            conn.close()
            done = True

    
        time = datetime.datetime.now()
        seconds = int(time.strftime("%S"))
        if abs(seconds - nowSeconds) > 3:
            game.fruit.randomize()
            nowSeconds = seconds
        screen.fill((175, 215, 70))
        game.spawingWalls()
        game.drawElements()
        pygame.display.flip()
        clock.tick(60)



menu = pygame_menu.Menu('Welcome', 800, 800,
                       theme=pygame_menu.themes.THEME_BLUE)

name_box = menu.add.text_input('Name :', default='username')
menu.add.button('Play', name_checker, name_box)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)

pygame.quit()