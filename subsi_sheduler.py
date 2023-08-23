import PySimpleGUI as sg

from pyxl import *
from unavlb_cls_sel import unavalible_cls_selector
from ShowTT import *

import shutil
from sys import exit
from os import name,system

import PySimpleGUI as sg

import pyperclip

empty_img = image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E@\x00\x00\x00\x00IEND\xaeB`\x82'


font_installed = False
for font in sg.Text.fonts_installed_list():
    if str(font).lower() == "roboto mono":
        font_installed = True



if name == 'nt':
    win_os = True
    from os import startfile 
    starting_size = (860,900)
    starting_size_1 = (630,400)  
else:
    win_os = False
    starting_size = (980,700)
    starting_size_1 = (727,380)

sg.set_options(font='Calibri 11')
if not font_installed:
    sg.popup('Please Install roboto mono font')
    if win_os:
        startfile('RobotoMono.ttf')
        exit()
    else:
        sg.popup('Linux Detected ; Please install calibri font olso')
        system('xdg-open "CalibriRegular.ttf"')
        system('xdg-open "RobotoMono.ttf"')
    sg.set_options(font='Helvetica 7')


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

update_s = False

if not error:
    
    out = []
    out1 = []

    window = None
    Day = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    period = ['1','2','3','4','5','6','7','8']
    selected_color = ('red', 'white')
    active_day,active_period,department_ = 'Monday',1,'all'
    teachers = []
    teacher_selected = None

    my_width, my_height = 1920,1080                                                                                                            #                                                                                                                        #
    width, height = sg.Window.get_screen_size()                                                                                               # -------> Set optimal program scaling w.r.t. the screen
    scaling_delta = min(width / my_width, height / my_height)
    


    def make_window(scaling = 2.3 , theme = 'SandyBeach'):
        global scale_var
        global window
        global scaling_delta

        scale_var = scaling_delta*scaling/2.3   
        print(scaling_delta,scaling,scale_var) 


        if window != None:
            window.close()
        sg.theme(theme)
        bg = sg.theme_background_color()
        bg_b = sg.theme_element_background_color()
        R_click_m = ['&Right',['More Info','Edit Data','Select unavalible classes','Preferences','Exit',]]
        
        layout = [  
                    [sg.Combo(values=dep_found,readonly=True,expand_x=True,key='department',auto_size_text=True,enable_events=True,default_value='All')],

                    [sg.Button(name,size = (10,1),expand_x=True) for name in Day],

                    [sg.Button(name,size=(6,1),expand_x=True) for name in period],

                    [
                        sg.Input(do_not_clear=True, size=(20,1),enable_events=True, key='_INPUT_FIND_TEACH_',expand_x=True),
                        sg.Button(image_data=info_icon,border_width=0, button_color=(bg, bg),key = 'Info_s')
                    ],

                    [sg.HorizontalSeparator()],

                    [sg.Text('Available Faculty',expand_x=True,justification='center',text_color='green',background_color=bg_b),
                    sg.Text('Engaged Faculty',expand_x=True,justification='center',text_color='red',background_color=bg_b)],

                    [sg.Listbox(values=teachers,font = ('roboto mono',9),key = 'free_list',text_color='Green',expand_x=True,expand_y=True,size = (27,16), enable_events=True,auto_size_text=True),sg.VSep(),
                    sg.Listbox(values=teachers,font = ('roboto mono',9),key = 'busy_list',text_color='Red',expand_x=True,expand_y=True,size = (27,16), enable_events=True,auto_size_text=True)],

                    [sg.Text(' ',key='status',border_width = 0,expand_x=True),sg.Button(image_data=info_icon,border_width=0, button_color=(bg, bg),key = 'Info')]
                    ]

                                                                                      #
        defalt_size = (round(starting_size[0]*scale_var),round(starting_size[1]*scale_var))
        print(defalt_size)
        window = sg.Window('Substitution Schedule Assistant',layout,auto_size_text=True,element_padding=0,scaling=scaling_delta*scaling,icon='icon.ico',margins=(1,1),resizable=True,right_click_menu=R_click_m)
        window.finalize()
        window.set_min_size((round(starting_size[0]*scale_var),round(232*scaling_delta)))          

                                                                                                #
        window['Monday'].update(button_color=selected_color)                                      # ------> Set defalt day,prd to monday,first prd and update the lists
        window['1'].update(button_color=selected_color)                                            #
        active_day_index = int(Day.index(active_day))                                               #
        active_period_num = int(active_period)                                                       #
                                                                                                            

        total_teach = len(is_free(data,1,1,'All')[0])+len(is_free(data,1,1,'All')[-1])
        window['status'].update(f'Loaded {len(dep_found)} departments with {total_teach} teachers')
        print('Window Made')
        return(window)


    scale_conf = None
    theme = None
    if config:
        scale_conf = float(config[0])
        theme = config[1]
        print(theme)
        window = make_window(scale_conf,theme)
        window2 = popup_table_layout(scaling_delta*scale_conf,theme,starting_size_1,scale_var)
    else:    
        window = make_window()
        window2 = popup_table_layout(scaling_delta*2.3,'kayak',starting_size_1,scale_var)
        
    counter = 0
    old_search = ''
    exec_class = [] 
    exec_teach_raw = {}
    out,table_data = [],[]
    
   # event, values = window.read()
    while True:             # Event Loop  
        counter += 1                                 #
        if counter > 1:                              #
            x = None                                 # ------> Initial one run to refresh lists
        else:                                        #
            x= 0                                     #
        

        win , event, values = sg.read_all_windows(x)
        print(win , event,values,sep='\n#######################################################################\n',end='\n#######################################################################\n')
        if event in (None, 'Exit'):
            break
        if event == 'Info':
            sg.popup('Substitution Schedule Assistant(v3.5) \nMade with <3 by Parth Sahni\n\nParthsahni09@gmail.com\ncompleted on 14/8/2023')
            try:
                if win_os:
                    startfile("https://github.com/P-rth/Subtitution-scheduler")
                else:
                    print("hello")
                    system('xdg-open "https://github.com/P-rth/Subtitution-scheduler"')
            except:
                sg.popup_error('error while opening github\nPlease open:https://github.com/P-rth/Subtitution-scheduler')

        if event == 'Info_s':
            sg.popup('This is the search bar \nIt can search for names,classes,number of free periods\nTo search unavailabe classes or teachers insted of cross use "!"')

        if event == 'Edit Data':
            if win_os:
                window.start_thread(lambda: system('Teacher_data.xlsx'), ('-THREAD-', '-THEAD ENDED-'))
            else:
                window.start_thread(lambda: system('xdg-open Teacher_data.xlsx'), ('-THREAD-', '-THEAD ENDED-'))
            
    
        if event == 'Select unavalible classes':
            mylist = find_classes(data)
            if exec_class != None:
                old_exec = exec_class 
                exec_class = unavalible_cls_selector(mylist,old_exec)
            else:
                exec_class = unavalible_cls_selector(mylist)
            
                
        if event in Day:
            update_s = True
            for k in Day:
                window[k].update(button_color=sg.theme_button_color())
            window[event].update(button_color=selected_color)
            active_day = event
        if event in period:
            update_s = True
            for k in period:
                window[k].update(button_color=sg.theme_button_color())
            window[event].update(button_color=selected_color)
            active_period = event

        
        if win == window:
            if values['department']:
                department_ = values['department']
            else:
                department_= None

            if event in Day or event in period or counter == 1 or event in ['Select unavalible classes','department','Preferences','✘']:
                update = True
            else:
                update = False

        if active_period != None and active_day != None and department_ != None and update:
            print(active_day,active_period,department_)
            active_day_index = int(Day.index(active_day))
            active_period_num = int(active_period)
            
            f_b_teach = is_free(data,active_period_num,active_day_index,department_,exec_class,exec_teach_raw)
            free_teach = f_b_teach[0]
            busy_teach = f_b_teach[-1]
            window['free_list'].update(values=free_teach)
            window['busy_list'].update(values=busy_teach)
            
        if event == 'free_list' and len(values['free_list']):
            teacher_selected = values['free_list'][0]
            teacher_selected = teacher_selected.split(':')[0].split('(')[0].strip()                                        #split has been done so that unavalible prompt dosent mess it up
            num_free_prd = find_free_periods_num(data,active_day_index,teacher_selected,exec_class)[0]
            pyperclip.copy(teacher_selected)
            window['status'].update(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
            print(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
         #  f_teach_name = unformat_list(list(free_teach.keys()))
         #   window['free_list'].set_vscroll_position(f_teach_name.index(teacher_selected)/len(free_teach))
           # window.Element('busy_list').Update(busy_teach) #remove background from other list (intentional)
            out,table_data = popup_table_update(teacher_selected,active_day,data,exec_class,window2,exec_teach_raw)
            
        if event == 'busy_list' and len(values['busy_list']):
            teacher_selected = values['busy_list'][0].split(':')[0].strip()
            teacher_selected = teacher_selected.split(':')[0].split('(')[0].strip()
            num_free_prd = find_free_periods_num(data,active_day_index,teacher_selected,exec_class)[0]
            pyperclip.copy(teacher_selected)
            window['status'].update(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
            
            print(teacher_selected+' has '+str(num_free_prd)+' free period(s) on '+active_day)
         #   b_teach_name = unformat_list(list(busy_teach.keys()))
         #   window['busy_list'].set_vscroll_position(b_teach_name.index(teacher_selected)/len(busy_teach))
            #window.Element('free_list').Update(free_teach) #remove background from other list (intentional)
            out,table_data = popup_table_update(teacher_selected,active_day,data,exec_class,window2,exec_teach_raw)
            
            
        if event == 'More Info':
    
            if teacher_selected != None:
                continue
            else:
                sg.popup('Select a teacher first')

        if event in range(5):
            unvlb_selected = [values[0],values[1],values[2],values[3],values[4]]
            exec_teach_raw[teacher_selected] = unvlb_selected   
 
            counter = 0
        
        
                
        if isinstance(event, tuple):
            if event[0] == 'table':
                if table_data != []:
                    if event[2][0] == -1 and event[2][1] != -1:           # Header was clicked and wasn't the "row" column
                        col_num_clicked = event[2][1]
                        if col_num_clicked > 0:
                            asd = ''
                            for i in out[col_num_clicked-1]:
                                asd = asd+i+' '
                            print(asd)
                            pyperclip.copy(asd)
                    else:
                        print(table_data[event[2][0]])
                        asd = ''
                        for i in table_data[event[2][0]]:
                            asd = asd+i+' '
                        print(asd)
                        pyperclip.copy(asd)
                    


        if event == '?_tt':
            sg.popup("Check the teacher's time Table. Crossed out classes mean the class is unavailable\nset unavailable to make teacher not show up in free list\nTo copy the time table for a day click the respective name of the day\nTo copy time table by period click on the respected row")

                
        if event == 'Preferences':
            if scale_conf and theme:
                scale1,theme1 = pref_popup(scale_conf,theme)
                
                if scale1 != scale_conf or theme1 != theme:
                    scale_conf = scale1
                    theme = theme1
                    window.close()
                    window2.close()
                    window = make_window(scale1,theme1)
                    window2 = popup_table_layout(scale1,theme1,starting_size_1,scale_var)
                    counter = 0

                    
                
            else:
                scale_conf,Theme = pref_popup()
                make_window(scale_conf,Theme)

        if win == window:
            if values['_INPUT_FIND_TEACH_'] not in ('',old_search,None) or event == "_INPUT_FIND_TEACH_" or update_s == True:
                update_s = False                         # if a keystroke entered in search field
                search = values['_INPUT_FIND_TEACH_']
                lower_free_list = [y.lower().replace('✘','!') for y in free_teach]
                new_values_free = [x for x in lower_free_list if search.lower() in x]  # do the filtering
                window.Element('free_list').Update([y.title().replace('!','✘') for y in new_values_free])     # display in the listbox

                lower_busy_list = [y.lower().replace('✘','!') for y in busy_teach]
                new_values_busy = [x for x in lower_busy_list if search.lower() in x]  # do the filtering
                window.Element('busy_list').Update([y.title().replace('!','✘') for y in new_values_busy])     # display in the listbox

            elif values['_INPUT_FIND_TEACH_'] != old_search:
                window.Element('free_list').Update(free_teach)          # display original unfiltered list
                window.Element('busy_list').Update(busy_teach)
                continue

            print(old_search)
            old_search = values['_INPUT_FIND_TEACH_']


                
            

    window.close()
 
else:
    sg.popup(error)