### 1664326 Raúl Josafat Correa Ascencio
### Selected topics of Optimization V4-V6
### Reads normal problems: Usando Alfa
import sys
import re
import math
import time
import operator
import random

Time = 0
RTime = 0
TProfit = 0
TPlaces = []
comienzo = 0

# improving Heuristic
improvingSolution = []
Radius = 0
improvIter = 0
# if len(sys.argv) < 3:
improvTimeL = 5
ImprovIterL = 2500
# elif len(sys.argv) < 4:
#     improvTimeL = int(sys.argv[2])
#     ImprovIterL = 50
# else:
#     improvTimeL = int(sys.argv[2])
#     ImprovIterL = int(sys.argv[3])
PossibleSol = []
bestImproving = 0
mejorGanancia = 0
HeuristicTime = 0

#random heuristic
k = 4

#Alfa
a = 0.5

#documentacion
written = ''

def leer_txt(lineas):
    global RTime
    global Time
    global TPlaces
    global written
    index = -1
    Places = []
    for linea in lineas:
        if index == -1:
            Time = int(linea[0])
            RTime = int(linea[0])
            Paths = int(linea[1])
            index += 1
            written += 'Time: '+ str(Time) +'\tPaths: '+ str(Paths) +'\n'
        else:
            Place = []
            Place.append(float(linea[0]))   # [0] X Coordinate
            Place.append(float(linea[1]))   # [1] Y Coordinate
            Place.append(int(linea[2]))     # [2] Profit
            Place.append(index)             # [3] Índice
            Place.append(True)              # [4] Visitable
            Places.append(Place)
            TPlaces.append(index)           # Lista de índices de lugares
            index += 1
    return(Places)

def Euclidean(PI,PF):
    distance = math.sqrt( (PI[0] - PF[0])**2 + (PI[1] - PF[1])**2 )
    return(distance)

def CandidateList(PInicial,Puntos, TimeLink):
    global RTime
    global a
    Ratios = []
    RestrictedList = []
    minRatio = 100000
    minIndex = 0
    maxRatio = 0
    maxIndex = 0
    ratiosIndex = 0
    for PFinal in Puntos:
        if PFinal[4]:
            Cost = Euclidean(PInicial,PFinal)
            if Cost <= (RTime + TimeLink) and Cost > 0: # Intento de limitar la lista
                Razon = PFinal[2] / Cost
                Ratio = []
                Ratio.append(PFinal[2]) # Profit
                Ratio.append(Cost)      # Cost
                Ratio.append(Razon)     # Ratio
                Ratio.append(PFinal[3]) # Index

                Ratios.append(Ratio)
                if Ratio[2] > maxRatio:
                    maxRatio = Ratio[2]
                    maxIndex = ratiosIndex
                if Ratio[2] < minRatio:
                    minRatio = Ratio[2]
                    minIndex = ratiosIndex
                ratiosIndex += 1

    RCL = (1 - a) * maxRatio + a * minRatio
    for candidate in Ratios:
        if candidate[2] >= RCL:
            RestrictedList.append(candidate)

    for candidate in Ratios:
        if candidate[2] >= RCL:
            RestrictedList.append(candidate)
    if len(RestrictedList) > 1:
        RestrictedList.sort(key=lambda R: R[2], reverse=True)
        return(RestrictedList)
    else:
        Ratios.sort(key=lambda R: R[2], reverse=True)
        return(Ratios)

def randomizeRatio(ratio):
    global k
    lenR = len(ratio)
    Random = []
    if len(ratio) > k-1:
        for x in range(0,k):
            Random.append(x)
        for n in range(0,lenR):
            if n == k-1:
                random.shuffle(Random)
            elif n > k-1:
                Random.append(n)
    else:
        for n in range(0,lenR):
            Random.append(n)
        random.shuffle(Random)
    return Random

