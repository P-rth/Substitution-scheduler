import openpyxl

def read_data(exel_file_path):
    data = []
    error = None
    dataframe = openpyxl.load_workbook(exel_file_path)
    for sheet in dataframe.worksheets:
    #    print(str(sheet)[12:-2])
        array = []
        cell = sheet['A1':'E8']
        try:
            teacher,department = str(sheet)[12:-2].split(',')
            teacher = teacher.strip()
            department = department.strip().lower()
        
            for i in cell:
                x = []
                for j in i:
                    x.append(j.value)
                array.append(x)
        
            array.append([teacher,department])
            data.append(array)
        except:
            error = 'Error there is no Department mentioned in the sheet title : \n\n'+str(sheet)[12:-2]+'\n of file '+exel_file_path+'\n\n The correct way to title : teacher_name,Department'+'\n\n The program will exit now.'
        
    return(data,error)

def is_free(data,prd,day,dep_req):
    out = []
    out_busy = []
    for array in data:
        teacher = array[-1][0]
        department = array[-1][1]
        if array[prd-1][day-1] == None:
            if dep_req == department or dep_req == 'ANY':
                out.append(teacher)
        else:
            if dep_req != 'ANY':
                if dep_req == department:
                    out_busy.append(str(teacher+' Busy with '+array[prd-1][day-1]))
            else:
                out_busy.append(str(teacher+' Busy with '+array[prd-1][day-1]))
                
    return(out,out_busy)

def find_departments(data):
    out = []
    for array in data:
        if not array[-1][1] in out:
            out.append(array[-1][1])
    return(out)
    
        
    
#for i in data:
#    for j in i:
#            print(j)
#    print('#####################')

#data = read_data('Book1.xlsx')           
#is_free(data,4,5,'sports')
