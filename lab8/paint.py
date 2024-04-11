import pygame

pygame.init()
FPS = 120
FramePerSec = pygame.time.Clock()
# Setting window size
win_x = 500
win_y = 500

win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption('Paint')

# Class for drawing 
class Drawing(object):
    def __init__(self):
        self.color = (128, 0, 0)
        self.width = 60
        self.height = 35
        self.rad = 6
        self.tick = 0
        self.time = 0
        self.play = False

    # Drawing Function
    def draw(self, win, pos):
        pygame.draw.circle(win, self.color, (pos[0], pos[1]), self.rad)
        if self.color == (255, 255, 255):
            pygame.draw.circle(win, self.color, (pos[0], pos[1]), 20)

    def click(self, win, list, list2):
        pos = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed() == (1, 0, 0) and pos[0] < 400:
            if pos[1] > 25:
                self.draw(win, pos)
        elif pygame.mouse.get_pressed() == (1, 0, 0):
            for button in list:
                if pos[0] > button.x and pos[0] < button.x + button.width:
                    if pos[1] > button.y and pos[1] < button.y + button.height:
                        self.color = button.color2
            for button in list2:
                if pos[0] > button.x and pos[0] < button.x + button.width:
                    if pos[1] > button.y and pos[1] < button.y + button.height:
                        if self.tick == 0:
                            if button.action == 1:
                                win.fill((255, 255, 255))
                                self.tick += 1
                            if button.action == 2 and self.rad > 4:
                                self.rad -= 1
                                self.tick += 1
                                pygame.draw.rect(
                                    win, (255, 255, 255), (410, 308, 80, 35))

                            if button.action == 3 and self.rad < 20:
                                self.rad += 1
                                self.tick += 1
                                pygame.draw.rect(
                                    win, (255, 255, 255), (410, 308, 80, 35))

                            if button.action == 5 and self.play == False:
                                self.play = True
                                self.time += 1
                            if button.action == 6:
                                self.play = False
                                self.time = 0

        # Отслеживание нажатий клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # Рисование треугольника
            pygame.draw.polygon(win, self.color, [(pos[0], pos[1] - self.rad), (pos[0] - self.rad, pos[1] + self.rad), (pos[0] + self.rad, pos[1] + self.rad)])
        elif keys[pygame.K_RETURN]:
            # Рисование круга
            pygame.draw.circle(win, self.color, pos, self.rad)
        elif keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            # Рисование квадрата
            pygame.draw.rect(win, self.color, (pos[0] - self.rad, pos[1] - self.rad, self.rad * 2, self.rad * 2))


# Class for buttons
class Button(object):
    def __init__(self, x, y, width, height, color, color2, outline=0, action=0, text=''):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.outline = outline
        self.color2 = color2
        self.action = action
        self.text = text

    # Class for drawing buttons
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), self.outline)
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, self.color2)
        pygame.draw.rect(win, (255, 255, 255), (410, 446, 80, 35))
        win.blit(text, (int(self.x + self.width / 2 - text.get_width() / 2), int(self.y + self.height / 2 - text.get_height() / 2)))


def drawHeader(win):
    # Drawing header space
    pygame.draw.rect(win, (188, 143, 143), (0, 0, 500, 25))
    pygame.draw.rect(win, (188, 143, 143), (0, 0, 400, 25), 2)
    pygame.draw.rect(win, (255, 245, 238), (400, 0, 100, 25), 2)

    # Printing header
    font = pygame.font.SysFont('comicsans', 30)

    toolsText = font.render('Tools', 1, (0, 0, 0))
    win.blit(toolsText, (int(450 - toolsText.get_width() / 2), int(26 / 2 - toolsText.get_height() / 2 + 2)))


def draw(win):
    player1.click(win, Buttons_color, Buttons_other)

    pygame.draw.rect(win, (0, 0, 0), (400, 0, 100, 500), 2)  # Drawing button space
    pygame.draw.rect(win, (255, 255, 255), (400, 0, 100, 500))
    pygame.draw.rect(win, (0, 0, 0), (0, 0, 400, 500), 2)  # Drawing canvas space
    drawHeader(win)

    for button in Buttons_color:
        button.draw(win)

    for button in Buttons_other:
        button.draw(win)

    pygame.display.update()


def main_loop():
    run = True
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                run = False

        draw(win)

        if 0 < player1.tick < 40:
            player1.tick += 1
        else:
            player1.tick = 0

        if 0 < player1.time < 4001:
            player1.time += 1
        elif 4000 < player1.time < 4004:
            player1.time = 4009
        else:
            player1.time = 0
            player1.play = False

    pygame.quit()


player1 = Drawing()
# Fill colored to our paint
win.fill((255, 255, 255))
pos = (0, 0)

# Defining color buttons
redButton = Button(453, 30, 40, 40, (255, 20, 147), (255, 20, 147))
blueButton = Button(407, 30, 40, 40, (255, 105, 80), (255, 105, 80))
greenButton = Button(407, 76, 40, 40, (220, 20, 60), (220, 20, 60))
orangeButton = Button(453, 76, 40, 40, (165, 42, 42), (165, 42, 42))
yellowButton = Button(407, 122, 40, 40, (188, 143, 143), (188, 143, 143))
purpleButton = Button(453, 122, 40, 40, (255, 160, 122), (255, 160, 122))
blackButton = Button(407, 168, 40, 40, (199, 21, 133), (199, 21, 133))
whiteButton = Button(453, 168, 40, 40, (255, 20, 147), (255, 20, 147), 1)

# Defining other buttons
clrButton = Button(407, 214, 86, 40, (201, 201, 201), (0, 0, 0), 0, 1, 'Clear')
eraserButton = Button(407, 214, 86, 40, (201, 201, 201), (0, 0, 0), 8, 'Eraser')
smallerButton = Button(407, 260, 40, 40, (201, 201, 201), (0, 0, 0), 0, 2, '-')
biggerButton = Button(453, 260, 40, 40, (201, 201, 201), (0, 0, 0), 0, 3, '+')
sizeDisplay = Button(407, 306, 86, 40, (0, 0, 0), (0, 0, 0), 1, 4, 'Size')

Buttons_color = [blueButton, redButton, greenButton, orangeButton,
                 yellowButton, purpleButton, blackButton, whiteButton]
Buttons_other = [clrButton, smallerButton, biggerButton,
                 sizeDisplay, eraserButton]

main_loop()
FramePerSec.tick(FPS)
