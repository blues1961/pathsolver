import pygame
import random
from astar import AStar

#Golbal constants

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE=(0,0,255)
LIGHT_GREY=(211,211,211)
LIGHT_RED=(192,192,192)
#Screen size

#Location description

TILE_WIDTH=5
TILE_HEIGHT=5
TILE_MARGIN=2

MAP_ROWS=80
MAP_COLS=100

SCREEN_WIDTH=MAP_COLS*(TILE_WIDTH+TILE_MARGIN)+100
SCREEN_HEIGHT=MAP_ROWS*(TILE_HEIGHT+TILE_MARGIN)+100


#Define mouse button
MOUSE_LEFT=1
MOUSE_MIDDLE=2
MOUSE_RIGHT=3


# Classes
class Game():

    astar=None
    map=None
    game_over=False
    score=0
    done = False

    def __init__(self):
        self.astar=AStar(MAP_COLS,MAP_ROWS)
        self.map=self.astar.map
        self.astar.print_map()
        self.game_over=False
        self.score=0
        self.done=False



    def process_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game.done=True
                pygame.quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
               if self.game_over==True:
                   self.__init__()
        return

    def run_logic(self):
        print('run logic')
        self.astar.currentNode.print()
        print(self.astar.endPos)
        self.astar.solverStep()
        if self.astar.currentNode.position==self.astar.endPos:
           self.game_over=True


    def display_frame(self,screen):
            # Set the screen background
            screen.fill(WHITE)

            # Draw the grid
            for row in range(MAP_ROWS):
                for column in range(MAP_COLS):
                    if self.map[row][column] == 0: color = WHITE
                    else: color=BLUE
                    pygame.draw.rect(screen,
                                     color,
                                     [(TILE_MARGIN + TILE_WIDTH) * column,
                                      (TILE_MARGIN + TILE_HEIGHT) * row,
                                      TILE_WIDTH,
                                      TILE_HEIGHT])


            for n in self.astar.closednodes:
                pygame.draw.rect(screen,LIGHT_GREY,[(TILE_MARGIN+TILE_WIDTH)*n.position[1],(TILE_MARGIN+TILE_HEIGHT)*n.position[0],TILE_WIDTH,TILE_HEIGHT])


            for n in self.astar.opennodes:
                pygame.draw.rect(screen,GREEN,[(TILE_MARGIN+TILE_WIDTH)*n.position[1],(TILE_MARGIN+TILE_HEIGHT)*n.position[0],TILE_WIDTH,TILE_HEIGHT])

            for pos in self.astar.path:
                 pygame.draw.rect(screen,RED,[(TILE_MARGIN+TILE_WIDTH)*pos[1],(TILE_MARGIN+TILE_HEIGHT)*pos[0],TILE_WIDTH,TILE_HEIGHT])

            pygame.draw.rect(screen,RED,[(TILE_MARGIN+TILE_WIDTH)*self.astar.endPos[1],(TILE_MARGIN+TILE_HEIGHT)*self.astar.endPos[0],TILE_WIDTH,TILE_HEIGHT])
            pygame.draw.rect(screen,RED,[(TILE_MARGIN+TILE_WIDTH)*self.astar.currentNode.position[1],(TILE_MARGIN+TILE_HEIGHT)*self.astar.currentNode.position[0],TILE_WIDTH,TILE_HEIGHT])
            pygame.display.flip()


def main():
    pygame.init()
    size=[SCREEN_WIDTH,SCREEN_HEIGHT]
    screen=pygame.display.set_mode(size)
    pygame.display.set_caption("A* - Visualisation")
    pygame.mouse.set_visible(True)
    clock=pygame.time.Clock()
    game=Game()
    game.game_over=False
    game.done=False
    while not game.done:
        game.process_events()
        if game.game_over!=True:
            game.run_logic()
            game.display_frame(screen)
            clock.tick(0)
    pygame.quit()

if __name__=="__main__":
    main()
