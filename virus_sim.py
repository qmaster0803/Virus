import matplotlib.pyplot as plot
import random
import time
import math
import cv2
import os

#definition
speedMin = 3
speedMax = 5
peopleCount = 10
fieldDimensions = 100
radius = 5
ver = 100
letal = 50
sickPeriodMin = 14
sickPeriodMax = 50
birth = 0
#end defenition

x = []
y = []
xVar = []
yVar = []
infected = []
infectedCount = 1
random.seed()
iterator = 0
deadStats = []
deadCount = 0
infectedStats = []
peopleStats = []
imm = []
immCount = 0
dead = []
sick = []
sickPeriod = []
immStats = []
born = 0
nextBreak = False
fig, plots = plot.subplots(2, figsize=(15, 15))


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

infected[0] = True

while(True):
    plots[0].text(0, 0, 'Days: '+str(iterator), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/60)), 'Population: '+str(peopleCount-deadCount), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/120)), 'Infected: '+str(infectedCount), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/180)), 'Dead: '+str(deadCount), fontsize=14, color='#FF0000')
    plots[0].text(0, int(fieldDimensions/(1000/240)), 'Immunity: '+str(immCount), fontsize=14, color='#FF0000')
    if(birth != 0): plots[0].text(0, int(fieldDimensions/(1000/300)), 'Born: '+str(born), fontsize=14, color='#FF0000')
    plots[0].set_xlim([0, fieldDimensions])
    plots[0].set_ylim([0, fieldDimensions])
    plots[1].plot(range(1, iterator+1), infectedStats, label='Infected', color="#FF0000")
    plots[1].plot(range(1, iterator+1), deadStats, label="Dead", color="#000000")
    plots[1].plot(range(1, iterator+1), peopleStats, label="Population", color="#0000FF")
    plots[1].plot(range(1, iterator+1), immStats, label="Immunity", color="#00FF00")
    plots[1].legend()
    for i in range(peopleCount):
        if(not dead[i]):
            if(infected[i]):
                for i2 in range(peopleCount):
                    if(not infected[i2] and not imm[i2] and i != i2 and not dead[i2]):
                        if(math.sqrt(abs(x[i] - x[i2])+abs(y[i] - y[i2])) < radius):
                            if(random.randint(0, 100) <= ver):
                                infected[i2] = True
                                sick[i2] = iterator
                                infectedCount += 1
            if(x[i] + xVar[i] <= 0 or x[i] + xVar[i] >= fieldDimensions): xVar[i] = -1*int(xVar[i]/abs(xVar[i]))*random.randint(speedMin, speedMax)
            if(y[i] + yVar[i] <= 0 or y[i] + yVar[i] >= fieldDimensions): yVar[i] = -1*int(yVar[i]/abs(yVar[i]))*random.randint(speedMin, speedMax)
            x[i] = x[i] + xVar[i]
            y[i] = y[i] + yVar[i]
            if(infected[i]): plots[0].scatter(x[i], y[i], 2, '#FF0000')
            elif(imm[i]): plots[0].scatter(x[i], y[i], 2, '#00FF00')
            else: plots[0].scatter(x[i], y[i], 2, '#0000FF')
        else:
            if(iterator - sick[i] < sickPeriod[i] + 7):
                plots[0].scatter(x[i], y[i], 2, '#000000')
    for i in range(peopleCount):
        if(infected[i]):
            if(iterator - sick[i] == sickPeriod[i]):
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
    if(birth > 0):
        if(iterator % birth == 0):
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
    iterator += 1
    infectedStats.append(infectedCount)
    deadStats.append(deadCount)
    peopleStats.append(peopleCount-deadCount)
    immStats.append(immCount)
    plot.draw()
    plot.pause(0.1)
    plot.savefig(str(iterator)+'.png', dpi=200)
    plots[0].cla()
    plots[1].cla()
    if(nextBreak): break
    if(infectedCount == 0): nextBreak = True

    
out = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 3.0, (1920, 1080))

for i in range(1, iterator+1):
    print(("%.2f" % (i/iterator*100.0)) + '%')
    out.write(cv2.resize(cv2.imread(str(i)+'.png'), (1920, 1080)))
    os.remove(str(i)+'.png')
 
out.release()
cv2.destroyAllWindows()
