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

def isValidInput(preprocessedInput):
    if  preprocessedInput.count('U') == 9 and preprocessedInput.count('R') == 9 and preprocessedInput.count('F') == 9 and preprocessedInput.count('D') == 9 and preprocessedInput.count('L') == 9 and preprocessedInput.count('B') == 9:
        return True
    return False

def debugPreprocessedInput(preprocessedInput):
    print("Has ", preprocessedInput.count('U'), "/9 U.")
    print("Has ", preprocessedInput.count('R'), "/9 R.")
    print("Has ", preprocessedInput.count('F'), "/9 F.")
    print("Has ", preprocessedInput.count('D'), "/9 D.")
    print("Has ", preprocessedInput.count('L'), "/9 L.")
    print("Has ", preprocessedInput.count('B'), "/9 B.")