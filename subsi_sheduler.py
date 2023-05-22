import PySimpleGUI as sg

from pyxl import *
from unavlb_cls_sel import unavalible_cls_selector
from ShowTT import popup_table

import shutil
from sys import exit
from os import system,startfile

info_icon = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB+0lEQVRIia3Wv2tTURQH8E9DBgcpAbWEDCWISCni4KCOUjAGNx1FioODqw4dHPwHHKSDiIiCi9XBTUWIoAiiCCIKFkGdtT/E34ikosO98T3jfS9a84VwX84753vOvff8eCPKMY4W9mALxlDBMubRwU28HMDzB+o4jSX8GPB7h4topohGErIWzuYMVnAXD/E67mADtmEX1kS9NziKy2WRH8TXGNknnESjRH89TuBttPmGY0XKU/gSFV9ge4y2HynZJB5H2y4O9CvU8SpHvilB0sAcrkfnqfePIsdCP8es7Fh2JozhvOxinxTsZEKWGHN5zwtROFtgSMiUnoNnqBboHY86H6JD01HwXUGq5aK7LZx1u0SvJrvLmXxk90qM/hVXI2enKmQAIc/LsBdb4/MiLpTo3sd+TFaF8ifkchn24XB8fjrAwfu4jhZd6NDQa1ywboi8tbh+rAhdkXTxrBY74jpfEVouocCaQyCvydK4U8EtISsqQjf833s5grX4jGs94SmDW8U5v7eKFDbLWsWVfLBjBje7tlCZMziUeF+XNbulFEdLNgvK2nUKEznyrjBXkpi2uoHTO5auvoGTGpltYWSOx/8ruIMHsmofFVJxSjYyF4UkuVQS0C80cEY2Cv9m6G9MEaV2kEdTuJvdwmdLPcqX8VyooRtKPlt+Aq3Ck3SHsl/0AAAAAElFTkSuQmCC'



try:
    config_f = open("ss.config")
    config = config_f.read().split(',')
    config_f.close()  
