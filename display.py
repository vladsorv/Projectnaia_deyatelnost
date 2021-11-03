#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

from model_parser import getModel
import numpy as np

from model_parser import getModel
import numpy as np

import json
import serial

ser = serial.Serial('COM3', 9600, timeout=0.1)
model_info = getModel('untitled.ply')

def main():
    colors = vtkNamedColors()

    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    actor = vtkActor()
    renderer.AddActor(actor)
    renderWindow.SetSize(600, 600)
    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))

    renderWindow.SetWindowName('Model')

    data=[0,0,0]
    while True:
        try:
            bytes_data = ser.readline()
            if len(bytes_data) > 0:
                data = json.loads(bytes_data.decode('utf-8'))
        except:
            pass
        print(data)
        x_ang,y_ang,z_ang = data
        model_to_display = model_info.dot([[1,              0,               0],
                                           [0,  np.cos(x_ang),  -np.sin(x_ang)],
                                           [0,  np.sin(x_ang),   np.cos(x_ang)]]).dot([[ np.cos(y_ang),  0,  np.sin(y_ang)],
                                                                                       [             0,  1,              0],
                                                                                       [-np.sin(y_ang),  0,  np.cos(y_ang)]]).dot([[ np.cos(z_ang),  -np.sin(z_ang),  0],
                                                                                                                                   [ np.sin(z_ang),   np.cos(z_ang),  0],
                                                                                                                                   [             0,               0,  1]])


        points = vtkPoints()

        for point in model_to_display:
            points.InsertNextPoint(point)

        polydata = vtkPolyData()
        polydata.SetPoints(points)

        glyphFilter = vtkVertexGlyphFilter()
        glyphFilter.SetInputData(polydata)
        glyphFilter.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(glyphFilter.GetOutputPort())
        mapper.Update()

        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colors.GetColor3d('Gold'))
        actor.GetProperty().SetPointSize(10)

        renderWindow.Render()

        renderWindowInteractor.ProcessEvents()

if __name__ == '__main__':
    main()
