import os
import PySimpleGUI as sg

sg.theme('Dark2')

layout =    [[sg.VPush()],
            [sg.Push(), sg.Text("Rotate degrees:       "), sg.InputText(size=(10,5), default_text="0"), sg.Push()],
            [sg.Push(), sg.Text("Acceleration m/s^2: "), sg.InputText(size=(10, 5), default_text="0"), sg.Push()],
            [sg.Push(), sg.Text("Speed m/s:             "), sg.InputText(size=(10, 5), default_text="0"), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button("Run"), sg.Button("Stop"), sg.Button("Cancel"), sg.Push()],
            [sg.VPush()]]

window = sg.Window("OMS Controll system", layout, resizable=True)


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event in "Run":
        print(values[0])
        print(values[1])
        print(values[2])
    elif event in "Stop":
        print("Stopping...")