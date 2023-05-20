from pyxl import *
info_icon = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB+0lEQVRIia3Wv2tTURQH8E9DBgcpAbWEDCWISCni4KCOUjAGNx1FioODqw4dHPwHHKSDiIiCi9XBTUWIoAiiCCIKFkGdtT/E34ikosO98T3jfS9a84VwX84753vOvff8eCPKMY4W9mALxlDBMubRwU28HMDzB+o4jSX8GPB7h4topohGErIWzuYMVnAXD/E67mADtmEX1kS9NziKy2WRH8TXGNknnESjRH89TuBttPmGY0XKU/gSFV9ge4y2HynZJB5H2y4O9CvU8SpHvilB0sAcrkfnqfePIsdCP8es7Fh2JozhvOxinxTsZEKWGHN5zwtROFtgSMiUnoNnqBboHY86H6JD01HwXUGq5aK7LZx1u0SvJrvLmXxk90qM/hVXI2enKmQAIc/LsBdb4/MiLpTo3sd+TFaF8ifkchn24XB8fjrAwfu4jhZd6NDQa1ywboi8tbh+rAhdkXTxrBY74jpfEVouocCaQyCvydK4U8EtISsqQjf833s5grX4jGs94SmDW8U5v7eKFDbLWsWVfLBjBje7tlCZMziUeF+XNbulFEdLNgvK2nUKEznyrjBXkpi2uoHTO5auvoGTGpltYWSOx/8ruIMHsmofFVJxSjYyF4UkuVQS0C80cEY2Cv9m6G9MEaV2kEdTuJvdwmdLPcqX8VyooRtKPlt+Aq3Ck3SHsl/0AAAAAElFTkSuQmCC'

def popup_table(name,day,data,exec_class,scaling_delta = 1):
   
    Day_list = ['Monday','Tuesday','Wednesday','Thursday','Friday']
    day_index = Day_list.index(day)
    time_t = find_free_periods_num(data,day_index,name,exec_class)[-1]
    bg = sg.theme_background_color()

    def format_t(t=time_t):
        list2 = []
        for i in time_t:
            if i == None:
                list2.append('-')
            else:
                list2.append(i)
        out = []
        for i in range(len(list2)):
            x = []
            x.extend([i+1,list2[i]])
            out.append(x)
        return(out)
                   
               
    layout = [  [sg.Text(name,background_color=sg.theme_background_color())],
                [sg.Combo(Day_list,default_value = day,key = 'dayselect',readonly=True,enable_events=True)],
                [sg.Table(
                    format_t(), 
                    ['Period','Class'],key='table', num_rows=8,expand_x=True,expand_y=True,hide_vertical_scroll=True,justification = "center",row_height=28,pad=(5,5)
                    )
                ],
                [sg.Button('Ok',border_width=0,font = 'Calibri 8',size = (3,1)),sg.Push(),sg.Button(image_data=info_icon,border_width=0, button_color=(bg, bg),key = '?')]
    ]
    window = sg.Window('Check TT', layout,margins=(0,0),element_justification='Center',element_padding = (20,5))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Ok'):
            break
        if event == 'dayselect':
            if values['dayselect'] != day:
                day = values['dayselect']
                day_index = Day_list.index(day)
                time_t = find_free_periods_num(data,day_index,name,exec_class)[-1]
                window['table'].update(format_t())
        if event == '?':
            sg.popup("Check the teacher's time Table for the selected day or any other day of the week. Crossed out classes mean the class is unavailable")
                
            
            
    window.close()
    
