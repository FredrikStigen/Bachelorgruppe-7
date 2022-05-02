import PySimpleGUI as sg
import os

sg.theme('Dark2')
layout =    [[sg.VPush()],
             [sg.Push(), sg.Image("pictures/logo2.png", size=(75, 75)), sg.Text("Control Panel", font=(any, 20)),
              sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text("Velocity:"), sg.InputText(size=(5, 5), default_text="0"),
             sg.Text("Acceleration:"), sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
             [sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Radio(text="Rotate to position:                        ", group_id=1
                                 , default=True), sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
            [sg.Push(), sg.Radio(text="Rotate between:", group_id=1, default=True), sg.InputText(size=(5, 5),
                                                                                                 default_text="0"),
             sg.Text("  <->    "), sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
            [sg.Push(), sg.Radio(text="Rotate with:      ", group_id=1, default=True), sg.InputText(size=(5, 5),
                                                                                                    default_text="0"),
             sg.Text(" delay: "), sg.InputText(size=(5, 5), default_text="0"), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Text(""), sg.Push()],
            [sg.Push(), sg.Button("Run"), sg.Button("Stop", button_color=("white", "red")),
             sg.Button("Cancel", button_color=("white", "gray")), sg.Push()],
            [sg.VPush()]]

window = sg.Window("OMS Control GUI", layout, resizable=True)



while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event in "Stop":
        print("Stopping...")
    elif event in "Run":
        if values[6] == True:
            print("1 True")
        elif values[8] == True:
            print("2 True")
        elif values[11] == True:
            print("3 True")


'''#print(values[0])
        #print(values[1])
        print(values[2]) #vel
        print(values[3]) #acc
        print(values[4]) #runtime
        #print(values[5])
        print(values[6]) #rtp
        print(values[7]) #pos
        print(values[8]) #rb
        print(values[9]) #pos1
        print(values[10]) #pos2
        print(values[11]) #rwd
        print(values[12]) #dist
        print(values[13]) #delay'''