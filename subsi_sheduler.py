import PySimpleGUI as sg
from pyxl import *
import shutil
from sys import exit
import os


try:
    data,error = read_data('Teacher_data.xlsx')
except:
    data_path = sg.popup_get_file('Data file not found Please select manually:',keep_on_top=True,no_titlebar=True,file_types=((('Exel Teacher time-table data file', 'xlsx'),)))
    print(data_path)
    if data_path != None and data_path.strip() != '':
        shutil.copy(data_path, 'Teacher_data.xlsx', follow_symlinks=True)
        data,error = read_data('Teacher_data.xlsx')
    else:
        sg.popup('Blank Path selected, Exiting!')
        exit()  
        
data = tuple(data) #make data immutatable
    
dep_found=find_departments(data)+['All']

if not error:
    sg.theme('SandyBeach')
    bg_b = sg.theme_element_background_color()
    teachers = []
    Day = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    period = ['1','2','3','4','5','6','7','8']
    selected_color = ('red', 'white')
    active_day = None
    active_period = None
    department_ = None
    teacher_selected = None
    R_click_m = ['&Right',['Check Time Table','Edit Data','Info','Exit',]]
    layout = [  
                [sg.Combo(values=dep_found,readonly=True,expand_x=True,key='department',auto_size_text=True,enable_events=True,default_value='All')],
                [sg.Button(name,size = (10,1),expand_x=True) for name in Day],
                [sg.Button(name,size=(6,1),expand_x=True) for name in period],
                [sg.HorizontalSeparator()],
                [sg.Text('Available Faculty',expand_x=True,justification='center',text_color='green',background_color=bg_b),
                 sg.Text('Engaged Faculty',expand_x=True,justification='center',text_color='red',background_color=bg_b)],
                [sg.Listbox(values=teachers,key = 'free_list',text_color='Green',expand_x=True,expand_y=True,size = (24,2),no_scrollbar=True, enable_events=True,auto_size_text=True),sg.VSep(),
                 sg.Listbox(values=teachers,key = 'busy_list',text_color='Red',expand_x=True,expand_y=True,size = (24,2),no_scrollbar=True, enable_events=True,auto_size_text=True)],
                [sg.Text('Click a teacher to view number of free periods',key='status',font = 'Defalt 10',expand_x=True,relief='sunken'),sg.Input('UNAVBL CLS',key = 'exec_class',size = (8,1),expand_x=True,enable_events=True)]
                ]

    my_width, my_height = 1920,1080                                                                                                            #
    scaling_old = 2.3                                                                                                                          #
    width, height = sg.Window.get_screen_size()                                                                                                # -------> Set optimal program scaling w.r.t. the screen
    scaling_delta = min(width / my_width, height / my_height)                                                                                  #
    defalt_size = (round(680*scaling_delta),round(868*scaling_delta))
    window = sg.Window('Substitution Schedule Assistant', layout,element_padding=0,scaling=scaling_delta*scaling_old,icon='icon.ico',margins=(1,1),resizable=True,size=defalt_size,right_click_menu=R_click_m)
    window.finalize()
    window.set_min_size((round(680*scaling_delta),round(232*scaling_delta)))          

    active_day,active_period,department_ = 'Monday',1,'all'                                  #
    window['Monday'].update(button_color=selected_color)                                      # ------> Set defalt day,prd to monday,first prd and update the lists
    window['1'].update(button_color=selected_color)                                            #
    active_day_index = int(Day.index(active_day))                                               #
    active_period_num = int(active_period)                                                       #
                                                                                                         
    free_teach = is_free(data,active_period_num,active_day_index,department_)[0]                  #
    busy_teach = is_free(data,active_period_num,active_day_index,department_)[-1]                  #
    window['free_list'].update(values=free_teach)                                                   #
    window['busy_list'].update(values=busy_teach)                                                    #

    
    counter = 0
    
    while True:             # Event Loop  
        counter += 1                                 #
        if counter > 1:                              #
            x = None                                 # ------> Initial one run to refresh lists
        else:                                        #
            x= 1                                     #
        
        event, values = window.read(timeout=x)
        if event in (None, 'Exit'):
            break
        if event == 'Info':
            sg.popup('Substitution Schedule Assistant(v2.1) \n Made By Parth Sahni of class XII-E \n Parthsahni09@gmail.com \n completed on 19/5/2023')
        if event == 'Edit Data':
             window.start_thread(lambda: os.system('Teacher_data.xlsx'), ('-THREAD-', '-THEAD ENDED-'))
             
        if event == 'exec_class':
            if values['exec_class'] in ('UNAVBL CLS','UNAVBL CL'):                    # there are 2 options here because by pressing backspase on letter is deleted then a event is triggered
                window['exec_class'].update('')                                       # full one is there to be safe (idk lol)
                continue
                
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
            active_day_index = int(Day.index(active_day))
            active_period_num = int(active_period)
            
            exec_class = values['exec_class']
            f_b_teach = is_free(data,active_period_num,active_day_index,department_,exec_class)
            free_teach = f_b_teach[0]
            busy_teach = f_b_teach[-1]
            window['free_list'].update(values=free_teach)
            window['busy_list'].update(values=busy_teach)
            
        if event == 'free_list' and len(values['free_list']):
            exec_class = values['exec_class']
            teacher_selected = values['free_list'][0]
            teacher_selected = teacher_selected.split(':')[0]                                        #split has been done so that unavalible prompt dosent mess it up
            num_free_prd = find_free_periods_num(data,active_day_index,teacher_selected,exec_class)[0]
            window['status'].update(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
            print(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
        if event == 'busy_list' and len(values['busy_list']):
            exec_class = values['exec_class']
            teacher_selected = values['busy_list'][0].split('-')[0].strip()
            num_free_prd = find_free_periods_num(data,active_day_index,teacher_selected,exec_class)[0]
            
            window['status'].update(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
            print(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
        if event == 'Check Time Table':
            if teacher_selected != None:
                time_t = find_free_periods_num(data,active_day_index,teacher_selected)[-1]
                popup_table(time_t,teacher_selected,active_day)
            else:
                sg.popup('Select a teacher first')
                
            

    window.close()
 
else:
    sg.popup(error)