except:
    config = None


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
    window = None
    Day = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    period = ['1','2','3','4','5','6','7','8']
    selected_color = ('red', 'white')
    active_day,active_period,department_ = 'Monday',1,'all'
    teachers = []
    teacher_selected = None
    def make_window(scaling = 2.3 , theme = 'SandyBeach'):
        global window
        global scaling_delta
        if window != None:
            window.close()
        sg.theme(theme)
        bg = sg.theme_background_color()
        bg_b = sg.theme_element_background_color()
        R_click_m = ['&Right',['Check Time Table','Edit Data','Select unavalible classes','Preferences','Exit',]]
        layout = [  
                    [sg.Combo(values=dep_found,readonly=True,expand_x=True,key='department',auto_size_text=True,enable_events=True,default_value='All')],
                    [sg.Button(name,size = (10,1),expand_x=True) for name in Day],
                    [sg.Button(name,size=(6,1),expand_x=True) for name in period],
                    [sg.HorizontalSeparator()],
                    [sg.Text('Available Faculty',expand_x=True,justification='center',text_color='green',background_color=bg_b),
                    sg.Text('Engaged Faculty',expand_x=True,justification='center',text_color='red',background_color=bg_b)],
                    [sg.Listbox(values=teachers,key = 'free_list',text_color='Green',expand_x=True,expand_y=True,size = (27,2),no_scrollbar=True, enable_events=True,auto_size_text=True),sg.VSep(),
                    sg.Listbox(values=teachers,key = 'busy_list',text_color='Red',expand_x=True,expand_y=True,size = (27,2),no_scrollbar=True, enable_events=True,auto_size_text=True)],
                    [sg.Text('Click a teacher to view number of free periods',key='status',border_width = 0,expand_x=True),sg.Button(image_data=info_icon,border_width=0, button_color=(bg, bg),key = 'Info')]
                    ]

        my_width, my_height = 1920,1080                                                                                                            #
        scaling_old = scaling                                                                                                                          #
        width, height = sg.Window.get_screen_size()                                                                                                # -------> Set optimal program scaling w.r.t. the screen
        scaling_delta = min(width / my_width, height / my_height)                                                                                  #
        defalt_size = (round(760*scaling_delta*scaling_old/2.3),round(868*scaling_delta*scaling_old/2.3))
        window = sg.Window('Substitution Schedule Assistant',layout,auto_size_text=True,font='Calibri 11',element_padding=0,scaling=scaling_delta*scaling_old,icon='icon.ico',margins=(1,1),resizable=True,size=defalt_size,right_click_menu=R_click_m)
        window.finalize()
        window.set_min_size((round(760*scaling_delta),round(232*scaling_delta)))          

                                                                                                #
        window['Monday'].update(button_color=selected_color)                                      # ------> Set defalt day,prd to monday,first prd and update the lists
        window['1'].update(button_color=selected_color)                                            #
        active_day_index = int(Day.index(active_day))                                               #
        active_period_num = int(active_period)                                                       #
                                                                                                            
        free_teach = is_free(data,active_period_num,active_day_index,department_)[0]                  #
        busy_teach = is_free(data,active_period_num,active_day_index,department_)[-1]                  #
        window['free_list'].update(values=free_teach)                                                   #
        window['busy_list'].update(values=busy_teach)
        return(window)


    scale_conf = None
    theme = None
    if config:
        scale_conf = float(config[0])
        theme = config[1]
        print(theme)
        window = make_window(scale_conf,theme)
    else:    
        window = make_window()
        
    counter = 0
    exec_class = [] 
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
            sg.popup('Substitution Schedule Assistant(v3) \nMade with <3 by Parth Sahni\n\nParthsahni09@gmail.com\ncompleted on 21/5/2023')
            try:
                startfile("https://github.com/P-rth/Subtitution-scheduler")
            except:
                sg.popup_error('error while opening github\nPlease open:https://github.com/P-rth/Subtitution-scheduler')
            
        if event == 'Edit Data':
             window.start_thread(lambda: system('Teacher_data.xlsx'), ('-THREAD-', '-THEAD ENDED-'))
            
    
        if event == 'Select unavalible classes':
            mylist = find_classes(data)
            if exec_class != None:
                old_exec = exec_class 
                exec_class = unavalible_cls_selector(mylist,old_exec)
            else:
                exec_class = unavalible_cls_selector(mylist)
            
                
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
            
            f_b_teach = is_free(data,active_period_num,active_day_index,department_,exec_class)
            free_teach = f_b_teach[0]
            busy_teach = f_b_teach[-1]
            window['free_list'].update(values=free_teach)
            window['busy_list'].update(values=busy_teach)
            
        if event == 'free_list' and len(values['free_list']):
            teacher_selected = values['free_list'][0]
            teacher_selected = teacher_selected.split(':')[0]                                        #split has been done so that unavalible prompt dosent mess it up
            num_free_prd = find_free_periods_num(data,active_day_index,teacher_selected,exec_class)[0]
            window['status'].update(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
            print(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
        if event == 'busy_list' and len(values['busy_list']):
            teacher_selected = values['busy_list'][0].split('-')[0].strip()
            num_free_prd = find_free_periods_num(data,active_day_index,teacher_selected,exec_class)[0]
            
            window['status'].update(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
            print(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
        if event == 'Check Time Table':
            if teacher_selected != None:
                print(scaling_delta)
                popup_table(teacher_selected,active_day,data,exec_class,scaling_delta)
            else:
                sg.popup('Select a teacher first')
                
        if event == 'Preferences':
            if scale_conf and theme:
                scale1,theme1 = pref_popup(scale_conf,theme)
                
                if scale1 != scale_conf or theme1 != theme:
                    scale_conf = scale1
                    theme = theme1
                    make_window(scale1,theme1,)
                
            else:
                scale_conf,Theme = pref_popup()
                make_window(scale_conf,Theme)
                
            

    window.close()
 
else:
    sg.popup(error)