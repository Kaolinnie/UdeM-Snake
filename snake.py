import ttgo as dev
import net
import mate
#import apps_two as apps
import apps
import ui
import random
import sprites as sp
import apples
from Player import Player
import time


bg = '#000'  # general background color
tick_counter = 0
apple_color = "#00A"
has_apple = False
# game state

me = None  # is 0 when non-networked, and 0 or 1 when networked

# the following global variables are useful for the networked version

networked   = False  # are we playing over the network?
random_seed = 0      # to get same random order on both nodes, set later
msg_type    = None   # type of the messages sent between the nodes, set later
ping_timer  = 0      # used to check that the mate is still with us
pong_timer  = 0
bestScore = 0
gameActive = True
tick_counter = 0
    
def init_game():
    global me, playerOne, apple, obstacles, despawn_tick_check, gameActive,tick_counter

    me = None
    tick_counter = 0
    playerOne = Player("playerOne", dev)
    despawn_tick_check = -1
    playerOne.spawn_player(dev)
    apple = None
    obstacles = []    
    gameActive = True
    
    dev.clear_screen(bg)
    
    
def spawn_obstacle(posX,posY):
    global obstacles
    newObstacle = {}
    newObstacle["posX"] = posX
    newObstacle["posY"] = posY
    obstacles.append(newObstacle)
    
def draw_obstacles():
    global obstacles
    for obstacle in obstacles:
        dev.fill_rect(obstacle["posX"],obstacle["posY"],10,10,'#0f0')
def spawn_item():
    global apple,spawns, despawn_tick_check, tick_counter
    chosenItem = random.randint(0,6)
    width = dev.screen_width
    height = dev.screen_height
    padding = 20
    posX = random.randint(padding, width - padding)
    posY = random.randint(padding, height - padding)
    apple = None
    if chosenItem == 0: apple = apples.Red_Apple(posX,posY)
    elif chosenItem == 1: apple = apples.Golden_Apple(posX,posY)
    elif chosenItem == 2: 
        apple = apples.Poison_Apple(posX,posY)
        despawn_tick_check = tick_counter + 50
    elif chosenItem == 3: 
        apple = apples.Eaten_Apple(posX,posY)
        despawn_tick_check = tick_counter + 50
    elif chosenItem == 4: apple = apples.Speed_Apple(posX,posY)
    elif chosenItem == 5: apple = apples.Timed_Apple(posX,posY)
    elif chosenItem == 6: apple = apples.Strength_Apple(posX,posY)
    apple.spawn()
    
def despawn_apple():
    global apple
    apple = None
    dev.clear_screen('#000')


