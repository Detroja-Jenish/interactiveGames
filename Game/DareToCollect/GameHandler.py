import json
import pygame

from gameGlobals import GameGlobals
from utils.getPersistentPath import getPersistentPath
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
        self.functions_register[function_name](pt1,pt2,args)
        
    def notToDo(self,pt1,pt2,args):
        pass
    def fun1(self,pt1,pt2,args):
        pt2.x += 1

    def fun2(self,pt1,pt2,args):
        pt2.x += 1
        pt1.x += 1

    def moveTo(self,pt1,pt2,args):
        self.animation_time += GameGlobals.dt
        x1,y1,x2,y2,total_animation_time = args["x1"]*GameGlobals.screen_width,args["y1"]*GameGlobals.screen_height,args["x2"]*GameGlobals.screen_width,args["y2"]*GameGlobals.screen_height,args["total_animation_time"]
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
    def __init__(self,pt1,pt2,functions):
        self.pt1 = pt1
        self.pt2 = pt2
        self.function_names = list(functions.keys())
        self.destroy = False
        self.args = list(functions.values())
        self.functionHandler = Function()

    def draw(self):
        pygame.draw.line(Spark.surface,(255,0,0),self.pt1.get_tupple(), self.pt2.get_tupple(),width=10)

    def update(self):
        if Level.current_state >= len(self.function_names) or self.function_names[Level.current_state] == "destroy":
            self.destroy = True
            return
        function_name = self.function_names[Level.current_state]
        # print(function_name)
        self.functionHandler.update(function_name,self.pt1,self.pt2,self.args[Level.current_state])
        # if function_name in self.args:
        #     print(self.args[function_name])
        #     functions_register[function_name](self.pt1,self.pt2,self.args[function_name])
        # else:functions_register[function_name](self.pt1,self.pt2)
    @classmethod
    def clearSurface(cls):
        cls.surface.fill((0,0,0,0))

    @classmethod
    def drawSurface(cls):
        GameGlobals.screen.blit(cls.surface,(0,0))
    
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
                Point(i["init"]["x1"]*GameGlobals.screen_width,i["init"]["y1"]*GameGlobals.screen_height), 
                Point(i["init"]["x2"]*GameGlobals.screen_width,i["init"]["y2"]*GameGlobals.screen_height), 
                i["functions"]
            ) for i in level_config[str(self.current_level)]["sparks"]
        ]
        self.keys = [
            Key(
                Point(
                    i[0]*GameGlobals.screen_width,
                    i[1]*GameGlobals.screen_height
                    )
            )for i in level_config[str(self.current_level)]["keys"]
        ]

    def draw(self):
        for key in self.keys:
            key.draw()

        Spark.clearSurface()
        for spark in self.sparks:
            spark.update()
            spark.draw()
        Spark.drawSurface()
    
    def collide(self,user_mask):
        Spark.collide(user_mask)
        for key in self.keys:
            if key.collide(user_mask):
                Level.current_state += 1
                Function.animation_time = 0
                self.keys.remove(key)
        
