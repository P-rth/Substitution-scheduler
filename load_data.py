import PySimpleGUI as sg
import ipaddress
from read_data_sql import *
from pyxl import *
from export_gui import *

def read_data_popup(sql=False,loc=(False,False),firststart = True):
    sg.theme('kayak')

    path = 'Teacher_data.xlsx'
    host = 'localhost'
    user = 'root'
    password = ''


    if firststart:
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



    internal_layout_exel = [
                      [sg.Text('File Location :'),sg.InputText(size=(30, 1), key='-FILENAME-',default_text=path)],
                      [sg.FileBrowse(enable_events=True),sg.Push(),sg.Button('Export to SQL')]
                      ]

    internal_layout_sql = [
                      [sg.Text('Host : ') ,sg.InputText(size=(30, 1),key='Host' ,default_text=host,expand_x=True), ],
                      [sg.Text('User : ') ,sg.InputText(size=(30, 1),key='User',default_text=user,expand_x=True), ],
                      [sg.Text('Password : ') ,sg.InputText(size=(30, 1),key='Password',default_text=password,expand_x=True),],
                      ]

    if sql == False:
        exel = True
        internal_layout = internal_layout_exel
    else:
        exel = False
        internal_layout = internal_layout_sql

    layout = [
        [sg.Text('Load data from:')],
        [sg.Radio('Exel','source',default=exel,enable_events=True,key='exel'),sg.Push(),sg.Radio('SQL','source',default=sql,enable_events=True,key='sql'),sg.Push()],
        [sg.Frame('Config',internal_layout,expand_x=True)],
        [sg.Checkbox(' Remember This',key='Remember',default = True)],
        [sg.Button('Go',disabled=True),sg.Push(), sg.Button('Exit'),],
    ]


    window = sg.Window('Substitution-schedule-assistant', layout,location=loc,finalize=True)
    if loc == (False,False) :
        window.move_to_center()


    while True:
        event, values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED,'Exit'):
            break
        if event == 'sql':
            x,y = window.current_location(more_accurate = True)
            window.close()
            return read_data_popup(sql=True,loc=(x,y),firststart = False)
            break
            
        if event == 'exel':
            x,y = window.current_location(more_accurate = True)
            window.close()
            return read_data_popup(sql=False,loc=(x,y),firststart = False)
            break

        if event == 'Export to SQL':
            export_to_sql_gui()

        if sql:
            if validip(values['Host']) or values['Host'] == 'localhost' and values['User'] :
                window['Go'].update(disabled=False)
            else:
                window['Go'].update(disabled=True)

        if exel:
            if values['-FILENAME-']:
                window['Go'].update(disabled=False)
            else:
                window['Go'].update(disabled=True)



        if event == 'Go':
            if sql == True:
                db_config = {
                    'host': values['Host'],
                    'user': values['User'],
                    'password': values['Password'],
                    'database': 'ssa_db'
                }
                data = read_data_from_sql(db_config)
                if data[0] == 'Error':
                    sg.popup(data[1])
                else:
                    if values['Remember'] == True:
                        csvwrite([
                                ['db','sql'],
                                ['host',values['Host']],
                                ['user',values['User']],
                                ['password',values['Password']]
                        ])
                    window.close()
                    return data
                    break  


            if exel == True:
                try:
                    data,error = read_data(values['-FILENAME-'])
                    if values['Remember'] == True:
                        csvwrite([
                                ['db','exel'],
                                ['path',values['-FILENAME-']]
                        ]) 
                    window.close()
                    return data
                    break 

                except Exception as e:
                    sg.popup(e)



    window.close()