def button_handler(event, resume):
    global ping_timer, pong_timer, tick_counter, despawn_tick_check, playerOne, obstacles, gameActive,me
    if not playerOne.isAlive: me = None
    if me is None: 
        gameover()
        return
        # not yet playing or no longer playing
    
    playerOne.move_player(dev, gameover, apple, spawn_item,obstacles)
    if despawn_tick_check > 0:
        if tick_counter == despawn_tick_check:
            despawn_apple()
            spawn_item()
    if tick_counter == 50:
        spawn_item()  
    if tick_counter % 200 == 0:
        width = dev.screen_width
        height = dev.screen_height
        padding = 20
        posX = random.randint(padding, width - padding)
        posY = random.randint(padding, height - padding)
        spawn_obstacle(posX,posY)
    draw_obstacles()
    
    if event == 'cancel':
        quit()
    elif event == 'tick':
        tick_counter += 1
        ui.center(dev.screen_width//2, dev.font_height*1, str(tick_counter+playerOne.score), '#FFF', bg)
        if networked:
            pong_timer -= 1
            if pong_timer < 0:
                leave()
                return
            ping_timer -= 1
            if ping_timer < 0:
                ping_timer = int(2 / ui.time_delta)  # send ping every 2 secs
                net.send(mate.id, [msg_type, 'ping'])
        dev.after(ui.time_delta, resume) # need to wait...
    else:
        if event == 'left_down':
            playerOne.moveY = 0
            if playerOne.moveX  == -1: playerOne.moveX = 1
            else: playerOne.moveX = -1
        elif event == 'right_down':
            playerOne.moveX = 0
            if playerOne.moveY == -1: playerOne.moveY = 1
            else: playerOne.moveY = -1
            
        resume()


#nothing to do past here
def gameover():
    global playerOne,tick_counter, gameActive, bestScore
    if bestScore <= tick_counter+playerOne.score:
        bestScore = tick_counter + playerOne.score

    gameActive = False
    dev.clear_screen('#000')
    x = dev.screen_width // 2
    ui.center(x, dev.font_height*4, 'GAME', '#FFF', bg)
    ui.center(x, dev.font_height*6, 'OVER', '#FFF', bg)
    ui.center(x, dev.font_height*8, 'Best', '#FFF', bg)
    ui.center(x, dev.font_height*10, str(bestScore), '#FFF', bg)
    ui.center(x, dev.font_height*12, 'SCORE:', '#FFF', bg)
    ui.center(x, dev.font_height*13, str(tick_counter), '#FFF', bg)

    time.sleep(5)
    snake_non_networked()
        
def start_game_soon(player):
    x = dev.screen_width // 2
    ui.center(x, dev.font_height*6, 'Get', '#FFF', bg)
    ui.center(x, dev.font_height*8, '5', '#FFF', bg)
    ui.center(x, dev.font_height*10, 'Ready', '#FFF', bg)
    time.sleep(0.5)
    dev.clear_screen(bg)
    ui.center(x, dev.font_height*6, 'Get', '#F00', bg)
    ui.center(x, dev.font_height*8, '4', '#F00', bg)
    ui.center(x, dev.font_height*10, 'Ready', '#F00', bg)
    time.sleep(0.5)
    dev.clear_screen(bg)
    ui.center(x, dev.font_height*6, 'Get', '#FFF', bg)
    ui.center(x, dev.font_height*8, '3', '#FFF', bg)
    ui.center(x, dev.font_height*10, 'Ready', '#FFF', bg)
    time.sleep(0.5)
    dev.clear_screen(bg)
    ui.center(x, dev.font_height*6, 'Get', '#F00', bg)
    ui.center(x, dev.font_height*8, '2', '#F00', bg)
    ui.center(x, dev.font_height*10, 'Ready', '#F00', bg)
    time.sleep(0.5)
    dev.clear_screen(bg)
    ui.center(x, dev.font_height*6, 'Get', '#FFF', bg)
    ui.center(x, dev.font_height*8, '1', '#FFF', bg)
    ui.center(x, dev.font_height*10, 'Ready', '#FFF', bg)
    start_game(player)

def start_game(player):
    global me
    me = player
    reset_mate_timeout()
    ui.track_button_presses(button_handler)  # start tracking button presses
    dev.clear_screen(bg)

def snake_non_networked():
    init_game()
    start_game_soon(0)

# The following functions are used when playing the game over the network

def master():  # the master is the node with the smallest id
    return net.id < mate.id

def message_handler(peer, msg):
    global pong_timer
    if peer is None:
        if msg == 'found_mate':
            found_mate()
        else:
            print('system message', msg)  # ignore other messages from system
    elif type(msg) is list and msg[0] == msg_type:
        if me == None:
            random.seed(random_seed ^ msg[1])  # set same RNG on both nodes
            # determine if we are player 0 or 1
            start_game_soon(master() ^ random.randrange(2))
        elif msg[1] == 'quit':
            leave()
        elif msg[1] == 'ping':
            reset_mate_timeout()
        else:
            print('received', peer, msg)

def found_mate():
    global random_seed

    init_game()

    # exchange random seeds so both nodes have the same RNG
    random_seed = random.randrange(0x1000000)
    net.send(mate.id, [msg_type, random_seed])

def snake_networked():
    global msg_type
    msg_type = 'SNAKENET'
    mate.find(msg_type, message_handler)

def snake(n):
    global networked
    networked = n
    if networked:
        snake_networked()
    else:
        snake_non_networked()

def reset_mate_timeout():
    global pong_timer
    pong_timer = int(5 / ui.time_delta)  # reset peer timeout to 5 seconds

def quit():  # called to quit the game
    if networked:
        net.send(mate.id, [msg_type, 'quit'])
    leave()
    

def leave():
    global me
    me = None  # no longer playing
    if networked:
        net.pop_handler()  # remove message_handler
    apps.menu()  # go back to app menu
    
apps.register('SNAKE', lambda: snake(False), False)
apps.register('SNAKENET', lambda: snake(True), True)
    
