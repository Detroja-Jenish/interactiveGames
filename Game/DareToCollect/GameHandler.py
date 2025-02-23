import json
import pygame

from gameGlobals import GameGlobals
from utils.getPersistentPath import getPersistentPath


def notToDo(pt1,pt2):
    pass
def fun1(pt1,pt2):
    pt2.x += 1

def fun2(pt1,pt2):
    pt2.x += 1
    pt1.x += 1

def moveTo(pt1,pt2,args=[100,100,200,200]):
    x1,y1,x2,y2 = args
    if pt1.x != x1:
        if pt1.x > x1 : pt1.x -= 1
        else : pt1.x += 10
    if pt1.y != y1:
        if pt1.y > y1 : pt1.y -= 1
        else : pt1.y += 10
    if pt2.x != x2:
        if pt2.x > x2 : pt2.x -= 1
        else : pt2.x += 10
    if pt2.y != y2:
        if pt2.y > y2 : pt2.y -= 1
        else : pt2.y += 10

functions_register = {
    "fun1":fun1,
    "fun2":fun2,
    "moveTo":moveTo,
    "notToDo": notToDo
}

class Function:
    animation_time = 0
    def __init__(self):
        self.functions_register = {
            "fun1":self.fun1,
            "fun2":self.fun2,
            "moveTo":self.moveTo,
            "notToDo": self.notToDo
        }

    def update(self,function_name,pt1,pt2,args):
        print("from function handler class")
        if not args:self.functions_register[function_name](pt1,pt2)
        else:self.functions_register[function_name](pt1,pt2,args)
        
    def notToDo(self,pt1,pt2):
        pass
    def fun1(self,pt1,pt2):
        pt2.x += 1

    def fun2(self,pt1,pt2):
        pt2.x += 1
        pt1.x += 1

    def moveTo(self,pt1,pt2,args=[100,100,200,200,300]):
        self.animation_time += GameGlobals.dt
        x1,y1,x2,y2,total_animation_time = args
        progress = min(self.animation_time / total_animation_time, 1)
        print("progress", progress)
        pt1.x =  pt1.init_x + progress*(x1 - pt1.init_x)
        pt1.y = pt1.init_y + progress*(y1 - pt1.init_y)
        pt2.x = pt2.init_x + progress*(x2 - pt2.init_x)
        pt2.y = pt2.init_y + progress*(y2 - pt2.init_y)
class Level:
    level_number = 1
    current_state = 0
    collision_count = 0


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.init_x = x
        self.init_y = y
    def get_tupple(self):
        return (self.x, self.y)

class Spark:
    surface = pygame.Surface((GameGlobals.screen_width,GameGlobals.screen_height),pygame.SRCALPHA,32)
    surface = surface.convert_alpha()
    def __init__(self,pt1,pt2,functions, args):
        self.pt1 = pt1
        self.pt2 = pt2
        self.functions = functions
        self.destroy = False
        self.args = args
        self.functionHandler = Function()

    def draw(self):
        pygame.draw.line(Spark.surface,(255,0,0),self.pt1.get_tupple(), self.pt2.get_tupple(),width=10)

    def update(self):
        if Level.current_state >= len(self.functions) or self.functions[Level.current_state] == "destroy":
            self.destroy = True
            return
        function_name = self.functions[Level.current_state]
        # print(function_name)
        self.functionHandler.update(function_name,self.pt1,self.pt2,None if function_name not in self.args else self.args[function_name])
        # if function_name in self.args:
        #     print(self.args[function_name])
        #     functions_register[function_name](self.pt1,self.pt2,self.args[function_name])
        # else:functions_register[function_name](self.pt1,self.pt2)
    @classmethod
    def clearSurface(cls):
        cls.surface.fill((0,0,0,0))
        # cls.surface = cls.surface.convert_alpha()
    
    @classmethod
    def collide(cls,user_mask):
        spark_mask = pygame.mask.from_surface(cls.surface)
        if spark_mask.overlap(user_mask,(0,0)):
            Level.collision_count+=1


class Key:
    def __init__(self,pt):
        self.image = pygame.transform.scale_by(pygame.image.load(getPersistentPath("assets/images/Meteors/Meteor_07.png")), 1/5)
        self.mask = pygame.mask.from_surface(self.image)
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx = pt.x
        self.image_rect.centery = pt.y

    def collide(self,user_mask):
        return False if not user_mask.overlap(self.mask, (self.image_rect.x,self.image_rect.y)) else True
    def draw(self):
        GameGlobals.screen.blit(self.image,self.image_rect)

class GameHandler:
    def __init__(self):
        self.current_level = 1
        level_config = {}
        with open("levels/DareToCollect.json","r") as fp:
            level_config = json.load(fp=fp)
        self.sparks = [
            Spark(
                Point(i["init"]["x1"],i["init"]["y1"]), 
                Point(i["init"]["x2"],i["init"]["y2"]), 
                i["functions"],
                i["args"]
            ) for i in level_config[str(self.current_level)]["sparks"]
        ]
        self.keys = [
            Key(
                Point(i[0],i[1])
            )for i in level_config[str(self.current_level)]["keys"]
        ]

    def draw(self):
        for key in self.keys:
            key.draw()
        Spark.clearSurface()
        # Spark.surface.fill((0,0,0))
        # Spark.surface.convert_alpha()
        # pygame.transform.threshold(Spark.surface,Spark.surface,search_color=(0,0,0),set_color=(0,0,0,0))
        for spark in self.sparks:
            spark.update()
            spark.draw()
        GameGlobals.screen.blit(Spark.surface,(0,0))
    
    def collide(self,user_mask):
        Spark.collide(user_mask)
        for key in self.keys:
            if key.collide(user_mask):
                Level.current_state += 1
                Function.animation_time = 0
                self.keys.remove(key)
        
