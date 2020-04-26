import pygame
import numpy as np

WIDTH, HEIGTH = 750, 750

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGTH))

pygame.display.set_caption('Mouse Repeler')

clock = pygame.time.Clock()

COLORS = {'k':(0,0,0),'w':(255,255,255),'g':(0,255,0),'r':(255,0,0),'y':(255,255,0)}

G = 1e9
mBall = 1000000
mMouse = 200
mFix = 500
r = 5

deltaT = 0.0001

class Ball:
    def __init__(self,x,y,r):
        self.pos = np.array([x,y])
        self.pos0 = np.array([x,y])
        self.r = r
        self.v = np.zeros(2)
    
    def plot(self):
        pass
        pygame.draw.circle(screen,COLORS['y'],(int(self.pos[0]),int(self.pos[1])),self.r,0)
        
    def update(self,x,y,repeal):
        F1 = np.zeros(2)
        # Repel Force
        r = np.array([x,y])
        d = (r-self.pos)
        normD = np.linalg.norm(d)
        if repeal and normD < self.r*10 and normD > self.r*2:
            F1 = -(G*mBall*mMouse/(normD**3))*d
        # Atrack Force
        d = self.pos0-self.pos
        F2 = np.zeros(2)
        normD = np.linalg.norm(d)
        if normD > self.r*4:
            F2 = (G*mBall*mFix/(normD**3))*d
        a = (F2+F1)/mBall
        damping = 1
        if not repeal:
            damping = normD/(WIDTH+HEIGTH)
        self.v += damping*a*deltaT
        self.pos += self.v*deltaT+0.5*a*deltaT**2   
             
x = np.linspace(5+2*r,WIDTH-5+2*r,50)
y = np.linspace(5+2*r,HEIGTH-5+2*r,50)
x,y = np.meshgrid(x,y)
x = x.flatten()
y = y.flatten()
balls = []
for i in range(0,x.size):
    balls.append(Ball(x[i],y[i],r))
  
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(COLORS['k'])
    
    x,y = pygame.mouse.get_pos()
    repeal = True
    if x == 0 or x == WIDTH-1 or y == 0 or y == HEIGTH-1:
        repeal = False    
    for ball in balls:
        ball.update(x,y,repeal)
        ball.plot()
    
    pygame.display.update()
    
    clock.tick(30)

pygame.quit()