import PySimpleGUI as sg
import ipaddress
from pyxl import csvread,validip
from export_to_sql import exportsql


def export_to_sql_gui():
    sg.theme('kayak')
    path = 'Teacher_data.xlsx'
    host = 'localhost'
    user = 'root'
    password = ''

    db_pref = csvread()
    if db_pref != None:
        if db_pref[0][1] == 'sql':
            sql = True
            host = db_pref[1][1]
            user = db_pref[2][1]
            password = db_pref[3][1]

        if db_pref[0][1] == 'exel':
            sql = False
            path = db_pref[1][1]


    layout_sql = [
                [sg.Text('Host : ') ,sg.InputText( key='Host' ,default_text=host,expand_x=True), ],
                [sg.Text('User : ') ,sg.InputText( key='User',default_text=user,expand_x=True), ],
                [sg.Text('Password : ') ,sg.InputText( key='Password',default_text=password,expand_x=True),],
            ]

    layout_exel = [
                   [],
                   [sg.Text('Select File :'),sg.InputText( key='-FILENAME-',default_text=path), sg.FileBrowse(enable_events=True)],
                  ]

    layout = [
              [sg.Frame('SQL',layout_sql,expand_x=True)],
              [sg.Frame('Excel',layout_exel,expand_x=True)],
              [sg.Button('Export',disabled=True),sg.Push(),sg.Button('Exit')]
             ]

    window = sg.Window('Title', layout)

    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED,'Exit'):
            break

        if validip(values['Host']) or values['Host'] == 'localhost' and values['User'] and values['-FILENAME-'] :
            window['Export'].update(disabled=False)
        else:
            window['Export'].update(disabled=True)

        if event == 'Export':
            db_config = {
                    'host': values['Host'],
                    'user': values['User'],
                    'password': values['Password'],
                }
            x = exportsql(db_config,values['-FILENAME-'])
            if x[0] == 'Error':
                sg.popup(x[1])
            else:
                sg.popup(f'{x[0]} teacher records uploaded to sql database')

    window.close()
