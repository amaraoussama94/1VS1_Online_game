# client
import pygame
import pickle
from network import Network




width = 600
height = 600

class Button :
    def __init__(self,text,x,y,color):
        self.text=text
        self.x=x
        self.y=y
        self.color=color
        self.width=150
        self.height=80
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        font=pygame.font.SysFont("comicsans",40)
        text= font.render(self.text,1,(255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)) )# to make text in the center
    def click(self,pos): # check if we press the button
        x1=pos[0]
        y1=pos[1]
        if self.x<= x1 <=self.x+self.width and self.y<= y1 <=self.y+self.height :
            return True
        else:
            return False


def redraw_window(win, game,p):
    win.fill((125, 125, 125))
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Waiting for player ... ", 1, (255, 255, 255))
        win.blit(text,(width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()
    else :
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Your Move.... ", 1, (0, 255, 100))
        win.blit(text, (20,200))
        text = font.render("Opponents Move.... ", 1, (0, 255, 100))
        for btn in btns:
            btn.draw(win)
        win.blit(text, (300, 200))
        move1=game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent() :
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render( move2, 1, (0, 0, 0))
        else :
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked in", 1, (0, 0, 0))
            else  :
                text1 = font.render("Waiting.....", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked in", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting.....", 1, (0, 0, 0))
            if p == 1:
                win.blit(text2, (50, 350))
                win.blit(text1, (350, 350))
            else:
                win.blit(text1, (50, 350))
                win.blit(text2, (350, 350))

        pygame.display.update()





def main():
    global game
    run=True
    clock=pygame.time.Clock()
    n=Network()
    player = int(n.get_p())
    print("you are player",player)

    while run :
        clock.tick(60)
        try:
            game=n.send("get")

        except:
            run=False
            print("Couldn't get game")
            break
        if game.bothWent():
            redraw_window(win,game,player)
            pygame.time.delay(500)
            try:
                game =n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            font = pygame.font.SysFont("comicsans", 50)
            if (game.winner()==1 and player==1) or (game.winner()==0 and player==0):
                text = font.render("You Won!", 1, (255, 255, 255))
            elif game.winner()==-1 :
                text = font.render("Tie Game!", 1, (255, 255, 255))
            else :
                text = font.render("You Lost!", 1, (255, 255, 255))

            win.blit(text, (width/2 -text.get_width()/2, height/2 -text.get_height()/2)) # text in the mid of the screen
            pygame.display.update()
            pygame.time.delay(2000)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run=False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos =pygame.mouse.get_pos()
                for  bts in btns:
                    if bts.click(pos) and game.connected():
                        if player==0:
                            if not game.p1Went:
                                n.send(bts.text) # send("Rock") |send("Paper")|send("Scissors")
                        else:
                            if not game.p2Went:
                                n.send(bts.text)
        redraw_window(win,game,player)
        pygame.display.update()
def menu_screen ():
    run= True
    clock=pygame.time.Clock()

    while run:
        win.fill((128, 128, 128))
        clock.tick(60)
        font=pygame.font.SysFont("comicsans",60)
        text=font.render('Click to Play...',1,(255,0,0))
        win.blit(text,(150,260))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                quit()
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run=False
    main()



pygame.font.init()
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("client")
btns =[Button("Rock",50,400,(0,0,0)),Button("Scissors",250,400,(255,0,0)),Button("Paper",450,400,(0,255,2))]
while True :
    menu_screen ()






