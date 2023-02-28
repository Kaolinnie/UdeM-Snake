import sprites as sp
import ttgo as dev
import snake
        
class Apple:
    def __init__(self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos
    def effect(self,player):
        return player
    def spawn(self):
        dev.draw_image(self.xPos,self.yPos,self.sprite)
    
class Red_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.apple
    def effect(self, player):
        player.biggerSnake()
        player.score+=1
        return player

    
class Golden_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.golden_apple
    def effect(self, player):
        player.biggerSnake()
        player.score+=10
        return player
    
class Poison_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.poison_apple
    def effect(self, player):
        player.isAlive = False
        return player
    
    
class Speed_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.speed_apple
    def effect(self, player):
        player.biggerSnake()
        player.speed+=4
        player.score+=5
        return player
    
class Timed_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.timed_apple
    def effect(self, player):
        player.biggerSnake()
        player.score+=1
        return player
    def spawn(self):
        dev.draw_image(self.xPos,self.yPos,self.sprite)
class Eaten_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.eaten_apple
        
    def effect(self, player):
        playerLen = len(player.position)-2
        if playerLen == 0:
            player.isAlive=False
            return player
        numToCut = random.randint(1,playerLen)
        for i in range(numToCut):
            player.position.pop()
        player.score+=1
        return player
    
    def spawn(self):
        dev.draw_image(self.xPos,self.yPos,self.sprite)
        
    def effect(self, player):
        player.biggerSnake()
        player.score+=5
        return player
    
class Strength_Apple(Apple):
    def __init__(self,xPos,yPos):
        Apple.__init__(self,xPos,yPos)
        self.sprite = sp.strength_apple
        
    def effect(self, player):
        player.biggerSnake()
        player.size+=5
        player.score+=5
        return player
   
        
    def effect(self, player):
        player.score+=5
        return player
        behindPlayer = []
        length = len(player['position'])-1
        beforeTail = player['position'][length-1]
        tail = player['position'][length]
        vectorX = beforeTail[0] - tail[0]*2
        vectorY = beforeTail[1] - tail[1]*2
        snake.spawn_obstacle(vectorX, vectorY)
    