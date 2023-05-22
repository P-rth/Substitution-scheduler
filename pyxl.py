import openpyxl
import PySimpleGUI as sg




def pref_popup(scale_old = 2.3 , theme_old = 'SandyBeach'):
    scale_ = scale_old
    theme_ = theme_old
    layout = [
        [sg.Text('Scale :'),sg.Slider((5,50), orientation='h',default_value = scale_old*10,key = 'scale')],
        [sg.Text('Theme :'),sg.Combo(sg.theme_list(),default_value = theme_old,key = 'theme')],
        [sg.Button('Ok',border_width=0,font='Calibri 10'),sg.Push(),sg.Button('Preview themes',border_width=0,font='Calibri 10'),sg.Button('Defalt',border_width=0,font='Calibri 10')]
    ]

    window = sg.Window('Title', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        
        if event == 'Defalt':
            window['scale'].update(23)
            window['theme'].update('SandyBeach')
            
            
        if event == 'Ok':
            scale_ = values['scale']/10
            theme_ = values['theme']
            f = open("ss.config", "w")
            f.write(f'{scale_},{theme_}')
            f.close()
            window.close()
            
        if event == 'Preview themes':
            sg.theme_previewer(4,scrollable = True)
            

            
    window.close()
    return(scale_,theme_)


def test_data(data):
    for i in data[0]:
        for j in i:
                print(j)
        print('#####################')
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

def read_data(exel_file_path):
    data = []
    error = None
    dataframe = openpyxl.load_workbook(exel_file_path)
    for sheet in dataframe.worksheets:
    #    print(str(sheet)[12:-2])
        array = []
        cell = sheet['B4':'F11']
        try:
            teacher = sheet["A2"].value
            department = sheet["A1"].value
            department = department.split(':')[-1].strip()
        
            for i in cell:
                x = []
                for j in i:
                    j = j.value
                    if j:
                        j = j.replace(" ", "").upper()
                    x.append(j)
                array.append(x)
        
            array.append([teacher,department])
            data.append(array)
        except:
            error = 'Error while reading: \n\n'+str(sheet)[12:-2]+'\n of file '+exel_file_path+'\n\nPlease check the format'+'\n\n The program will exit now.'
        
    return(data,error)

    
    window.close()
    for i in exec_class:
        if i.strip().isalnum():
            k = exec_class.index(i)
            exec_class[k] = exec_class[k].upper().strip()
        elif i.strip() == '' or i == 'UNAVBL CLS':
            continue
        else:
            sg.popup_error(f'Unavailable class "{i}" is not in correct format \n\n correct format : 9A,5b,6c... \n (class names seprated by commas - not case sensitive)')
            break
    return(exec_class)


def is_free(data,prd,day,dep_req,exec_class = []):
    out = []
    out_busy = []
    exec_class = exec_class
        
            
    for array in data:
        class_sel = array[prd-1][day]
        if class_sel:
            class_sel = class_sel.upper()
        teacher = array[-1][0]
        department = array[-1][1]
        if array[prd-1][day] == None:
            if dep_req == department or dep_req == 'All':
                out.append(teacher)
        else:
            if dep_req != 'All':
                if dep_req == department:
                    if class_sel not in exec_class:
                        out_busy.append(str(teacher+' - Busy with '+class_sel))
                    else:
                        out.append(f'{teacher}: {class_sel} unavailable')
            else:
                if class_sel not in exec_class:
                        out_busy.append(str(teacher+' - Busy with '+class_sel))
                else:
                        out.append(f'{teacher}: {class_sel} unavailable')
                
    return(out,out_busy)

def find_departments(data):
    out = []
    for array in data:
        if not array[-1][1] in out:
            out.append(array[-1][1])
    return(out)
    
def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])
    
    
def find_free_periods_num(data,day,teacher,exec_class=[]):
    tt = []
    counter = 0
    for i in data:
        if i[-1][0] == teacher:        #last row of data , first coulm (name)
            for j in i[0:-1]:           #to remove name from the timetable while looking for free prd
                if j[day] not in exec_class:
                    tt.append(j[day])
                else:
                    tt.append(strike(f'{j[day]} '))
            break
    for i in tt:
        if i == None or i in exec_class:
            counter += 1
    return(counter,tt)
            


import re                                                                           #
def natural_sort(l):                                                                 #
    convert = lambda text: int(text) if text.isdigit() else text.lower()             # Natural sort function
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]       # idk how but it just works
    return sorted(l, key=alphanum_key)                                               # https://t.ly/JLUU stackoverflow copied code
                                                                                    #

def find_classes(data):
    cls_found = []              # to look at output not error
    for i in data:
        for j in i[0:-1]:
            for k in j:      #to remove name from the timetable
                if k != None:
                    if k not in cls_found:               # to add only if not already present
                        cls_found.append(k)

    return(natural_sort(cls_found))


