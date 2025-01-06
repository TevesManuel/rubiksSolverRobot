colorToFace = {
    'white'  : 'U',
    'blue'   : 'R',
    'red'    : 'F',
    'yellow' : 'D',
    'green'  : 'L',
    'orange' : 'B',
}

cubeFaces = {
    "whiteFace": [],
    "blueFace": [],
    "redFace": [],
    "yellowFace": [],
    "greenFace": [],
    "orangeFace": []
}

def preprocessInput(cubeFaces):
    return ''.join(colorToFace[color] for face in ['whiteFace', 'blueFace', 'redFace', 'yellowFace', 'greenFace', 'orangeFace'] for color in cubeFaces[face])