def decide(Place1, Place2, Places, TimeLink):
    global RTime
    # global TProfit
    decision = []
    Ratio1 = []
    Ratio2 = []
    Ratio1 = CandidateList(Place1,Places, TimeLink)
    Ratio2 = CandidateList(Place2,Places, TimeLink)
    Random1 = randomizeRatio(Ratio1)
    Random2 = randomizeRatio(Ratio2)
    best1 = 0
    for r1 in Ratio1:
        bestIndex1 = Ratio1[Random1[best1]][3]
        P1New = Places[bestIndex1]
        Time1 = Ratio1[Random1[best1]][1]
        best2 = 0
        for r2 in Ratio2:
            bestIndex2 = Ratio2[Random2[best2]][3]
            P2New = Places[bestIndex2]
            Time2 = Ratio2[Random2[best2]][1]
            if P2New != P1New:
                Time3 = Euclidean(P1New,P2New)
                TTime = Time1 + Time2 + Time3
                if TTime <= RTime:
                    decision.append(P1New) # New Point 1
                    decision.append(P2New) # New Point 2
                    decision.append(Time3) # Cost from New Point 1 to New Point 2
                    decision.append('both')
                    P1New[4] = False
                    P2New[4] = False
                    RTime -= TTime
                    # print(f'{Time1}, {Time2}, {Time3}')
                    return(decision)
                else:
                    Time3 = Euclidean(P1New,Place2)
                    TTime = Time1 + Time3
                    if TTime <= RTime:
                        decision.append(P1New) # New Point 1
                        decision.append(P1New) # New Point 1
                        decision.append(Time3) # Cost from New Point 1 to Point 2
                        decision.append('left')
                        P1New[4] = False
                        RTime -= TTime
                        # print(f'{Time1}, Sans Time2, {Time3}')
                        return(decision)
                    else:
                        Time3 = Euclidean(Place1,P2New)
                        TTime = Time2 + Time3
                        if TTime <= RTime:
                            decision.append(P2New) # New Point 2
                            decision.append(P2New) # New Point 2
                            decision.append(Time3) # Cost from Point 1 to New Point 2
                            decision.append('right')
                            P2New[4] = False
                            RTime -= TTime
                            # print(f'Sans Time1, {Time2}, {Time3}')
                            return(decision)
            best2 += 1
        best1 += 1
    decision.extend((-1, -1, -1))
    return(decision)

def profitCheck(placesSolution, placesArray):
    Profit = 0
    for place in placesSolution:
        Profit += placesArray[place][2]
    return Profit

def SecondCheck(AnsEndroits,Endroits):
    longueur = len(AnsEndroits)
    prix = 0
    for i in range(0, longueur-1):
        E1 = AnsEndroits[i]
        E2 = AnsEndroits[i + 1]
        prix += Euclidean(Endroits[E1],Endroits[E2])
    return prix

def placesFromIndexList(indeces, places):
    solList = []
    for place in places:
        if place[3] in indeces:
            solList.append(place)
    return(solList)

def spacing(Sol, allPlaces, bestProfit, AvrgDist):
    global Time
    global TPlaces
    global Radius
    global improvingSolution
    # global PossibleSol
    global HeuristicTime
    global comienzo
    NewSol = []
    if time.time() - comienzo <= (improvTimeL - HeuristicTime)/1.5 :
        for S in Sol:
            NewSol.append(S)
        NewProfit = 0
        NewPlaces = [P for P in TPlaces if P not in Sol]
        # print(f'blablabla{NewPlaces}')
        listNewPlaces = []
        listNewPlaces = placesFromIndexList( NewPlaces, allPlaces)
        i = 0
        maxi = len(Sol) - 1
        for Place in Sol:
            if i == 0 or i == maxi:
                i+=1
            else:
                RestrictedPlaces = []
                RestrictedPlaces = CandidateList(allPlaces[Place],listNewPlaces, AvrgDist) # Nuevo!!
                for NewPlace in RestrictedPlaces:
                    if time.time() - comienzo <= (improvTimeL - HeuristicTime)/1.5 : # Nuevo!!
                        if Euclidean(allPlaces[Place],allPlaces[NewPlace[3]]) <= Radius:
                            TempPlace = NewSol[i]
                            NewSol[i] = NewPlace[3]
                            NewCost = round(SecondCheck(NewSol,allPlaces),4)
                            if NewCost <= Time:
                                NewProfit = profitCheck(NewSol,allPlaces)

                                # si el Profit es mejor     y la solución no está repetida                   y no se repite el lugar en la solución
                                if NewProfit > bestProfit and NewSol.count(NewPlace) < 2:  # and [NewSol,NewCost,NewProfit] not in PossibleSol
                                    # print(f'Spacing: {NewSol}, Cost {NewCost} , Profit {NewProfit}') ### temporal
                                    improvingSolution = NewSol # "return"
                                    PossibleSol.append([improvingSolution,NewCost,NewProfit])
                                    return
                                    # spacing(NewSol,allPlaces,NewProfit, AvrgDist)
                                else:
                                    NewSol[i] = TempPlace
                            else:
                                NewSol[i] = TempPlace
                    else:
                        return
                i+=1
    else:
        return

