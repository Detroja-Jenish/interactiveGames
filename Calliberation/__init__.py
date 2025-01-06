from Camera import Camera
from EventHandler import Event, EventHandler
from Game.AstroidShooter import AstroidShooter
from gameGlobals import GameGlobals
import numpy as np
import json
import pygame
from utils.getPersistentPath import getPersistentPath

class Calliberation:
    def __init__(self):
                #print(data)
        self.cropping_rect = pygame.Rect(GameGlobals.config["calliberationCords"]["x"], GameGlobals.config["calliberationCords"]["y"], GameGlobals.config["calliberationCords"]["width"], GameGlobals.config["calliberationCords"]["height"])
                
            #print("exception genrated while creating cropping retangle")
        self.resizing = False
        self.moving = False
        self.offset_x = 0
        self.offset_y = 0
        self.resizing_margin = 10 

        self.eventHandler = EventHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : GameGlobals.doQuit()))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN, lambda _ : GameGlobals.doQuit(), condition = lambda e : e.key == pygame.K_q))
        self.eventHandler.registerEvent("setCalliber",Event( pygame.KEYDOWN, lambda _ : Camera.setCrop(self.cropping_rect.x,self.cropping_rect.y,self.cropping_rect.width,self.cropping_rect.height), lambda _ : GameGlobals.setIsCameraCallibered(True),lambda _:self.saveCalliberationData() ,condition=lambda e : e.key == pygame.K_c))
        self.eventHandler.registerEvent("reCalliber",Event(    pygame.KEYDOWN,    lambda _ :GameGlobals.setIsCameraCallibered(False),    condition= lambda e : e.key == pygame.K_r))
        self.eventHandler.registerEvent("start playing",Event(    pygame.KEYDOWN,    lambda _ :GameGlobals.setStartToPlay(True),    condition= lambda e : e.key == pygame.K_p))
        self.eventHandler.registerEvent("handleResize",Event(pygame.MOUSEBUTTONDOWN,lambda e : self.handleResize(e),lambda event: self.cropping_rect.collidepoint(event.pos)))
        self.eventHandler.registerEvent("deactiveResize",Event(pygame.MOUSEBUTTONUP,lambda _ :self.deactiveResize()))
        self.eventHandler.registerEvent("handleRectMove",Event(pygame.MOUSEMOTION,lambda e :self.handleRectMove(e)))
    def doCaliber(self):
        Camera.readFrame()
        if not Camera.ret:
            raise "Error occurred in capturing frame"
        frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        GameGlobals.screen.blit(frame_surface, (0, 0))
        pygame.draw.rect(GameGlobals.screen, (255, 0, 0), self.cropping_rect, 2)  # Draw a red rectangle with a border thickness of 2
        pygame.display.flip()
        self.eventHandler.checkEventOccurnce();


    def handleResize(self,event):
        if self.is_resizing_area(event.pos):
            self.resizing = True
        else:
            self.moving = True
            self.offset_x = self.cropping_rect.x - event.pos[0]
            self.offset_y = self.cropping_rect.y - event.pos[1]

    def deactiveResize(self):
        self.moving = False
        self.resizing = False

    def handleRectMove(self,event):
        if self.moving:
            self.cropping_rect.x = event.pos[0] + self.offset_x
            self.cropping_rect.y = event.pos[1] + self.offset_y
        elif self.resizing:
            # Resize the rectangle (only lower-right corner resizing for simplicity)
            self.cropping_rect.width = event.pos[0] - self.cropping_rect.x
            self.cropping_rect.height = event.pos[1] - self.cropping_rect.y

    def is_resizing_area(cls, mouse_pos):
        # Check if the mouse is within the resizing margin of the bottom-right corner
        return (
            abs(mouse_pos[0] - (cls.cropping_rect.x + cls.cropping_rect.width)) <= cls.resizing_margin and
            abs(mouse_pos[1] - (cls.cropping_rect.y + cls.cropping_rect.height)) <= cls.resizing_margin
        )
    
    def saveCalliberationData(self):
        configFilePath = getPersistentPath("config.json")
        print(configFilePath)
        try:
            with open(configFilePath,"r") as fp:
                data = json.load(fp)
        except:
            data = {}
        with open(configFilePath,"w") as fp:
            #print("from setCrop -> config.json -> write mode")
            data["calliberationCords"] = {
                "x":self.cropping_rect.x, "y":self.cropping_rect.y , "width":self.cropping_rect.width , "height":self.cropping_rect.height
            }
            json.dump(data,fp,indent=4)