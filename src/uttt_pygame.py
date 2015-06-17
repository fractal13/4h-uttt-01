from uttt_data import *
from pygame_game import PygameGame
import pygame, pygame.locals
import uttt_data

class UTTTGame(PygameGame):

    def __init__(self, width_px, height_px, frames_per_second, data, send_queue):
        # PygameGame sets self.width and self.height        
        PygameGame.__init__(self, "Ultimate Tic Tac Toe", width_px, height_px, frames_per_second)
        self.data = data
        self.send_queue = send_queue
        self.z = 0
        self.x = 0
        self.c = 0
        self.n = 0
        self.b = 0
        self.m = 0
        self.a = 0
        self.s = 0
        self.v = 0
        pygame.font.init()
        pygame.mixer.init()
        self.font = pygame.font.SysFont("OCR A Extended",17)
        pygame.mixer.music.load('Mario.mp3')
        pygame.mixer.music.play(-1, 0.0)
        self.coin = pygame.mixer.Sound('coin.wav')
        self.firstTurn = True
        self.goomba = pygame.image.load("goomba.png")
        self.mario = pygame.image.load("mario.png")
        self.bg = pygame.image.load("bg1.png")
        self.bg2 = pygame.image.load("bg2Cropped2.png")
        self.mute = False
        self.pause = False
        return

    def handle_state(self):
        if self.data:
            state = self.data.GetState()
            if state in [ uttt_data.STATE_SHOW_SIGNUP, uttt_data.STATE_WAIT_SIGNUP, 
                          uttt_data.STATE_SIGNUP_FAIL_USERNAME,
                          uttt_data.STATE_SHOW_LOGIN, uttt_data.STATE_WAIT_LOGIN, uttt_data.STATE_LOGIN_FAIL,
                          uttt_data.STATE_SIGNUP_FAIL_EMAIL, uttt_data.STATE_SIGNUP_FAIL_PASSWORD,
                          uttt_data.STATE_SIGNUP_FAIL_PASSWORD_UNMATCHED, uttt_data.STATE_SIGNUP_OK ]:
                # minimize window
                #pygame.display.iconify()
                if self.screen.get_size() != ( 1, 1 ):
                    print "shrink"
                    self.screen = pygame.display.set_mode(
                        # set the size
                        (1, 1),
                        # use double-buffering for smooth animation
                        pygame.DOUBLEBUF |
                        # apply alpha blending
                        pygame.SRCALPHA |
                        # allow resizing
                        pygame.RESIZABLE)
                
            elif state in [ uttt_data.STATE_WAIT_GAME, uttt_data.STATE_SHOW_GAME,
                            uttt_data.STATE_GAME_OVER, uttt_data.STATE_TURN_FAILED,
                            uttt_data.STATE_WAIT_TURN ]:
                # unminimize window
                if self.screen.get_size() != ( self.width, self.height ):
                    print "WHAT?  pygame doesn't support unminimize?"
                    self.screen = pygame.display.set_mode(
                        # set the size
                        (self.width, self.height),
                        # use double-buffering for smooth animation
                        pygame.DOUBLEBUF |
                        # apply alpha blending
                        pygame.SRCALPHA |
                        # allow resizing
                        pygame.RESIZABLE)
            elif state in [ uttt_data.STATE_SOCKET_CLOSED, uttt_data.STATE_SOCKET_ERROR,
                            uttt_data.STATE_ERROR ]:
                # close
                if self.data.GetWinner() == PLAYER_N:
                    print "KEEP GOING"
                if self.data.GetWinner() == PLAYER_X:
                    print "You Win"
                if self.data.GetWinner() == PLAYER_O:
                    print"You Lose"
                print "Socket closed, or other error, pygame will quit."
                pygame.quit()
            elif state in [ uttt_data.STATE_SOCKET_OPEN ]:
                # what should I do?
                pass
            else:
                print "Unknown state in pygame: ", state

        return

    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        self.handle_state()
        if 1 in newbuttons:
            if self.data.GetNextPlayer() != self.data.GetPlayer():
                # not our turn
                print "YOU LITTLE REBEL"
                return

        if 1 in newbuttons:
            self.coin.play()
            print "working"
            
            mX,mY = mouse_position[0], mouse_position[1]
            col = mX / (self.width/9)
            row = mY / (self.height/9)
            board = 3 * (row / 3) + (col / 3)
            position = 3 * (row % 3) + (col % 3)
            
            if self.data and self.send_queue:
                if (self.data.GetNextBoard() == board) and self.firstTurn == False:
                    text = self.data.SendTurn(board, position)
                    print "pygame: queuing: %s" % (text, )
                    self.send_queue.put(text)
                elif self.firstTurn == True:
                    text = self.data.SendTurn(board, position)
                    print "pygame: queuing: %s" % (text, )
                    self.send_queue.put(text)
                    self.firstTurn = False

        if pygame.K_m in newkeys:
            if self.mute == False:
                self.mute = True
                pygame.mixer.music.set_volume(0.0)
            elif self.mute == True:
                self.mute = False
                pygame.mixer.music.set_volume(0.5)

        if pygame.K_p in newkeys:
            if self.pause == False:
                self.pause = True
                pygame.mixer.music.pause()
            elif self.pause == True:
                self.pause = False
                pygame.mixer.music.unpause()
                
        if self.data.GetNextBoard() == -1:
            self.z = 255
            self.x = 255
            self.z = 255
            self.c = 255
            self.v = 255
            self.b = 255
            self.n = 255
            self.m = 255
            self.a = 255
            self.s = 255
        else:
            self.z = 0
            self.x = 0
            self.z = 0
            self.c = 0
            self.v = 0
            self.b = 0
            self.n = 0
            self.m = 0
            self.a = 0
            self.s = 0

        if self.data.GetNextBoard() == 0:
            self.x = 255
        else:
            self.x = 0

        if self.data.GetNextBoard() == 1:
            self.z = 255
        else:
            self.z = 0
            
        if self.data.GetNextBoard() == 2:
            self.c = 255
        else:
            self.c = 0
            
        if self.data.GetNextBoard() == 3:
            self.v = 255
        else:
            self.v = 0
            
        if self.data.GetNextBoard() == 4:
            self.b = 255
        else:
            self.b = 0
            
        if self.data.GetNextBoard() == 5:
            self.n = 255
        else:
            self.n = 0
            
        if self.data.GetNextBoard() == 6:
            self.m = 255
        else:
            self.m = 0
            
        if self.data.GetNextBoard() == 7:
            self.a = 255
        else:
            self.a = 0
            
        if self.data.GetNextBoard() == 8:
            self.s = 255
        else:
            self.s = 0

        
        return

    def paint(self, surface):
    #prints the background
        
    #middle
        rect = pygame.Rect(self.width/3,self.height/3,self.width/3,self.height/3)
        surface.fill((self.b,0,0),rect )
    #bottom right
        rect = pygame.Rect(self.height/3*2,self.height/3*2,self.width/3,self.height/3)
        surface.fill((self.s,0,0),rect )
    #top right
        rect = pygame.Rect(self.width/3*2,0,self.width/3,self.height/3)
        surface.fill((self.c,0,0),rect )
    #top middle
        rect = pygame.Rect(self.width/3,0,self.width/3,self.height/3)
        surface.fill((self.z,0,0),rect )
    #middle left
        rect = pygame.Rect(0,self.height/3,self.width/3,self.height/3)
        surface.fill((self.v,0,0),rect )
    #top left
        rect = pygame.Rect(0,0,self.width/3,self.height/3)
        surface.fill((self.x,0,0),rect )
    #bottom left
        rect = pygame.Rect(0,self.height/3*2,self.width/3,self.height/3)
        surface.fill((self.m,0,0),rect )
    #middle right
        rect = pygame.Rect(self.height/3*2,self.width/3,self.width/3,self.height/3)
        surface.fill((self.n,0,0),rect )
    #bottom middle
        rect = pygame.Rect(self.width/3,self.height/3*2,self.width/3,self.height/3)
        surface.fill((self.a,0,0),rect )

    # Background
        surface.blit(self.bg2, (0,0))

    # HUD
        opponent = "You are playing: " + self.data.GetOpponentName()
        self.drawTextLeft(surface, opponent, (0, 0, 0), 25, 35, self.font)

        currentTurn = "It is " + self.data.GetNextPlayer() + "'s turn"
        self.drawTextLeft(surface, currentTurn, (0, 0, 0), 25, 45, self.font)

        you = "You are " + self.data.GetPlayer() + "s"
        self.drawTextLeft(surface, you, (0, 0, 0), 25, 55, self.font)
        
    
        # Regular Lines
        for i in range(1,9):
            pygame.draw.line(surface, (255,255,255), (0, i*self.height/9), (self.width, i*self.height/9))
        for j in range(1,9):
            pygame.draw.line(surface, (255,255,255), (j*self.width/9, 0), (j*self.height/9, self.height))

        # Board Lines
        for k in range(1,3):
            pygame.draw.line(surface, (255,255,0), (0, k*self.height/3), (self.width, k*self.height/3), 3)
        for l in range(1,3):
            pygame.draw.line(surface, (255,255,0), (l*self.width/3, 0), (l*self.height/3, self.height), 3)

        # Markers
        for board in range(9):
            for position in range(9):
                col = 3 * (board % 3) + position % 3
                row = 3 * (board / 3) + position / 3
                x = int((col + .5) * self.width / 9)
                y = int((row + .5) * self.height / 9)
                marker = self.data.GetMarker(board, position)
                if marker == uttt_data.PLAYER_X:
                    #pygame.draw.circle(surface, (0,0,255), (x, y), 14)
                    surface.blit(self.goomba, (x - 15, y - 15))
                elif marker == uttt_data.PLAYER_O:
                    #pygame.draw.circle(surface, (0,255,0), (x, y), 14)
                    surface.blit(self.mario, (x - 30, y - 30))
        return

    def drawTextLeft(self, surface, text, color, tX, tY, font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomleft = (tX, tY)
        surface.blit(textobj, textrect)

def uttt_pygame_main(data, send_queue):
    game = UTTTGame(600, 600, 30, data, send_queue)
    game.main_loop()
    return

if __name__ == "__main__":
    uttt_pygame_main(UTTTData(), None)