def inserting(Solucion, lugares, AvrgDist):
    global Time
    global TPlaces
    global Radius
    global improvIter
    global ImprovIterL
    global bestImproving
    global mejorGanancia
    global comienzo
    NuevosSitios = [L for L in TPlaces if L not in Solucion]
    listaNuevosSitios = []
    listaNuevosSitios = placesFromIndexList(NuevosSitios, lugares)
    i = 1
    if time.time() - comienzo <= improvTimeL:
        for Lugar in Solucion:
            LugaresFiltrados = []
            LugaresFiltrados = CandidateList(lugares[Lugar],listaNuevosSitios, AvrgDist*4)
            for NuevoLugar in LugaresFiltrados:
                continuar = improvIter <= ImprovIterL and time.time() - comienzo <= improvTimeL
                if Euclidean(lugares[Lugar],lugares[NuevoLugar[3]]) <= Radius and continuar:
                    Solucion.insert(i,NuevoLugar[3])
                    # print(f'Sol: {Solucion}\tNL: {NuevoLugar},{i}')
                    NewCost = round(SecondCheck(Solucion,lugares),4)
                    if NewCost <= Time:
                        NProfit = profitCheck(Solucion,lugares)
                        # si la ganancia es mejor     y el lugar no se repite en la solución
                        if NProfit >= mejorGanancia and Solucion.count(NuevoLugar[3]) < 2: # Nuevo!!
                            LugaresFiltrados.remove(NuevoLugar)
                            bestImproving = Solucion
                            mejorGanancia = NProfit
                        else:
                            Solucion.remove(NuevoLugar[3]) # Nuevo!!
                    else:
                        Solucion.remove(NuevoLugar[3])
                    improvIter += 1
            i += 1
    else:
        return

# def inserting(Solucion, lugares):
#     global Time
#     global TPlaces
#     global Radius
#     global improvIter
#     global ImprovIterL
#     global improvingSolution
#     global bestImproving
#     global mejorGanancia
#     NuevosLugares = [L for L in TPlaces if L not in Solucion]
#     i = 1
#     for Lugar in Solucion:
#         for NuevoLugar in NuevosLugares:
#             continuar = improvIter <= ImprovIterL and time.time() - comienzo <= improvTimeL
#             if Euclidean(lugares[Lugar],lugares[NuevoLugar]) <= Radius and continuar:
#                 Solucion.insert(i,NuevoLugar)
#                 # print(f'Sol: {Solucion}\tNL: {NuevoLugar},{i}')
#                 NewCost = round(SecondCheck(Solucion,lugares),5)
#                 if NewCost <= Time:
#                     NProfit = profitCheck(Solucion,lugares)
#                         # si la ganancia es mejor     y el lugar no se repite en la solución
#                     if NProfit >= mejorGanancia and len(Solucion) == len(set(Solucion)):
#                         NuevosLugares.remove(NuevoLugar)
#                         improvIter += 1
#                         bestImproving = Solucion
#                         mejorGanancia = NProfit
#                     else:
#                         Solucion.remove(NuevoLugar)
#                 else:
#                     Solucion.remove(NuevoLugar)
#             else:
#                 return
#         i += 1

