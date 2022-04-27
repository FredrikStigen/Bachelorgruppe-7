

import PySimpleGUI as sg
import math

sg.theme('Dark2')

layout =    [[sg.VPush()],
            [sg.Push(), sg.Radio(text="Kunder", group_id=1, default=True), sg.Radio(text="Krim", group_id=1), sg.Push()],
            [sg.Push(), sg.Radio(text="0%", group_id=2, default=True), sg.Radio(text="5%", group_id=2),
             sg.Radio(text="10%", group_id=2), sg.Radio(text="15%", group_id=2), sg.Push()],
            [sg.Push(), sg.InputText(size=15), sg.Push()],
            [sg.Push(), sg.Text('', key='-TEXT-'), sg.Push()],
            [sg.Push(), sg.Text('', key='-TEXT2-'), sg.Push()],
            [sg.Push(), sg.Text('', key='-TEXT3-'), sg.Push()],
            [sg.Push(), sg.Text('', key='-TEXT4-'), sg.Push()],
            [sg.Push(), sg.Text('', key='-TEXT5-'), sg.Push()],
            [sg.Push(), sg.Button("Beregn"), sg.Button('Lukk'), sg.Push()],
            [sg.VPush()]]

window = sg.Window('TF Kalkulator', layout, size=(300, 300), resizable=True)

def pris(kunder):
    return kunder * 10000

def makskrim(kunder):
    return int((kunder / 2200) + 3)

def minkrim(kunder):
    return math.ceil(((kunder / 2200) + 3)/10)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Lukk'):
        break
    if event in ('Beregn'):
        if values[0] == True:
            kunder = int(values[6])
            price = pris(kunder)
            window['-TEXT3-'].update("Pris for kunder: {:,d},- kr".format(price))

            maksk = makskrim(kunder)
            mink = minkrim(kunder)

            window['-TEXT-'].update("Min krim: {:,d}".format(mink))
            window['-TEXT2-'].update("Maks krim: {:,d}".format(maksk))

            if values[2] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(kunder * 375))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(kunder * 375 * 2))
            elif values[3] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(int((kunder * 375) * 1.05)))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(int((kunder * 375 * 2) * 1.05)))
            elif values[4] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(int((kunder * 375) * 1.10)))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(int((kunder * 375 * 2) * 1.10)))
            elif values[5] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(int((kunder * 375) * 1.15)))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(int((kunder * 375 * 2) * 1.15)))
        elif values[1] == True:
            kunder = (int(values[6]) - 3) * 2200
            window['-TEXT-'].update("Krim: {:,d}".format(makskrim(kunder)))
            window['-TEXT2-'].update("Du trenger: {:,d} kunder".format(kunder))
            window['-TEXT3-'].update("Pris for kunder: {:,d},- kr".format(pris(kunder)))
            if values[2] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(kunder * 375))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(kunder * 375 * 2))
            elif values[3] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(int((kunder * 375) * 1.05)))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(int((kunder * 375 * 2) * 1.05)))
            elif values[4] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(int((kunder * 375) * 1.10)))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(int((kunder * 375 * 2) * 1.10)))
            elif values[5] == True:
                window['-TEXT4-'].update("Maks inntekt 1mg: {:,d},- kr".format(int((kunder * 375) * 1.15)))
                window['-TEXT5-'].update("Maks inntekt 2mg: {:,d},- kr".format(int((kunder * 375 * 2) * 1.15)))