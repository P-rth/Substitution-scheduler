import PySimpleGUI as sg
from pyxl import *
import shutil
import os


try:
    data,error = read_data('Teacher_data.xlsx')
except:
    data_path = sg.popup_get_file('Data file not found Please select manually:',keep_on_top=True,file_types=(('Exel Teacher time-table data file','xlsx')))
    shutil.copy(data_path, 'Teacher_data.xlsx', follow_symlinks=True)
    data,error = read_data('Teacher_data.xlsx')
    
    
dep_found=find_departments(data)+['ANY']

if not error:
    sg.theme('Greenmono')
    teachers = []
    Day = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    period = ['1','2','3','4','5','6','7','8']
    selected_color = ('red', 'white')
    active_day = None
    active_period = None
    department_ = None

    layout = [  
                [sg.Combo(values=dep_found,readonly=True,expand_x=True,key='department',auto_size_text=True,enable_events=True,default_value='ANY')],
                [sg.Button(name,size = (10,1)) for name in Day],
                [sg.Button(name,size=(6,1),expand_x=True) for name in period],
                [sg.Listbox(values=teachers,key = 'free_list',text_color='Green',expand_x=True,expand_y=True,size = (24,30),right_click_menu=['&Right',['Edit Data','Exit']]),
                 sg.Listbox(values=teachers,key = 'busy_list',text_color='Red',expand_x=True,expand_y=True,size = (24,30),right_click_menu=['&Right',['Edit Data','Exit']])]
                ]

    window = sg.Window('Window Title', layout,element_padding=0,scaling=2)

    while True:             # Event Loop
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == 'Edit Data':
             os.system('Teacher_data.xlsx')
        if event in Day:
            for k in Day:
                window[k].update(button_color=sg.theme_button_color())
            window[event].update(button_color=selected_color)
            active_day = event
        if event in period:
            for k in period:
                window[k].update(button_color=sg.theme_button_color())
            window[event].update(button_color=selected_color)
            active_period = event
        if values['department']:
            department_ = values['department']
        else:
            department_= None
        if active_period != None and active_day != None and department_ != None:
            print(active_day,active_period,department_)
            active_day_num = int(Day.index(active_day)+1)
            active_period_num = int(active_period)
            
            free_teach = is_free(data,active_period_num,active_day_num,department_)[0]
            busy_teach = is_free(data,active_period_num,active_day_num,department_)[-1]
            window['free_list'].update(values=free_teach)
            window['busy_list'].update(values=busy_teach)

    window.close()
    
else:
    sg.popup(error)