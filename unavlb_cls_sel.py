import PySimpleGUI as sg

info_icon = b'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAB+0lEQVRIia3Wv2tTURQH8E9DBgcpAbWEDCWISCni4KCOUjAGNx1FioODqw4dHPwHHKSDiIiCi9XBTUWIoAiiCCIKFkGdtT/E34ikosO98T3jfS9a84VwX84753vOvff8eCPKMY4W9mALxlDBMubRwU28HMDzB+o4jSX8GPB7h4topohGErIWzuYMVnAXD/E67mADtmEX1kS9NziKy2WRH8TXGNknnESjRH89TuBttPmGY0XKU/gSFV9ge4y2HynZJB5H2y4O9CvU8SpHvilB0sAcrkfnqfePIsdCP8es7Fh2JozhvOxinxTsZEKWGHN5zwtROFtgSMiUnoNnqBboHY86H6JD01HwXUGq5aK7LZx1u0SvJrvLmXxk90qM/hVXI2enKmQAIc/LsBdb4/MiLpTo3sd+TFaF8ifkchn24XB8fjrAwfu4jhZd6NDQa1ywboi8tbh+rAhdkXTxrBY74jpfEVouocCaQyCvydK4U8EtISsqQjf833s5grX4jGs94SmDW8U5v7eKFDbLWsWVfLBjBje7tlCZMziUeF+XNbulFEdLNgvK2nUKEznyrjBXkpi2uoHTO5auvoGTGpltYWSOx/8ruIMHsmofFVJxSjYyF4UkuVQS0C80cEY2Cv9m6G9MEaV2kEdTuJvdwmdLPcqX8VyooRtKPlt+Aq3Ck3SHsl/0AAAAAElFTkSuQmCC'


def unavalible_cls_selector(names,names_sel_old = []):
    bg = sg.theme_background_color()
    names_sel = names_sel_old
    for i in names_sel_old:
        names.remove(i)

    layout = [[sg.Text('Search'),sg.Input(size=(30, 1), enable_events=True, key='-INPUT-',expand_x= True),sg.Button(image_data=info_icon,key = 'Help',border_width=0, button_color=(bg, bg))],
            [sg.HSep(pad=((0,0),(0,5)),color = sg.theme_background_color())],
            [sg.Text('All classes',expand_x= True,justification = 'center'),sg.Text('Unavailible classes',expand_x= True,justification = 'center')],
            [sg.Listbox(names, size=(10, 8), enable_events=True, key='-LIST-',expand_x=True,expand_y=True),sg.Listbox(names_sel, size=(10, 4), enable_events=True, key='-LISTSELECT-',expand_x=True,expand_y=True)],
            [sg.Button('Done',border_width=0,font='Calibri 10'),sg.Text('Click on class name to move it to unavalible and back')]]

    window = sg.Window('Select unavalible classes', layout,resizable=True,finalize=True)
    window.set_min_size((381,245))

    # Event Loop
    while True:
        event, values = window.read(timeout=10)
        if event in (sg.WIN_CLOSED, 'Exit'):                # always check for closed window
            break
        if values['-INPUT-'] != '':                         # if a keystroke entered in search field
            search = values['-INPUT-'].upper()
            new_values = [x for x in names if search in x]  # do the filtering
            window['-LIST-'].update(new_values)     # display in the listbox
        else:
            # display original unfiltered list
            window['-LIST-'].update(names)
        # if a list item is chosen
        if event == '-LIST-' and len(values['-LIST-']):
            names.remove(values['-LIST-'][0])
            names_sel.append(values['-LIST-'][0])
            window['-LIST-'].update(names)
            window['-LISTSELECT-'].update(names_sel)
            
        if event == '-LISTSELECT-' and len(values['-LISTSELECT-']):
            names.append(values['-LISTSELECT-'][0])
            names_sel.remove(values['-LISTSELECT-'][0])
            window['-LIST-'].update(names)
            window['-LISTSELECT-'].update(names_sel)
            
        if event == 'Help':
            sg.popup('This is the window to select unavalible classes \n\nusing this feature you can select one or more classes and teachers who have a period with them will be shown free in the main program')
            
        if event == 'Done':
            print(names_sel)
            break
        
            
      
    window.close()
    return(names_sel)
