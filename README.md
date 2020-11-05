# PP5proy 2020

## Objetivo del trabajo práctico
Se deberá realizar una aplicación gráfica que implemente el juego, incluyendo el siguiente
material:
1. Diagrama de clases con detalles explicativos
2. Patrones de diseño utilizados
3. Paquete de código de la aplicación realizada en Python 3.7+
4. Guía rápida de uso de la aplicación

## Aplicación a desarrollar
La aplicación que se desea desarrollar, tiene que tener las siguientes funcionalidades:
1. Permitir dos jugadores “humano” vs “humano”. El límite debe poder ser configurable
al inicio del juego (opciones 1000, 5000, 10000 o un número ingresado)
2. Poder jugar dos jugadores “humano” vs “máquina”. La máquina debe tener tres
modos de juegos configurables al inicio de la partida. El modo conservador se
planta cuando hizo 100 puntos o más. Un modo normal se planta a partir de 200 y
un modo agresivo se planta a partir de 300.
3. Grabar y recuperar el juego en un archivo. Al momento de jugar, un jugador puede
optar por grabar el juego y salir. Se deben grabar los puntajes hasta el momento y
cualquier información que considere necesaria para reanudarlo correctamente. Si
bien el trabajo es individual, se acepta compartir el protocolo de persistencia, de
forma tal de intercambiar archivos.

## Puntos Opcionales
La implementación de los siguientes items son opcionales, pero suman puntos a la
corrección final si se encuentran implementados en la entrega. Sin embargo, para que
tengan validez, la aplicación debe estar completa y funcional.
1. Inteligencia artificial avanzada: si la maquina detecta que lleva una determinada
ventaja sobre el jugador puede jugar en modo conservador mientras que, si se
encuentra en desventaja, puede alternar a modo normal o agresivo.
2. Grabar el ranking de jugadores, conteniendo los 10 mejores puntajes, y mantenerlo
actualizado a medida que finalizan las partidas, permitiendo ingresar un nombre del
jugador para grabarlo.
3. Implementar sonidos en determinados momentos del juego.
