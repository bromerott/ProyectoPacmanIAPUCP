import util
import searchAgents
import csv


def enhancedPacmanFeatures(state, action):

     ###################################################################
    #                            FEATURES                               #
    #   STOP: 50 si la accion es STOP. 0 Si es otra cosa.               #
    #   NEAREST_GHOST: MD al fantasma mas Cercano                       #
    #   NEAREST_CAPSULE: MD a la capsula mas cercana                    #
    #   FOOD: Lista de MDs a las 5 comidas mas cercanas                 #
    #   CAPSULE COUNT: # de Capsulas que existen                        #
    #   SCORE: Score actual                                             #
    #   ASUSTADITOS: # de Fantasmas asustados                           #
     ###################################################################

    features = util.Counter()
    # Feature de STOP
    features["STOP"] = int(action == "STOP") * 50

    # Generar arreglos y listas de los atributos del estado
    successor = state.generateSuccessor(0, action)
    pac_pos = successor.getPacmanPosition()
    ghosts = successor.getGhostPositions()

    # Fantasma Arriba
    features["win"] = successor.isWin()
    features["lose"] = int(successor.isLose())*100

    x,y = pac_pos
    if (x,y+2) in ghosts:
        features["UP"] = 100
    else:
        features["UP"] = 0

    if (x,y-2) in ghosts:
        features["DOWN"] = 100
    else:
        features["DOWN"] = 0

    if (x+2,y) in ghosts:
        features["RIGHT"] = 100
    else:
        features["RIGHT"] = 0

    if (x-2,y) in ghosts:
        features["LEFT"] = 100
    else:
        features["LEFT"] = 0


    if (x+1,y+1) in ghosts:
        features["NW"] = 100
    else:
        features["NW"] = 0

    if (x-1,y-1) in ghosts:
        features["NE"] = 100
    else:
        features["NE"] = 0

    if (x+1,y-1) in ghosts:
        features["SW"] = 100
    else:
        features["SW"] = 0

    if (x-1,y+1) in ghosts:
        features["SE"] = 100
    else:
        features["SE"] = 0



    capsules = successor.getCapsules()
    state_food = state.getFood()
    food = [(x, y)
            for x, row in enumerate(state_food)
            for y, food in enumerate(row)
            if food]
    nearest_ghosts = sorted([util.manhattanDistance(pac_pos, i) for i in ghosts])

    # Feature de Fantasmita Mas Cercano
    features["nearest_ghost"] = nearest_ghosts[0]*3

    # Feature de Pildora mas cercana
    nearest_caps = sorted([util.manhattanDistance(pac_pos, i) for i in capsules])
    if nearest_caps:
        features["nearest_capsule"] = nearest_caps[0]
    else:
        features["nearest_capsule"] = 0

    # Feature de MD a las 5 comidas mas cercanas
    nearest_food = sorted([(util.manhattanDistance(pac_pos, i),i) for i in food])
    nearest_food = nearest_food[:5]
    for i in xrange(min(len(nearest_food), 5)):
        nearest_food[i]=searchAgents.mazeDistance(pac_pos,nearest_food[i][1],state)

    for i, weight in zip(xrange(min(len(nearest_food), 5)), [1.5,1.4,1.3,1.2,1.1]):
        features[("food", i)] = weight * nearest_food[i]

    # Feature de cantidad de capsulas
    features["capsule count"] = len(capsules) * 10

    # Feature de Score
    features["score"] = state.getScore()

    # Feature de cantidad de Fantasmitas Asustaditos
    ghostStates = state.getGhostStates()
    numOfScaredGhosts = 0
    for ghostState in ghostStates:
        if ghostState.scaredTimer > 0:
            numOfScaredGhosts += 1
    features["asustaditos"]=numOfScaredGhosts

    return features