import pygame
import random
import ChainTable

GAME_WINDOW_WIDTH = 600
GAME_WINDOW_HEIGHT = 480
FPS = 60
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()
headGridwidth= 30
GridXmax = GAME_WINDOW_WIDTH/headGridwidth 
GridYmax = GAME_WINDOW_HEIGHT/headGridwidth 
'''
SNAKE_SPEED =  1
RIGHT = (SNAKE_SPEED,0)
LEFT = (-1*SNAKE_SPEED,0)
UP = (0,-1*SNAKE_SPEED)
DOWN = (0,SNAKE_SPEED)
STATIC =(0,0)
'''

class Pos():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __repr__(self):
        return str((self.x,self.y))
    def move(self,key):
        newx = self.x
        newy = self.y
        if(key=='d'):
            newx +=  1
        elif(key=='a'):
            newx -=  1
        elif(key=='w'):
            newy -=  1
        elif(key=='s'):
            newy +=  1
        else:
            return Pos(self.x,self.y) 
        return Pos(newx,newy)
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

class Grid(pygame.sprite.Sprite):
    def __init__(self,posItem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((headGridwidth,headGridwidth))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = posItem.x*headGridwidth
        self.rect.y = posItem.y*headGridwidth

mapGrids = []
allmapGrids_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()

head = Pos(10,10)
headNode = ChainTable.Node(head)
body_with_head = ChainTable.ChainTable()
body_with_head.append(headNode)

for j in range(GridYmax):
    lineGrid = []
    for i in range(GridXmax):
        grid = Grid(Pos(i,j))
        lineGrid.append(grid)
        allmapGrids_sprites.add(grid)
    mapGrids.append(lineGrid)

#headGrid = Grid(head)
mapGrids[head.y][head.x].image.fill(YELLOW)
x = 'd'
rx = random.randint(1,int(GAME_WINDOW_WIDTH/headGridwidth)-2)
ry = random.randint(1,int(GAME_WINDOW_HEIGHT/headGridwidth)-2)
food = Pos(rx,ry)
mapGrids[food.y][food.x].image.fill(RED)
DicAppearPos ={}
DicAppearPos[(head.x,head.y)] = 1
i = 1
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    last = x
    keystate = pygame.key.get_pressed()
    if(keystate[pygame.K_DOWN]):
        x = 's'
    elif(keystate[pygame.K_UP]):
        x = 'w'
    elif(keystate[pygame.K_RIGHT]):
        x = 'd'
    elif(keystate[pygame.K_LEFT]):
        x = 'a'
    else:
        pass

    if(i%9==0):
        head = head.move(x)
        if(head.x >= 0 and head.x < GAME_WINDOW_WIDTH/headGridwidth and head.y < GAME_WINDOW_HEIGHT/headGridwidth and head.y >= 0):
            '''
            if ( DicAppearPos.has_key((head.x,head.y)) ):
                print DicAppearPos
                print ("double item")
                running = False
                break
            '''
            mapGrids[head.y][head.x].image.fill(YELLOW)
            newheadNode = ChainTable.Node(head)
            body_with_head.append(newheadNode)
            if ( DicAppearPos.has_key((head.x,head.y)) ):
                print ("double item")
                running = False
                break
                #DicAppearPos[(head.x,head.y)] = DicAppearPos[(head.x,head.y)]  + 1
            else:
                DicAppearPos[(head.x,head.y)] = 1

            if(not(head == food)):
                lastBody = body_with_head.getItem(0)
                if( DicAppearPos.has_key((lastBody.x,lastBody.y)) ):
                    del DicAppearPos[(lastBody.x,lastBody.y)]
                #print (lastBody)
                #print (DicAppearPos.has_key((lastBody.x,lastBody.y)))
                #del DicAppearPos[(lastBody.x,lastBody.y)]
                mapGrids[lastBody.y][lastBody.x].image.fill(GREEN)
                body_with_head.delete(0)
            else:
                rx = random.randint(1,int(GAME_WINDOW_WIDTH/headGridwidth)-2)
                ry = random.randint(1,int(GAME_WINDOW_HEIGHT/headGridwidth)-2)
                food = Pos(rx,ry)
                mapGrids[food.y][food.x].image.fill(RED)
            #print (body_with_head.length)
        else:
            print ("Game Over")
            running = False
    i += 1
    allmapGrids_sprites.draw(screen)
    pygame.display.flip()
     
pygame.quit()
print (body_with_head.length)
for i in range(body_with_head.length):
    print (i)
    print (body_with_head.getItem(i))
print (DicAppearPos)
