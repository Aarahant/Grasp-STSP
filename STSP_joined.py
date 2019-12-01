from STSPpart1 import main
from STSPpart2 import mainRand
import sys
import time
import random
comienzo = time.time()
problema = sys.argv[1]
if len(sys.argv) < 3:
    k = 3
else:
    k = int(sys.argv[2])
# written2 = ''
alfaList = [[0],[0.1],[.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9],[1]]
lenght = len(alfaList)
probability = 1/lenght
for alpha in alfaList:
    alpha.append(probability)
    probability += 1/lenght
# print(f'{alfaList}\n')

Original = []
# print(f'----------original-------')
Original = main(problema, 1) # [Profit_original, Distance_original, ans_original, time_og, Profit_Improving, Distance_Improving, ans_Improving, time_impr, improvementPercent]

# print(f'\n----------random---------')
Random = [Original[4],Original[5],Original[6], 1]
b = -1
Iter = 1000
run = 0

def alphaSelect(probability, alfas):
    if probability < alfas[0][1]:
        index = 0
    elif probability < alfas[1][1]:
        index = 1
    elif probability < alfas[2][1]:
        index = 2
    elif probability < alfas[3][1]:
        index = 3
    elif probability < alfas[4][1]:
        index = 4
    elif probability < alfas[5][1]:
        index = 5
    elif probability < alfas[6][1]:
        index = 6
    elif probability < alfas[7][1]:
        index = 7
    elif probability < alfas[8][1]:
        index = 8
    elif probability < alfas[9][1]:
        index = 9
    else:
        index = 10
    return index

Zs = [[],[],[],[],[],[],[],[],[],[],[]]
for iteracion in range(0,Iter):
    aleatorio = random.uniform(0,1)
    alfaIndex = alphaSelect(aleatorio, alfaList)
    alfa = alfaList[alfaIndex][0]

    ###TEMP
    # written1 = str(iteracion) + '\n'
    # instances.write(written1)
    # instances.close()

    NuevoRandom = mainRand(problema, alfa, k) # [Profit_Random, Distance_Random, path]
    Zs[alfaIndex].append(NuevoRandom[0])
    if NuevoRandom[0] > Random[0]:
        Random = NuevoRandom
        b = iteracion
    run += 1

    # Reactive Grasp (Avrg vs Best?) Restarle el mínimo proly sea buena idea
    if run%100 == 0:
        # Get the average Z per alpha
        avrgZ = []
        for Zi in Zs:
            countZ = len(Zi)
            totZ = 0
            for Z in Zi:
                totZ += Z
            avrgZ.append(totZ/countZ)
        sumZ = 0
        # print(f'{avrgZ} is the average list of {Zs}')

        #Get the total Z
        for x in avrgZ:
            sumZ += x

        #assign new probability
        newProb = 0
        ndx = 0
        for x in avrgZ:
            newProb += (x/Random[0]) / (sumZ/Random[0])
            alfaList[ndx][1] = newProb
            ndx += 1
        # print(f'alfa List = {alfaList}\n')






        # Time = round((time.time() - comienzo),3)
    # if time.time() - comienzo > maxTime:
    #     break

#         print(f'\n---Original: {Original}.')
#         print(f'---New best: {Random}.')
#         print(f'---found after {Time}s')
#         print(f'---at iteratin number {b}\n')
#     print(f'\n')
# written2 += '\n----------solution--------\n'
# written2 += 'Original: '+ str(Original) +'\n'
# written2 += 'Random: ' + str(Random) + '...Found at iteration number ' + str(b) + '\n'
TotalTime = round((time.time() - comienzo),3)
# written2 += 'Total time: ' + str(TotalTime) + '\n'

# instances = open('STSPv7.txt', 'a')
# instances.write(written2)
# instances.write('\n')
# instances.close()

if Random[0] != 0:
    improvementPercent = round(100*(Random[0] - Original[4])/Random[0] , 2)
else:
    improvementPercent = 0
#         Profit_og, Distance_og,   Time_og,      lclSrchProfit, lclSrchDist,  lclSrch Time, lclSrch %,   Profit_Rand, Dist_Rand,  mejora              ,runtime    , alfa,     path
print(f'{Original[0]}:{Original[1]}:{Original[3]}:{Original[4]}:{Original[5]}:{Original[7]}:{Original[8]}:{Random[0]}:{Random[1]}:{TotalTime}:{improvementPercent}:{Random[3]}:{Random[2]}')
