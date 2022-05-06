import PySimpleGUI as sg
import os
import client

sg.theme('Dark2')
layout =    [[sg.VPush()],
             [sg.Push(), sg.Image("pictures/logo2.png", size=(75, 75)), sg.Text("Control Panel", font=(any, 20)),
              sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text("Velocity:"), sg.InputText(size=(5, 5), default_text="120"),
             sg.Text("Acceleration:"), sg.InputText(size=(5, 5), default_text="6"), sg.Push()],
             [sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Radio(text="Rotate to position:                        ", group_id=1
                                 , default=True), sg.InputText(size=(5, 5), default_text="180"), sg.Push()],
            [sg.Push(), sg.Radio(text="Rotate between:", group_id=1, default=False), sg.InputText(size=(5, 5),
                                                                                                 default_text="0"),
             sg.Text("  <->    "), sg.InputText(size=(5, 5), default_text="180"), sg.Push()],
            [sg.Push(), sg.Radio(text="Rotate with:      ", group_id=1, default=False), sg.InputText(size=(5, 5),
                                                                                                    default_text="90"),
             sg.Text(" delay: "), sg.InputText(size=(5, 5), default_text="2"), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text(""), sg.Push()],
            [sg.Push(), sg.Button("Run"), sg.Button("Stop", button_color=("white", "red")),
             sg.Button("Cancel", button_color=("white", "gray")), sg.Push()],
            [sg.VPush()]]

window = sg.Window("OMS Control GUI", layout, resizable=True)



while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        client.values(int(0), False, int(0), int(0), int(0))
        break
    elif event in "Stop":
        client.values(int(0), False, int(0), int(0), int(0))
    elif event in "Run":
        #print("Velocity: {}  --  Acceleartion: {}".format(values[2], values[3]))
        if values[5]:
            #print("Rotating to pos: {}".format(values[6]))
            client.values(int(123), True, int(values[2]), int(values[3]), int(values[6]))
        elif values[7]:
            client.values(int(456), True, int(values[2]), int(values[3]), int(values[8]), int(values[9]))
        elif values[10]:
            #print("Rotating {} degrees, then wait for {} seconds".format(values[11], values[12]))
            client.values(int(789), True, int(values[2]), int(values[3]), int(values[11]), int(values[12]))



