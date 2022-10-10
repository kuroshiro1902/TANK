import random
import pygame, sys
from pygame.locals import *

pygame.init()

pygame.display.set_caption('ALORA')
FPS = 60
fpsClock = pygame.time.Clock()
Screen = pygame.display.set_mode((800,600)) #12 hang, 16 cot

#BACKGROUND
Background= pygame.image.load('./images/grass.png')
# Background = pygame.transform.scale(Background_img,(800,600))
#WALLS
class Wall: # 46x42
    def __init__(self,x,y,path):
        self.x = x
        self.y = y
        #0    1
        self.location = [[x,y],[x+50,y],[x,y+50],[x+50,y+50]]
        #2    3
        self.this = pygame.image.load(path)
        self.rest = 3
    def draw(self):
        self.location = [[self.x,self.y],[self.x+50,self.y],[self.x,self.y+50],[self.x+50,self.y+50]]
        Screen.blit(self.this,(self.x,self.y))

Walls = []
    #create walls
for x in range(16):
    for y in range(1,11):
        if random.randint(0,100) < 40:
            wall = Wall(-50,-50,"./images/wall.png")
            wall.x = x*50
            wall.y = y*50
            Walls+=[wall]
#

# check collionsions for 4 directions
def L(Tank,Walls):
    for wall in Walls:
        if Tank.x == (wall.x+50): #axis
            wall_top_right_y = wall.location[1][1]
            wall_bottom_right_y = wall.location[3][1]
            tank_top_left_y = Tank.location[0][1]
            tank_bottom_left_y = Tank.location[2][1]
            #
            tank_dot_above_blocked = (wall_top_right_y <= tank_top_left_y) and (tank_top_left_y<=wall_bottom_right_y)
            tank_dot_under_blocked = (wall_top_right_y <= tank_bottom_left_y) and (tank_bottom_left_y<=wall_bottom_right_y)
            if tank_dot_above_blocked or tank_dot_under_blocked: 
                # print(Tank.x,wall.x+50)
                # print("DIEM TREN:",wall_bottom_right_y,tank_top_left_y,wall_top_right_y)
                # print("DIEM DUOI",wall_bottom_right_y,tank_bottom_left_y,wall_top_right_y)
                return False
    return True

#

#TANK
class Tank:
    def __init__(self,x,y,path):
        self.x = x
        self.y = y
        #x:0 , y:1
        #[0][0,1]    [1][0,1]
        self.location = [[x,y],[x+46,y],[x,y+42],[x+46,y+42]]
        #[2][0,1]    [3][0,1]
        self.path = path
        self.this = pygame.image.load(path)
        self.last_key = 'd'
    def draw(self):
        if self.y<0: self.y=0
        if self.x<0: self.x=0
        if self.x>756: self.x = 756
        if self.y>558: self.y = 558
        self.location = [[self.x,self.y],[self.x+46,self.y],[self.x,self.y+42],[self.x+46,self.y+42]]
        Screen.blit(self.this,(self.x,self.y))
        self.angle = 0
    def check_collision(self,Walls):
        pass
    def move(self,key):
        if key[K_w]:
            self.y -=2
            self.last_key = 'w'

        if key[K_a]:
            if L(self,Walls):
                self.x -=2
            self.last_key = 'a'
            
        if key[K_s]:
            self.y +=2
            self.last_key = 's'

        if key[K_d]:
            self.x +=2
            self.last_key = 'd'

        self.path = self.path[:len(self.path)-5]+self.last_key+".png"
        self.this = pygame.image.load(self.path)

TANK1 = Tank(0,0,"images/tank_blue/tank_blue_d.png")
TANK2 = Tank(750,550,"images/tank_red.png")
#

#GAME
i=0
while True:
    Screen.blit(Background,(0,0))
    TANK1.draw()
    TANK2.draw()
    for wall in Walls:
        wall.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    TANK1.move(keys)
    pygame.display.update()
    fpsClock.tick(FPS)
    