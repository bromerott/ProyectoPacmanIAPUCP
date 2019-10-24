
import util
from perceptron import PerceptronClassifier
from pacman import GameState

PRINT = True

#Como funciona un PERPCEPTRON clasificador de clases multiples?
#Para clasificar:
#En esencia, lo que hacemos es calcular un score de un estado dada una accion.
#Por ejemplo, un feature podria ser (Hay un fantasma en la siguiente posicion de pacman, dada la accion?)
#Y a ese feature se le asigna un puntaje, como...-1!
#Despues de armar todos nuestros features, todos los puntajes se suman para calcular el score del estado dada la accion.
#Asi, se escoge la accion que tenga el mayor puntaje.

#Por ultimo, una herramienta se introduce a los scores: los pesos.
#Asi como las notas, un vector de pesos nos ayuda a implementar cuanto creemos que importa un feature.
#Por ejemplo, asumamos el anterior feature, y otro mas que hace lo mismo, pero revisa la presencia de comida enves de fantasmas.
#El puntaje asignado a la presencia del features sera...3!

#Notamos que sin pesos, pacman valor mas la comida que los fantasmas, y eso podria hacer que se suicide.
#Para arreglar esto, agregamos un vector de caracteristicas que le de mas importancia a los fantasmas que a la comida (como [4,2])

#Para entrenar:
#El Perceptron, para entrenar, comienza con unos pesos calculados al azar, y los modifica cada vez que se equivoca.
#Por supuesto, el perceptron sabe que se equivoca porque tiene un dataset donde dados ciertos features, la accion correcta esta dada.
#(el proceso de entrenamiento esta explicado mas a fondo debajo)

class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, 25)
        self.weights = util.Counter()

    #Clasificar un vector de features "data" en una clase "[guesses]"
    def classify(self, data ):
        guesses = []
        #Separar features de movimientos legales
        for datum, legalMoves in data:
            #En vectors se guardara los scores de cada posible movimiento
            vectors = util.Counter()
            #Para cada movimiento, calcular el score a traves de un producto punto
            for l in legalMoves:
                vectors[l] = self.weights * datum[l]
            #Agregar a guesses solo la accion con el score mas alto
            guesses.append(vectors.argMax())

        #Retornar la clase en forma de lista. (Ej. [South])
        return guesses


    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        #self.features = trainingData[0][0]['Stop'].keys() # could be useful later

        #Entrenar cierta cantidad de veces (N fijo)
        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            #print "|",
            #Para cada data en la tabla de features
            for i in range(len(trainingData)):
                #Extraer un data en TrainingData -> datum
                datum = trainingData[i]
                #Clasificar datum -> guess
                guess = self.classify([datum])[0]
                #Extraer movimiento correcto (dado)
                correctLabel = trainingLabels[i]
                #Verificar que la clasificacion fue correcta
                if guess != correctLabel:
                    #Si fue errada, actualizar pesos
                    self.weights += datum[0][correctLabel]
                    self.weights -= datum[0][guess]


##Razonamiento detras de Actualizacion de Weights, el verdadero aprendizaje:
#Asumamos que la clasificacion correcta de nuestrom datum debio de ser SOUTH, pero adivinamos NORTH.
#Que significa esto?
#Que los pesos estan mal! Como modificarlos para que favorezcan mas SOUTH y menos NORTH?
#Es claro que el score de (datum dado SOUTH) debio de ser mas alto, y el de (datum dado NORTH) mas bajo.

#La modificacion perfecta es imposible de adivinar, pero pensemos:
#Podriamos tratar de aumentar algunos pesos, pero eso funcionaria si supieramos en cuales (datum dado SOUTH) es mas alto para subir esos,
#y tambien en cuales (datum dado NORTH) fue alto, para bajar esos.
#Pero no necesitamos saber en cuales.

#Al sumarle a cada peso el feature de (datum dado SOUTH), estamos aumentando los pesos en los cuales SOUTH fue alto!
#(recordar que al no haber normalizacion, mientras mas alto sea un feature, mas score genera.)

#De manera analoga, al disminuir cada peso el feature de (datum dado NORTH), estamos disminuyendo los pesos en los cuales NORTH fue alto!

#Ejemplo:
#2 features nada mas: 
#DIE: 2 si es que un fantasma se encuentra en la siguiente posicion a la que ira pacman, dada la accion. 0 sino.
#(recordar que cada feature se calcula con un estado y una accion)
#FOODUP: 1 si una comida se encuentra en la siguiente posicion de pacman, dada la accion. 0 sino.

#Vector de weights inicial: [1,5]

#Entonces, asumamos que extraemos en un momento dado los 2 features, y recibimos esto:
#Vector de Features dado NORTH: [2,1] (fantasma arriba de pacman, encima de una comida)
#Vector de Features dado SOUTH: [0,1] (una comida debajo de pacman)
#Score dado NORTH: 2 + 5 = 7
#Score dado SOUTH: 0  + 5 = 5
#Entonces, se escoge NORTH (score mas alto).

#Fue este el guess correcto? Por supuesto que no, pacman priorizo comer sobre sobrevivir!
#Entonces, debemos de actualizar los pesos!
#1. Favorecer SOUTH:
#Vector de weights 2: [1,5] + [0,1] = [1,6]
#2. Desfavorecer NORTH:
#Vector de weights 3: [1,6] - [2,1] = [-1,5] = Vector de weights actual

#Ahora, asumamos que nos encontramos en la misma situacion.
#Vector de weights actual: [-1,5]

#Score dado NORTH= 2*-1 + 5 = 3
#Score dado SOUTH= 0*-1 + 5 = 5

#Ahora se escoge SOUTH! El vector de pesos se ha dado cuenta que la presencia de un fastasma deberia de ser una razon en contra
#de escoger la accion, no a favor! De esta manera, ahora cada vez que pacman se encuentre en esta situacion, sabra que debe de ir a SOUTH.
