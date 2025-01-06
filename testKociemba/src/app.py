import kociemba

color_to_face = {
    'white': 'U',
    'red': 'R',
    'green': 'F',
    'yellow': 'D',
    'orange': 'L',
    'blue': 'B',
}

colors = {
    'U': ['green', 'green', 'green', 'red', 'white', 'yellow', 'red', 'white', 'yellow'],
    'R': ['blue', 'blue', 'red', 'blue', 'blue', 'white', 'blue', 'blue', 'yellow'],
    'F': ['yellow', 'red', 'orange', 'yellow', 'red', 'orange', 'yellow', 'red', 'orange'],
    'D': ['orange', 'yellow', 'white', 'orange', 'yellow', 'white', 'blue', 'blue', 'blue'],
    'L': ['orange', 'green', 'green', 'yellow', 'green', 'green', 'white', 'green', 'green'],
    'B': ['white', 'white', 'white', 'orange', 'orange', 'orange', 'red', 'red', 'red'],
}

# Convertir a estado
estado = ''.join(color_to_face[color] for cara in ['U', 'R', 'F', 'D', 'L', 'B'] for color in colors[cara])
print(estado)

solucion = kociemba.solve(estado)

# Imprimir la solución
print("Solución:", solucion)