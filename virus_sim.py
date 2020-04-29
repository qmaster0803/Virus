import matplotlib.pyplot as plot
import random
import time
import math
import cv2
import os

#definition (default)
speedMin = 3
speedMax = 5
peopleCount = 300
fieldDimensions = 1000
radius = 5
ver = 100
letal = 50
sickPeriodMin = 14
sickPeriodMax = 50
birth = 0
limitOfDays = 0
isolation = False #NOT WORKING NOW!
#end defenition

#coordinates of every human
x = []
y = []
#speed of every human
xVar = []
yVar = []

#"True" or "False" for every human
infected = []
#total count of infected people
infectedCount = 1

#"True" or "False" for every human
imm = []
#total count of immunity
immCount = 0

#"True" or "False" for every human
dead = []
#total count of dead
deadCount = 0

#"True" or "False" for every human
sick = []
#On init, every human has different (random) sickness time
sickPeriod = []

#total days counter
iterator = 0

#for stats
peopleStats = []
infectedStats = []
immStats = []
deadStats = []
born = 0

#initializing random integer generator
random.seed()

#for exit from main loop
#you need to run loop again, for rendering last shot of video
nextBreak = False

#initializing plots
fig, plots = plot.subplots(2, figsize=(15, 15))

def defineAll():
    global speedMin, speedMax, peopleCount, fieldDimensions, radius, ver, letal, sickPeriodMin, sickPeriodMax, birth, limitOfDays, isolation
    print('Virus simulator by qmaster0803')
    print('Please enter simulation parameters (Enter - default):')
    try:
        speedMin = int(input('Minimum speed of human? '))
    except ValueError:
        print('Setting default: '+str(speedMin))
    try:
        speedMax = int(input('Maximum speed of human? '))
    except ValueError:
        print('Setting default: '+str(speedMax))
    try:
        peopleCount = int(input('Starting population? '))
    except ValueError:
        print('Setting default: '+str(peopleCount))
    try:
        fieldDimensions = int(input('Field dimensions? '))
    except ValueError:
        print('Setting default: '+str(fieldDimensions))
    try:
        radius = int(input('Infection radius? '))
    except ValueError:
        print('Setting default: '+str(radius))
    try:
        ver = int(input('Chance of infection? '))
    except ValueError:
        print('Setting default: '+str(ver))
    try:
        letal = int(input('Chance of death? '))
    except ValueError:
        print('Setting default: '+str(letal))
    try:
        sickPeriodMin = int(input('Minimum time of illness? '))
    except ValueError:
        print('Setting default: '+str(sickPeriodMin))
    try:
        sickPeriodMax = int(input('Maximum time of illness? '))
    except ValueError:
        print('Setting default: '+str(sickPeriodMax))
    try:
        birth = int(input('Birth rate? '))
    except ValueError:
        print('Setting default: '+str(birth))
    try:
        limitOfDays = int(input('Maximum duration of simulation (days)? '))
    except ValueError:
        print('Setting default: '+str(limitOfDays))
    try:
        isolation = False #NOT WORKING NOW!
    except ValueError:
        print('Setting default: '+str(isolation))

#initializing all variables for every human
def init():
    global x, y, xVar, yVar, infected, imm, died, sick, sickPeriod, peopleCount, born
    for i in range(peopleCount):
        x.append(random.randint(0, fieldDimensions))
        y.append(random.randint(0, fieldDimensions))
        if(random.randint(0, 1) == 0): xVar.append(-random.randint(speedMin, speedMax))
        else: xVar.append(random.randint(speedMin, speedMax))
        if(random.randint(0, 1) == 0): yVar.append(-random.randint(speedMin, speedMax))
        else: yVar.append(random.randint(speedMin, speedMax))
        infected.append(False)
        imm.append(False)
        dead.append(False)
        sick.append(0)
        sickPeriod.append(random.randint(sickPeriodMin, sickPeriodMax))
    #patient zero
    infected[0] = True

def showBottomPlot():
    global plots
    plots[1].plot(range(1, iterator+1), infectedStats, label='Infected', color="#FF0000")
    plots[1].plot(range(1, iterator+1), deadStats, label="Dead", color="#000000")
    plots[1].plot(range(1, iterator+1), peopleStats, label="Population", color="#0000FF")
    plots[1].plot(range(1, iterator+1), immStats, label="Immunity", color="#00FF00")
    plots[1].legend()

def showStatsOnMainPlot():
    global plots
    plots[0].text(0, 0, 'Days: '+str(iterator), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/60)), 'Population: '+str(peopleCount-deadCount), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/120)), 'Infected: '+str(infectedCount), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/180)), 'Dead: '+str(deadCount), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/240)), 'Immunity: '+str(immCount), fontsize=14, color='#FF0000')
    if(birth != 0): plots[0].text(0, int(fieldDimensions/(1000/300)), 'Born: '+str(born), fontsize=14, color='#FF0000')

