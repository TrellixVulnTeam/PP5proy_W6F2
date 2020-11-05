import random
import collections
import pickle

"""Diccionario con el valor de cada dado dependiendo de cuántas veces salió."""
dadoValor = {1:  # cara 1: 1 vez es 100 - 3 veces es 1000
    {
        0: 0,
        1: 100,
        2: 200,  # 2*100
        3: 1000,
        4: 400,  # 4*100
        5: 500,  # 5*100
        6: 2000  # 2*1000 (dos veces triple)
    },
    2: {  # cara 2: 3 veces es 200
        0: 0,
        1: 0,
        2: 0,
        3: 200,
        4: 0,
        5: 0,
        6: 400  # 2*200 (dos veces triple)
    },
    3: {  # cara 3: 3 veces es 300
        0: 0,
        1: 0,
        2: 0,
        3: 300,
        4: 0,
        5: 0,
        6: 600  # 2*300 (dos veces triple)
    },
    4: {  # cara 4: 4 veces es 400
        0: 0,
        1: 0,
        2: 0,
        3: 400,
        4: 0,
        5: 0,
        6: 800  # 2*400 (dos veces triple)
    },
    5: {  # cara 5: 1 vez es 50 - 3 veces es 500
        0: 0,
        1: 50,
        2: 100,  # 2*50
        3: 500,
        4: 200,  # 4*50
        5: 250,
        6: 1000  # 2*500 (dos veces triple)
    },
    6: {  # cara 6: 3 veces es 600
        0: 0,
        1: 0,
        2: 0,
        3: 600,
        4: 0,
        5: 0,
        6: 1200  # 2*600 (dos veces triple)
    }
}


class Juego:
    """clase del juego que tiene lista de jugadores, puntaje ganador, y los puntos acumulados en la ronda
       pasa los turnos"""
    def __init__(self):
        self.listaJugadores = []  # contiene los jugadores de la partida actual
        self.puntajeGanador = 10000  # puntaje al que se llega para ganar. 10k por default
        self.ranking = {}  # para el ranking del juego, se agregan tipo <Nombre>: <puntaje>
        self.puntosRonda = 0

    def elegir_jugadores(self, lista):
        """toma lista de jugadores tipo [[nombre1, tipo1], [nombre2, tipo2]] y los agrega a la lista de jugadores"""
        # 0 - Humano, 1 - Máquina (Fácil), 2 - Máquina (Normal), 3 - Máquina (Difícil)

        for jugador in lista:
            if jugador[1] == 0:  # jugador humano
                jugador = Jugador(jugador[0])
                self.listaJugadores.append(jugador)  # agrega a lista de jugadores
            elif jugador[1] == 1:  # jugador maquina facil
                jugador = MaquinaConservador(jugador[0])
                self.listaJugadores.append(jugador)
            elif jugador[1] == 2:  # maquina normal
                jugador = MaquinaNormal(jugador[0])
                self.listaJugadores.append(jugador)
            elif jugador[1] == 3:  # maquina agresiva
                jugador = MaquinaAgresivo(jugador[0])
                self.listaJugadores.append(jugador)

        self.listaJugadores = collections.deque(self.listaJugadores)  # lo casteo a deque para poder rotar
        self.jugadorActual = self.listaJugadores[0]  # define el jugador actual

    def elegir_puntaje(self, puntos):
        """cambia el puntaje al que hay que llegar para ganar"""
        self.puntajeGanador = puntos

    @staticmethod
    def primera_tirada():
        """tirada de 6 dados en donde instancio objetos Dado nuevos"""
        dados = []

        for _ in range(6):
            dado = Dado()
            dado.tirar_dado()
            dados.append(dado)

        return dados

    @staticmethod
    def turno_perdido(dados):
        """Verifica si la tirada sirve o se perdio el turno, devuelve True si se pierde el turno
           Turno sirve si hay 1, 5, numero triple o escalera"""

        if not Juego.is_escalera(dados):  # no es escalera (contiene 1 y 5)
            if 1 not in dados and 5 not in dados:  # no hay 1s ni 5s
                if not Juego.hay_triples(dados):  # no hay triples
                    return True

        return False  # si alguna de las anteriores no se cumplio

    @staticmethod
    def is_escalera(dados):
        """Verifica si la tirada es una escalera y devuelve True, caso contrario False"""
        escalera = [1, 2, 3, 4, 5, 6]  # caso en el que tiene un dado con cada valor
        return len(dados) == 6 and set(escalera).issubset(dados)

    @staticmethod
    def hay_triples(dados):
        """Verifica si hay numeros que salieron tres veces y devuelve True"""
        numeros = list(set(dados))  # toma los valores una sola vez
        cantidad = [dados.count(x) for x in numeros]  # lista con cantidad de veces que salieron los numeros
        return cantidad.count(3) > 0 or cantidad.count(6) > 0


    @staticmethod
    def tirar_dados(dados):
        for dado in dados:
            if not dado.guardado:
                dado.tirar_dado()

        return dados

    @staticmethod
    def calcular_puntos(eleccion):
        """toma la lista de dados elegidos y calcula el puntaje que darian"""
        numeros = list(set(eleccion))  # toma los valores de las caras una sola vez ej eleccion = [6,6,6] numeros = [6]
        cantidad = [[x, eleccion.count(x)] for x in numeros]  # devuelve lista de sublistas, cuantas veces esta c/u

        if Juego.is_escalera(eleccion):  # verifica si es escalera
            return 2500  # escalera vale 2500 puntos

        else:
            puntos = 0
            for sublista in cantidad:  # recorre sublistas de num de cara y cuantas veces esta ej [1, 3]
                dado = sublista[0]  # toma el valor de la cara del dado
                cant = sublista[1]  # toma cuantas veces salio ese valor
                # busca el puntaje en dicc y agrega a puntaje del turno
                puntos += dadoValor[dado][cant]

            return puntos

    def agregar_puntos(self):
        """Agrega al jugador los puntos acumulados en la ronda"""
        self.jugadorActual.puntosTotal += self.puntosRonda

    def pasar_turno(self):
        """pasa el turno al siguiente jugador"""
        self.listaJugadores.rotate(1)  # rota el deque con los jugadores una posicion
        self.jugadorActual = self.listaJugadores[0]  # actualiza el jugador actual

    def is_ganador(self, jugador):
        """verifica si el jugador actual llego al puntaje ganador"""
        return jugador.puntosTotal >= self.puntajeGanador


