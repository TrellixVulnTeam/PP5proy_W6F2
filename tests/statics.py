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

def is_escalera(dados):
    """Verifica si la tirada es una escalera y devuelve True, caso contrario False"""
    escalera = [1, 2, 3, 4, 5, 6]  # caso en el que tiene un dado con cada valor
    return len(dados) == 6 and set(escalera).issubset(dados)

def hay_triples(dados):  # en clase juego
    """Verifica si hay numeros que salieron tres veces y devuelve True"""
    numeros = list(set(dados))  # toma los valores una sola vez
    cantidad = [dados.count(x) for x in numeros]  # lista con cantidad de veces que salieron los numeros
    return cantidad.count(3) > 0 or cantidad.count(6) > 0

def turno_perdido(dados):
    """Verifica si la tirada sirve o se perdio el turno, devuelve True si se pierde el turno
       Turno sirve si hay 1, 5, numero triple o escalera"""

    if not is_escalera(dados):  # no es escalera (contiene 1 y 5)
        if 1 not in dados and 5 not in dados:  # no hay 1s ni 5s
            if not hay_triples(dados):  # no hay triples
                return True

    return False  # si alguna de las anteriores no se cumplio

def calcular_puntos(eleccion):
    """toma la lista de dados elegidos y calcula el puntaje que darian"""
    numeros = list(set(eleccion))  # toma los valores de las caras una sola vez ej eleccion = [6,6,6] numeros = [6]
    cantidad = [[x, eleccion.count(x)] for x in numeros]  # devuelve lista de sublistas, cuantas veces esta c/u

    if is_escalera(eleccion):  # verifica si es escalera
        return 2500  # escalera vale 2500 puntos

    else:
        puntos = 0
        for sublista in cantidad:  # recorre sublistas de num de cara y cuantas veces esta ej [1, 3]
            dado = sublista[0]  # toma el valor de la cara del dado
            cant = sublista[1]  # toma cuantas veces salio ese valor
            # busca el puntaje en dicc y agrega a puntaje del turno
            puntos += dadoValor[dado][cant]

        return puntos

def maquina_hay_triples(dados):  # para eleccion de triples por la maquina
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