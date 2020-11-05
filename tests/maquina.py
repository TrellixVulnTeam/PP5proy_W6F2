class Jugador:
    """Jugador humano, nombre y puntos acumulados en el juego actual"""
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntosTotal = 0

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