class Jugador:
    """Jugador humano, nombre y puntos acumulados en el juego actual"""
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntosTotal = 0

    @staticmethod
    def elegir(self, dados):  # heredado por las maquinas
        pass


class MaquinaConservador(Jugador):
    @staticmethod
    def hay_triples(dados):
        """Verifica si algun numero salio tres veces y devuelve cual"""
        numeros = list(set(dados))  # toma los valores una sola vez
        cantidad = [[x, dados.count(x)] for x in numeros]  # lista con cantidad de veces que salieron los numeros
        # ordeno cantidad para que los que salieron mas veces aparezcan primero
        cantidad.sort(reverse=True, key=lambda x: x[1])

        for num in cantidad:  # sublistas tipo [num, cantidad]
            if num[1] == 3:  # si salio 3 veces
                return num[0]  # devuelve cual num salio 3 veces
            else:
                return 0

    def elegir(self, dados):
        """Para todas las maquinas. Eligen 1s, 5s, escaleras y triples"""
        eleccion = []
        indice = 0  # eleccion son los indices a elegir en la lista de dados

        escalera = [1, 2, 3, 4, 5, 6]  # caso en el que tiene un dado con cada valor
        if len(dados) == 6 and set(escalera).issubset(dados):  # verifica si la tirada es una escalera
            eleccion = [0, 1, 2, 3, 4, 5]  # elige todos los dados

        else:
            for valor in dados:
                if valor == 1:
                    eleccion.append(indice)  # agrega indice de los 1s a la lsita de eleccion
                if valor == 5:
                    eleccion.append(indice)  # agrega indice de los 5s a la lista de eleccion
                indice += 1  # pasa al siguiente indice

            # elegir triples
            triple = self.hay_triples(dados)  # 0 si no hay triples, sino num que salio triple
            if triple != 0 and triple != 5 and triple != 1:
                # algun num salio triple, no incluyo 5 ni 1 porque ya los eligio en el for anterior
                indice = 0  # eleccion es por indice
                for valor in dados:
                    if valor == triple:  # si es el num que salio triple
                        eleccion.append(indice)  # elige los indices donde esta el valor triple
                    indice += 1

        return eleccion

    def seguir(self, puntos):
        """Sigue hasta los 100 puntos"""
        return puntos <= 100  # devuelve True si no llego a los 100 puntos


class MaquinaNormal(MaquinaConservador):
    def seguir(self, puntos):
        """Sigue hasta los 200 puntos"""
        return puntos <= 200  # devuelve True si no llego a los 200 puntos


class MaquinaAgresivo(MaquinaConservador):
    def seguir(self, puntos):
        """Sigue hasta los 300 puntos"""
        return puntos <= 300  # devuelve True si no llego a los 300 puntos


class Dado:
    """un dado que cae en una cara (valor)"""
    def __init__(self):
        self.valor = 0  # valor de la cara
        self.guardado = False  # si esta guardado (True) no hay que volver a tirarlo
        self.sumado = False  # si ya se agrego su puntaje a los puntos acumulados en la ronda
                             # me sirve para no sumar el puntaje del mismo dado dos veces

    def tirar_dado(self):
        """tirar el dado y obtener un numero aleatorio del 1 al 6 para saber en qué cara 'cayó'
           llamado por turno y devuelve el valor a turno"""
        self.valor = random.randint(1, 6)


class Partida:
    def __init__(self, juego, dados, puntosTirada):
        self.juego = juego
        self.dados = dados
        self.puntosTirada = puntosTirada

    @staticmethod
    def pickle(path, objeto):
        """serializa objeto partida recibido en un archivo en el path que recibe"""
        pickle_out = open(path, "wb")  # abre el archivo para serializar el objeto
        pickle.dump(objeto, pickle_out)  # serializa objeto
        pickle_out.close()  # cierra archivo

    @staticmethod
    def unpickle(path):
        """deserializa objeto partida de un archivo en el path que recibe"""
        pickle_in = open(path, "rb")  # abre el archivo con los objetos serializados
        objeto = pickle.load(pickle_in)  # guarda el objeto
        pickle_in.close()  # cierra archivo

        return objeto  # devuelve el objeto

