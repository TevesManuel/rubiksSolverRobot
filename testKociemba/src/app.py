import kociemba

colorToFace = {
    'white'  : 'U',
    'blue'   : 'R',
    'red'    : 'F',
    'yellow' : 'D',
    'green'  : 'L',
    'orange' : 'B',
}

colors = {
    'U': [ 'green'  , 'green'  , 'green'  , 'red'    , 'white'  , 'yellow' , 'red'    , 'white' , 'yellow' ],
    'R': [ 'blue'   , 'blue'   , 'red'    , 'blue'   , 'blue'   , 'white'  , 'blue'   , 'blue'  , 'yellow' ],
    'F': [ 'yellow' , 'red'    , 'orange' , 'yellow' , 'red'    , 'orange' , 'yellow' , 'red'   , 'orange' ],
    'D': [ 'orange' , 'yellow' , 'white'  , 'orange' , 'yellow' , 'white'  , 'blue'   , 'blue'  , 'blue'   ],
    'L': [ 'orange' , 'green'  , 'green'  , 'yellow' , 'green'  , 'green'  , 'white'  , 'green' , 'green'  ],
    'B': [ 'white'  , 'white'  , 'white'  , 'orange' , 'orange' , 'orange' , 'red'    , 'red'   , 'red'    ],
}

state = ''.join(colorToFace[color] for face in ['U', 'R', 'F', 'D', 'L', 'B'] for color in colors[face])

print("State: ", state)
solution = kociemba.solve(state)
print("Solution:", solution)