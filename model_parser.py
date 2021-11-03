import numpy as np

def getModel(file):
    with open(file, 'r') as model_file:
        data = model_file.read()

    model_points = []

    start = False
    for line in data.splitlines():
        if start:
            point = line.split(' ')
            l = len(point)
            if l != 6:
                break;
            x,y,z,r,g,b = point
            model_points.append([x,y,z])
        if (line == 'end_header'):
            start = True

    model = np.array(model_points, dtype=np.float)

    return model
