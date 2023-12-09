from pyxl import *
info_icon = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB+0lEQVRIia3Wv2tTURQH8E9DBgcpAbWEDCWISCni4KCOUjAGNx1FioODqw4dHPwHHKSDiIiCi9XBTUWIoAiiCCIKFkGdtT/E34ikosO98T3jfS9a84VwX84753vOvff8eCPKMY4W9mALxlDBMubRwU28HMDzB+o4jSX8GPB7h4topohGErIWzuYMVnAXD/E67mADtmEX1kS9NziKy2WRH8TXGNknnESjRH89TuBttPmGY0XKU/gSFV9ge4y2HynZJB5H2y4O9CvU8SpHvilB0sAcrkfnqfePIsdCP8es7Fh2JozhvOxinxTsZEKWGHN5zwtROFtgSMiUnoNnqBboHY86H6JD01HwXUGq5aK7LZx1u0SvJrvLmXxk90qM/hVXI2enKmQAIc/LsBdb4/MiLpTo3sd+TFaF8ifkchn24XB8fjrAwfu4jhZd6NDQa1ywboi8tbh+rAhdkXTxrBY74jpfEVouocCaQyCvydK4U8EtISsqQjf833s5grX4jGs94SmDW8U5v7eKFDbLWsWVfLBjBje7tlCZMziUeF+XNbulFEdLNgvK2nUKEznyrjBXkpi2uoHTO5auvoGTGpltYWSOx/8ruIMHsmofFVJxSjYyF4UkuVQS0C80cEY2Cv9m6G9MEaV2kEdTuJvdwmdLPcqX8VyooRtKPlt+Aq3Ck3SHsl/0AAAAAElFTkSuQmCC'


def format_t(t):
        list2 = []
        for i in t:
            if i == None:
                list2.append('-')
            else:
                list2.append(i)
        return(list2)


def popup_table_layout(scaling,theme,starting_size_1,scale_var):
    bg = sg.theme_background_color()
    Day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    layout = [  [sg.Sizer(h_pixels = 0, v_pixels = 0)],
                [sg.Text('Teacher Name',background_color=bg,key='teach_name')],
                [sg.Table(
                    [[],[],[],[],[],[],[],[]], 
                    ['  ','Mon','Tue','Wed','Thu','Fri'],
                    key='table',
                    enable_click_events=True,
                    enable_events=True,
                    num_rows=8,
                    expand_x=True,
                    expand_y=True,
                    vertical_scroll_only = True,
                    hide_vertical_scroll=True,
                    justification = "center",
                    pad=(5,5),
                    alternating_row_color=sg.theme_progress_bar_color()[1],
                    )
                ],  
    ]
    layout1 = [
               [sg.VPush()],
               [sg.Checkbox(Day_list[0],disabled=True,enable_events=True)],
               [sg.Checkbox(Day_list[1],disabled=True,enable_events=True)],
               [sg.Checkbox(Day_list[2],disabled=True,enable_events=True)],
               [sg.Checkbox(Day_list[3],disabled=True,enable_events=True)],
               [sg.Checkbox(Day_list[4],disabled=True,enable_events=True)],
               [sg.VPush()],
               [sg.Push(),sg.Button(image_data=info_icon,border_width=0, button_color=(bg, bg),key = '?_tt')],
               ]
    
    col = sg.Column([[sg.Frame('Set Unavailable',layout1,expand_x=True,expand_y=True)]],expand_x=True,expand_y=True)
    col1 = sg.Col([[sg.Frame('Time Table',layout,element_justification='Center',expand_x=True,expand_y=True)]],expand_x=True,expand_y=True)
    test_layout = [[sg.Pane([col,col1],orientation='h',relief=None,expand_x=True,expand_y=True)]
                   ]
    window = sg.Window('Check TT', test_layout,keep_on_top=True,element_padding=(1,1),margins=(5,5),element_justification='Center',resizable=True,finalize = True,grab_anywhere = True,scaling=scaling)

    window.size = (window.size[0]+int(70*scaling),window.size[1])
    window.finalize()
    
    window.set_min_size(window.size)     
    return(window)



def popup_table_update(name,day,data,exec_class,window,exec_teach_raw = {}):

    out1 = []
    out = []
    table_data = []

    Day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    day_index = Day_list.index(day)
    time_t = find_free_periods_num(data,day_index,name,exec_class)[-1]
    window['teach_name'].update(name)
    
    for i in range(5):
        window[i].update(disabled=False)

    

    for i in range(5):
        time_t = find_free_periods_num(data,i,name,exec_class)[-1]
        out.append(format_t(time_t))
    #print(out)
    table_data = rotate(out)  
    for i in range(8):
        out1 += [[str(i+1)]+table_data[i]]

    window['table'].Update(out1)
    

    print(exec_teach_raw)

    if name in list(exec_teach_raw.keys()):
        for i in range(len(exec_teach_raw[name])):
            print(i)
            if exec_teach_raw[name][i]:
                window[i].Update(value = True)
            else:
                window[i].Update(value = False)
    else:
        for i in range(5):
            window[i].Update(value = False)


    return(out,table_data)
    