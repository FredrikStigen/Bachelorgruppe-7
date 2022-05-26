import PySimpleGUI as sg
import client

sg.theme('Dark2')
layout =    [[sg.VPush()],

             [sg.Push(), sg.Image("pictures/OMS3.png", size=(75, 75)), sg.Text("Control Panel", font=(any, 20)),
              sg.Push()],

            [sg.HorizontalSeparator()],

            [sg.Push(), sg.Text("Velocity:"), sg.InputText(size=(5, 5), default_text="120", tooltip="Degrees"),
             sg.Text("Acceleration:"), sg.InputText(size=(5, 5), default_text="6", tooltip="Radians Squared"), sg.Push()],
             [sg.Push()],

            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Radio(text="Rotate to position:                        ", group_id=1
                                 , default=True), sg.InputText(size=(5, 5), default_text="180", tooltip="Degrees"), sg.Push()],

            [sg.Push(), sg.Radio(text="Rotate between:", group_id=1, default=False), sg.InputText(size=(5, 5),
                                                                                                 default_text="0", tooltip="Degrees"),
             sg.Text("  <->    "), sg.InputText(size=(5, 5), default_text="180", tooltip="Degrees"), sg.Push()],

            [sg.Push(), sg.Radio(text="Rotate with:      ", group_id=1, default=False), sg.InputText(size=(5, 5),
                                                                                                    default_text="90", tooltip="Degrees"),
             sg.Text(" delay: "), sg.InputText(size=(5, 5), default_text="2", tooltip="Seconds"), sg.Push()],

            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button("Start Joystick", button_color=("White", "green")),
             sg.Button("Stop Joystick", button_color=("white", "red")), sg.Push()],
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
        #print("Stop")
        client.values(int(0), False, int(0), int(0), int(0))
    elif event in "Run":
        if values[5]:
            print(values[5])
            client.values(int(123), True, int(values[2]), int(values[3]), int(values[6]))
        elif values[7]:
            print(values[7])
            client.values(int(456), True, int(values[2]), int(values[3]), int(values[8]), int(values[9]))
        elif values[10]:
            client.values(int(789), True, int(values[2]), int(values[3]), int(values[11]), int(values[12]))
            #print(values[11], values[12])
    elif event in "Start Joystick":
        #print("Joystick started...")
        client.values(int(1111), True, int(values[2]), int(values[3]), int(values[6]))
    elif event in "Stop Joystick":
        #print("Joystick stopped...")
        client.values(int(2222), False, int(values[2]), int(values[3]), int(values[6]))



