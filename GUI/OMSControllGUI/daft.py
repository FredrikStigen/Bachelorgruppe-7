import os
#PySimpleGui is the name of library we use to develop a GUI
import PySimpleGUI as sg

#Defines a theme for the GUI
sg.theme('Dark2')

#Defines how the layout of the GUI is, and what operations are available in the GUI
layout =    [[sg.VPush()],
             [sg.Push(), sg.Image("pictures/logo2.png", size=(75, 75)), sg.Text("Control Panel", font=(any, 20)),
              sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text("Velocity:"), sg.InputText(size=(5, 5), default_text="0"),
             sg.Text("Acceleration:"), sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
             [sg.Push()],
            [sg.HorizontalSeparator()],

            [sg.Push(), sg.Radio(text="Rotate to position:                        ", group_id=1, default=True),
             sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
            [sg.Push(), sg.Radio(text="Rotate between:", group_id=1, default=True),
             sg.InputText(size=(5, 5), default_text="0"),
             sg.Text("  <->    "),sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
            [sg.Push(), sg.Radio(text="Rotate with:      ", group_id=1, default=True),
             sg.InputText(size=(5, 5), default_text="0"),
             sg.Text(" delay: "), sg.InputText(size=(5, 5), default_text="0"), sg.Push()],

            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text(""), sg.Push()],
            [sg.Push(), sg.Button("Run"), sg.Button("Stop", button_color=("white", "red")),
             sg.Button("Cancel", button_color=("white", "gray")), sg.Push()],
            [sg.VPush()]]

#Defines the popup window, with the namebar, layout and that it is resizeable
window = sg.Window("OMS Control GUI", layout, resizable=True)

#Event loop for the GUI
#We define what should happen when any of the buttons on the GUI is pressed
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event in "Stop":
        print("Stopping...")
    elif event in "Run":
        vel = values[2]
        acc = values[3]
        rtpc = values[5]
        pos = values[6]
        rbpc = values[7]
        pos1 = values[8]
        pos2 = values[9]
        rdwdc = values[10]
        dis = values[11]
        delay = values[12]
        method = 0

        print(vel)
        print(acc)
        if rtpc == True:
            print(pos)
            method = 1
            print(method)
        elif rbpc == True:
            print(pos1)
            print(pos2)
            method = 2
            print(method)
        elif rdwdc == True:
            print(dis)
            print(delay)
            method = 3
            print(method)

