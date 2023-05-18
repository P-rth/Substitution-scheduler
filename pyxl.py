import openpyxl
import PySimpleGUI as sg

def popup_table(list_in,name,day):
    list = []
    for i in list_in:
        if i == None:
            list.append('-')
        else:
            list.append(i)
    layout = [[sg.Text(name)],[sg.Text(day)],
        [sg.Table([[1,list[0]], 
                   [2,list[1]],
                   [3,list[2]],
                   [4,list[3]],
                   [5,list[4]],
                   [6,list[5]],
                   [7,list[6]],
                   [8,list[7]],], 
                  ['Period','Class'], num_rows=2,expand_x=True,expand_y=True,hide_vertical_scroll=True,justification = "center",row_height=28)],
        [sg.Button('Ok')]
    ]
    sg.theme('SandyBeach')
    window = sg.Window('Title', layout,margins=(0,0),element_padding=(0,0),size = (250,360),element_justification='Center')
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED,'Ok'):
            break
    
    window.close()


def test_data(data):
    for i in data:
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
            error = 'Error there is no Department mentioned in the sheet title : \n\n'+str(sheet)[12:-2]+'\n of file '+exel_file_path+'\n\n The correct way to title : teacher_name,Department'+'\n\n The program will exit now.'
        
    return(data,error)

def exec_class_fix(exec_class):
    exec_class = exec_class.split(',')
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


def is_free(data,prd,day,dep_req,exec_class = ''):
    out = []
    out_busy = []
    exec_class = exec_class_fix(exec_class)
        
            
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
    
    
def find_free_periods_num(data,day,teacher,exec_class=''):
    exec_class = exec_class_fix(exec_class)
    tt = []
    counter = 0
    for i in data:
        if i[-1][0] == teacher:        #last row of data , first coulm (name)
            for j in i[0:-1]:           #to remove name from the timetable while looking for free prd
                tt.append(j[day])
            break
    for i in tt:
        if i == None or i in exec_class:
            counter += 1
    return(counter,tt)
            
     

    




#data = read_data('Book1.xlsx')           
#is_free(data,4,5,'sports')
