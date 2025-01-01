from Calliberation import Calliberation
from ClimbBall import ClimbBall
from gameGlobals import GameGlobals

game = ClimbBall()
# def main():
calliberation = Calliberation()
while not GameGlobals.quit:
    if GameGlobals.startToPlay:
        game.play()
    else:
        calliberation.doCaliber()

# main()