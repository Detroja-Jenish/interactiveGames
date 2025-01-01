from Calliberation import Calliberation
from Game.AstroidShooter import AstroidShooter
from Game.ClimbBall import ClimbBall
from gameGlobals import GameGlobals

game = AstroidShooter()
# def main():
calliberation = Calliberation()
while not GameGlobals.quit:
    if GameGlobals.startToPlay:
        game.play()
    else:
        calliberation.doCaliber()

# main()