def checkRebound(x1, x2, y1, y2, i):
    global x, y, xVar, yVar
    if(x[i] + xVar[i] <= 0 or x[i] + xVar[i] >= fieldDimensions): xVar[i] = -1*int(xVar[i]/abs(xVar[i]))*random.randint(speedMin, speedMax)
    if(y[i] + yVar[i] <= 0 or y[i] + yVar[i] >= fieldDimensions): yVar[i] = -1*int(yVar[i]/abs(yVar[i]))*random.randint(speedMin, speedMax)

def immOrDie(i):
    global imm, infected, infectedCount, immCount, deadCount, dead
    if(random.randint(0, 100) > letal):
        imm[i] = True
        infected[i] = False
        infectedCount -= 1
        immCount += 1
    else:
        deadCount += 1
        dead[i] = True
        infected[i] = False
        infectedCount -= 1

def checkInfection(i):
    global infected, infectedCount, sick
    for i2 in range(peopleCount):
        if(not infected[i2] and not imm[i2] and i != i2 and not dead[i2]):
            if(math.sqrt(abs(x[i] - x[i2])+abs(y[i] - y[i2])) < radius):
                if(random.randint(0, 100) <= ver):
                    infected[i2] = True
                    sick[i2] = iterator
                    infectedCount += 1

def createHuman():
    global x, y, xVar, yVar, infected, imm, died, sick, sickPeriod, peopleCount, born
    x.append(random.randint(0, fieldDimensions))
    y.append(random.randint(0, fieldDimensions))
    if(random.randint(0, 1) == 0): xVar.append(-random.randint(speedMin, speedMax))
    else: xVar.append(random.randint(speedMin, speedMax))
    if(random.randint(0, 1) == 0): yVar.append(-random.randint(speedMin, speedMax))
    else: yVar.append(random.randint(speedMin, speedMax))
    infected.append(False)
    imm.append(False)
    dead.append(False)
    sick.append(0)
    sickPeriod.append(random.randint(sickPeriodMin, sickPeriodMax))
    peopleCount += 1
    born += 1

def createVideo(iterator):
    out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 3.0, (1920, 1080))

    for i in range(1, iterator+1):
        print(("%.2f" % (i/iterator*100.0)) + '%')
        out.write(cv2.resize(cv2.imread(str(i)+'.png'), (1920, 1080)))
        os.remove(str(i)+'.png')
     
    out.release()
    cv2.destroyAllWindows()

def simulate():
    global plots, peopleCount, dead, infected, isolation, fieldDimensions, x, y, xVar, yVar, imm, iterator, sick, sickPeriod, birth, infectedStats, deadStats, peopleStats, immStats, nextBreak, limitOfDays
    while(True):
        #clear
        plots[0].cla()
        plots[1].cla()
        
        showStatsOnMainPlot()
        plots[0].set_xlim([0, fieldDimensions])
        plots[0].set_ylim([0, fieldDimensions])
        showBottomPlot()
        for i in range(peopleCount):
            if(not dead[i]):
                if(infected[i]):
                    checkInfection(i)
                if(isolation): pass #TODO
                else: checkRebound(0, fieldDimensions, 0, fieldDimensions, i)
                #do move
                x[i] = x[i] + xVar[i]
                y[i] = y[i] + yVar[i]
                #show people on main plot
                if(infected[i]): plots[0].scatter(x[i], y[i], 2, '#FF0000')
                elif(imm[i]): plots[0].scatter(x[i], y[i], 2, '#00FF00')
                else: plots[0].scatter(x[i], y[i], 2, '#0000FF')
            else:
                if(iterator - sick[i] < sickPeriod[i] + 7):
                    plots[0].scatter(x[i], y[i], 2, '#000000')
        for i in range(peopleCount):
            if(infected[i]):
                if(iterator - sick[i] == sickPeriod[i]):
                    immOrDie(i)
        if(birth > 0):
            if(iterator % birth == 0):
                createHuman()
        iterator += 1

        #for stats
        infectedStats.append(infectedCount)
        deadStats.append(deadCount)
        peopleStats.append(peopleCount-deadCount)
        immStats.append(immCount)

        #draw, wait and save plots
        plot.draw()
        plot.pause(0.1)
        plot.savefig(str(iterator)+'.png', dpi=200)

        #for exiting
        if(nextBreak or iterator == limitOfDays): break
        if(infectedCount == 0): nextBreak = True

    plot.close('all')
    createVideo(iterator)

if(__name__ == '__main__'):
    defineAll()
    init()
    simulate()
