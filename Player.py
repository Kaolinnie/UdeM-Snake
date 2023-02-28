class Player:
    
    def __init__(self,name,dev):
        self.name = name
        self.speed = 5
        self.moveX = 0
        self.moveY = 1
        self.position = [[dev.screen_height//2,dev.screen_width//2],[dev.screen_height//2-10,dev.screen_width//2-10],]
        self.isAlive = True
        self.size = 10
        self.score = 0
    
    # Spawn the player in the middle screen
    def spawn_player(self, dev):
        for i in self.position:
            dev.fill_rect(i[0],i[1],self.size,self.size,'#000')
            
    # move the player
    def move_player(self,dev,gameover, apple, spawn_item,obstacles):
        padding = 10
        width = dev.screen_width - padding
        height = dev.screen_height - padding 
        
        for i in self.position:
            try:
                dev.fill_rect(i[0],i[1],self.size,self.size,'#000')
            except:
                self.isAlive = False
                return
        
        length = len(self.position)
        for i in range(length-1,0,-1):
            if i == 0: break
            self.position[i][0]=self.position[i-1][0]
            self.position[i][1]=self.position[i-1][1]
        self.position[0][0] += self.moveX * self.speed
        self.position[0][1] += self.moveY * self.speed
        
        newPos = self.position[0]
        if newPos[0] < padding or newPos[0] > width or newPos[1] < padding or newPos[1] > height:
            self.isAlive = False
            return
        self.collide_apple(apple,spawn_item,dev)
        self.collide_block(obstacles)

        for i in range(len(self.position)):
            if i%2==0:
                color='#fff'
            else: color="#ff0"
            try:
                dev.fill_rect(self.position[i][0],self.position[i][1],self.size,self.size,color)
            except:
                self.isAlive = False
                    
    # collide with apple                
    def collide_apple(self, apple, spawn_item,dev):  
        if apple == None: return
        playerX = self.position[0][0]
        playerY = self.position[0][1]
        itemX = apple.xPos
        itemY = apple.yPos
        distance = ((playerX - itemX+5)**2 + (playerY - itemY+5)**2)**0.5

        if distance <= 15:
            self = apple.effect(self)
            dev.clear_screen('#000')
            spawn_item()
    
    # collide with block
    def collide_block(self, obstacles):  
        if len(obstacles) == 0: return
        playerX = self.position[0][0]
        playerY = self.position[0][1]
    
        for block in obstacles:
            distance = ((playerX - block["posX"]+5)**2 + (playerY - block["posY"]+5)**2)**0.5
            if distance <= 10:
                self.isAlive = False
    
    # increases the size of the snake
    def biggerSnake(self):
        length = len(self.position)-1
        beforeTail = self.position[length-1]
        tail = self.position[length]
        vectorX = beforeTail[0] - tail[0]
        vectorY = beforeTail[1] - tail[1]
        newSpot = [tail[0]+vectorX,tail[1]+vectorY]
        self.position.append(newSpot)

        
    def __str__(self):
        return self.name