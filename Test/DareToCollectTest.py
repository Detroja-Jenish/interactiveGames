import pygame
import json

line_config = {}
with open("./instruction.json","r") as fp:
    line_config = json.load(fp=fp)
pygame.init()
pygame.mixer.init()
font = pygame.font.Font(None, 74)
info = pygame.display.Info()
screen_width, screen_height = info.current_w - 10,info.current_h - 10
screen = pygame.display.set_mode((screen_width, screen_height))
quit = False
clock = pygame.time.Clock()


def fun1(pt1,pt2):
    pt2.x += 1

def fun2(pt1,pt2):
    pt2.x += 1
    pt1.x += 1

def moveTo(pt1,pt2,args=[100,100,200,200]):
    x1,y1,x2,y2 = args
    if pt1.x != x1:
        if pt1.x > x1 : pt1.x -= 1
        else : pt1.x += 1
    if pt1.y != y1:
        if pt1.y > y1 : pt1.y -= 1
        else : pt1.y += 1
    if pt2.x != x2:
        if pt2.x > x2 : pt2.x -= 1
        else : pt2.x += 1
    if pt2.y != y2:
        if pt2.y > y2 : pt2.y -= 1
        else : pt2.y += 1

functions_register = {
    "fun1":fun1,
    "fun2":fun2,
    "moveTo":moveTo
}

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def get_tupple(self):
        return (self.x, self.y)

class Line:
    def __init__(self,pt1,pt2,functions, args):
        self.pt1 = pt1
        self.pt2 = pt2
        self.functions = functions
        self.state = 0
        self.destroy = False
        self.args = args

    def draw(self,screen):
        pygame.draw.line(screen,(255,0,0),self.pt1.get_tupple(), self.pt2.get_tupple(),width=10)
    def update(self):
        if self.state >= len(self.functions) or self.functions[self.state] == "destroy":
            self.destroy = True
            return
        function_name = self.functions[self.state]
        if function_name in self.args:
            functions_register[function_name](self.pt1,self.pt2,self.args[function_name])
        functions_register[function_name](self.pt1,self.pt2)

# lines = [
#     Line(Point(100,100),Point(200,200),fun1, fun2)
#     ,Line(Point(100,300),Point(200,600),fun2, fun1)
# ]


lines = [
            Line(
                Point(i["init"]["x1"],i["init"]["y1"]), 
                Point(i["init"]["x2"],i["init"]["y2"]), 
                i["functions"],
                i["args"]
            ) for i in line_config
        ]

count = 0


while not quit:
    count += 1
    update_status = False
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n: 
            update_status = True

    screen.fill((200,200,200))
    for line in lines:
        if update_status : line.state += 1
        line.draw(screen)
        line.update()
        if line.destroy: lines.remove(line)

    pygame.display.flip()
    clock.tick(15)