def solution(lugares):
    global Time
    global RTime
    global TProfit
    global improvingSolution
    global Radius
    global bestImproving
    global mejorGanancia
    global HeuristicTime
    global comienzo
    global written
    global a

    solucionAleatoria = []

    P1 = lugares[0]
    P1[4] = False
    P2 = lugares[1]
    P2[4] = False
    AnsLugaresL = []
    AnsLugaresR = []
    AnsLugaresL.append(P1[3]) # Lugar de inicio
    AnsLugaresR.append(P2[3]) # Lugar de fin
    TimeLink = 0
    seguir = 1
    Validador = 0
    while seguir == 1:
        RTime += TimeLink
        NuevosLugares = decide(P1, P2, lugares, TimeLink)
        Validador = NuevosLugares[2]
        if Validador < 0:
            RTime -= TimeLink
            seguir = 0
        else:
            TimeLink = NuevosLugares[2]
            if NuevosLugares[3] == 'left':
                P1 = NuevosLugares[0]
                AnsLugaresL.append(P1[3]) # Lado inicial
            elif NuevosLugares[3] == 'right':
                P2 = NuevosLugares[1]
                AnsLugaresR.insert(0, P2[3]) # Lado final
            else:
                P1 = NuevosLugares[0]
                P2 = NuevosLugares[1]
                AnsLugaresL.append(P1[3]) # Lado inicial
                AnsLugaresR.insert(0, P2[3]) # Lado final
    AnsLugares = AnsLugaresL + AnsLugaresR
    Cost1 = round(SecondCheck(AnsLugares,lugares),4)
    Cost = round(Time - RTime,4)
    written += 'The selected path is '+ str(AnsLugares) +' with an alfa of ' + str(a) + '\n'
    TProfit = profitCheck(AnsLugares,lugares)

    if Time > 90:    # Potencialmente no. aleatorio
        const = 2
    else:
        const = 3
    AvrgDist = Cost / len(AnsLugares)
    Radius = const * AvrgDist
    written += 'The profit of this path will be ' + str(TProfit)+'.\n'
    written += 'The time taken for traveling through this path is '+ str(Cost) +'.\n'
    HeuristicTime = round((time.time() - comienzo),2)
    written += 'Heuristic execution time: '+ str(HeuristicTime) +'s\n'
    feasible = (Cost > Cost1 - 0.1 and Cost < Cost1 + 0.1) and len(AnsLugares) == len(set(AnsLugares)) and AnsLugares[0] == 0 and AnsLugares[-1] == 1
    written += 'Feasible solution: ' + str(feasible) + '\n'

    PossibleSol.append([AnsLugares, Cost, TProfit])
    improvingSolution = AnsLugares
    spacing(AnsLugares, lugares, TProfit, AvrgDist) # mejora improvingSolution
    # sOrderCost = sorted(PossibleSol, key = operator.itemgetter(1))
    # sOrderProfit = sorted(sOrderCost, key = operator.itemgetter(2), reverse=True)
    mejorGanancia = profitCheck(improvingSolution, lugares)
    bestImproving = improvingSolution
    inserting(improvingSolution, lugares, AvrgDist) # cambia bestImproving
    impCost = round(SecondCheck(bestImproving,lugares),4)
    written += 'The improved Solution is '+ str(bestImproving) + '\n'
    written += 'The improved Profit is ' + str(mejorGanancia) +'\n'
    written += 'The time taken for traveling through this new path is ' + str(impCost) + '\n'
    TotalTime = round((time.time() - comienzo),2)
    written += 'Total execution time: ' + str(TotalTime) +'s\n'
    if mejorGanancia > 0:
        improvementPercent = round(100*(mejorGanancia - TProfit)/mejorGanancia , 2)
    else:
        improvementPercent = 0
    written += 'The improvement percentage is ' + str(improvementPercent) + '%\n'
    feasibleI = impCost <= Time and len(bestImproving) == len(set(bestImproving)) and bestImproving[0] == 0 and bestImproving[-1] == 1
    written += 'Feasible solution: ' + str(feasibleI) +'\n'


    # instances = open('STSPv7.txt', 'a')
    # instances.write(written)
    # instances.write('\n')
    # instances.close()

    if feasibleI:
        solucionAleatoria = [mejorGanancia, impCost, bestImproving, a]
    else:
        solucionAleatoria = [0, 0, 0, 1]
    return solucionAleatoria
    #imprimir en script
    # print(f'{TProfit}:{Cost}:{HeuristicTime}:{mejorGanancia}:{impCost}:{TotalTime}:{improvementPercent}')

# Main
def mainRand(argumento, alfa, key):
    global comienzo
    global a
    global written
    global k
    k = key
    a = alfa
    randSol = []
    comienzo = time.time()
    if len(sys.argv) < 2:
        sys.exit("Error... The name of the file to be read is missing.")
    # argumento = sys.argv[1]
    formato = []
    file = open(argumento, "r")
    contenido = file.readlines()
    for linea in contenido:
        removeNLine = linea.rstrip()
        removeTab = re.split(r'\t+',removeNLine)
        formato.append(removeTab)
    file.close()
    lieux = leer_txt(formato)
    randSol = solution(lieux)
    return randSol
