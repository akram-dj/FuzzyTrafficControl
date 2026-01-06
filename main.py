import random
import time
import threading
import pygame
import sys
from TrafficSignal import TrafficSignal
from Vehicle import Vehicle
from Fuzzy_Controller import fuzzy_decision, get_next_green_signal
defaultGreen = {0:10, 1:10, 2:10, 3:10}
defaultRed = 15
defaultYellow = 5
signals = []
noOfSignals = 4
currentGreen = 0   # Indicates which signal is green currently
# nextGreen = (currentGreen+1)%noOfSignals    # Indicates which signal will turn green next
currentYellow = 0   # Indicates whether yellow signal is on or off 
speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'bike':2.5}  # average speeds of vehicles

# Coordinates of vehicles' start
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}    
y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]
vehicleCountCoods = [(530,190),(810,190),(810,530),(530,530)]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}

# Gap between vehicles
stoppingGap = 15    # stopping gap
movingGap = 15   # moving gap

# Flag to enable/disable fuzzy logic
USE_FUZZY_LOGIC = True

pygame.init()
simulation = pygame.sprite.Group()


def get_vehicle_count(direction):
    """Count total vehicles waiting in a direction (not crossed)"""
    count = 0
    for lane in [0, 1,2]:
        for vehicle in vehicles[direction][lane]:
            if vehicle.crossed == 0:
                count += 1
    return count


def get_all_vehicle_counts():
    """Get vehicle counts for all directions"""
    counts = {}
    for i in range(noOfSignals):
        direction = directionNumbers[i]
        counts[i] = get_vehicle_count(direction)
    return counts

def initialize():
    global signals
    signals = []
    for i in range(noOfSignals):
        ts = TrafficSignal(defaultRed, defaultYellow, defaultGreen[i])
        signals.append(ts)
    repeat()

def repeat():
    global currentGreen, currentYellow

    # ========================
    # 1) GREEN PHASE
    # ========================
    while signals[currentGreen].green > 0:
        updateValues()
        time.sleep(1)
    # ========================
    # 2) YELLOW PHASE
    # ========================
    currentYellow = 1

    # Reset stop positions for vehicles in current direction
    for i in range(0, 3):
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
            
    while signals[currentGreen].yellow > 0:
        updateValues()
        time.sleep(1)
    currentYellow = 0

    # ========================
    # 3) FUZZY DECISION
    # ========================
    vehicle_counts = get_all_vehicle_counts()

    # Ask fuzzy system for next direction and green time
    next_direction, next_green_time = get_next_green_signal(vehicle_counts)

    print(f"Fuzzy Decision -> Direction: {directionNumbers[next_direction]} | "
          f"Vehicles: {vehicle_counts[next_direction]} | Green: {next_green_time}s")

    # ========================
    # 4) RESET CURRENT SIGNAL
    # ========================
    signals[currentGreen].green = defaultGreen[currentGreen]
    signals[currentGreen].yellow = defaultYellow
    signals[currentGreen].red = defaultRed

    # ========================
    # 5) SWITCH TO FUZZY-CHOSEN SIGNAL
    # ========================
    currentGreen = next_direction

    # Set green time decided by fuzzy logic
    signals[currentGreen].green = next_green_time

    # ========================
    # 6) SET RED FOR ALL OTHERS
    # ========================
    for i in range(noOfSignals):
        if i != currentGreen:
            signals[i].red = signals[currentGreen].green + signals[currentGreen].yellow
            signals[i].yellow = defaultYellow

    # ========================
    # 7) REPEAT FOREVER
    # ========================
    repeat()

def updateValues():
    for i in range(0, noOfSignals):
        if i == currentGreen:
            if currentYellow == 0:
                if signals[i].green > 0:
                    signals[i].green -= 1
            else:
                if signals[i].yellow > 0:
                    signals[i].yellow -= 1
        else:
            if signals[i].red > 0:
                signals[i].red -= 1




# Generating vehicles in the simulation
def generateVehicles():
    while(True):
        vehicle_type = random.randint(0,3)
        lane_number = random.randint(1,2)
        temp = random.randint(0,99)
        direction_number = 0
        dist = [25,50,75,100]
        if(temp<dist[0]):
            direction_number = 0
        elif(temp<dist[1]):
            direction_number = 1
        elif(temp<dist[2]):
            direction_number = 2
        elif(temp<dist[3]):
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type],
                vehicles,speeds[vehicleTypes[vehicle_type]],
                [x[directionNumbers[direction_number]][lane_number],y[directionNumbers[direction_number]][lane_number]], 
                direction_number, 
                directionNumbers[direction_number],
                defaultStop[directionNumbers[direction_number]],simulation)
        time.sleep(1)


class Main:
    thread1 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread1.daemon = True
    thread1.start()

    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)

    # Screensize 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('images/intersection.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("TRAFFIC SIMULATION - FUZZY LOGIC CONTROL")

    # Loading signal images and font
    redSignal = pygame.image.load('images/signals/red.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    greenSignal = pygame.image.load('images/signals/green.png')
    font = pygame.font.Font(None, 30)
    countFont = pygame.font.Font(None, 25)

    thread2 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
    thread2.daemon = True
    thread2.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))   # display background in simulation
        
        # Display signals
        for i in range(0,noOfSignals):  # display signal and set timer according to current status: green, yellow, or red
            if(i==currentGreen):
                if(currentYellow==1):
                    signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if(signals[i].red<=20):
                    signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
        
        signalTexts = ["","","",""]

        # Display signal timer
        for i in range(0,noOfSignals):  
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods[i])
        
        # Display vehicle count for each direction
        for i in range(0, noOfSignals):
            direction = directionNumbers[i]
            count = get_vehicle_count(direction)
            countText = countFont.render(f"Vehicles: {count}", True, green, black)
            screen.blit(countText, vehicleCountCoods[i])

        # Display the vehicles
        for vehicle in simulation:  
            screen.blit(vehicle.image, [vehicle.x, vehicle.y])
            vehicle.move(stopLines,currentGreen,currentYellow,vehicles,movingGap)
        
        pygame.display.update()


Main()
