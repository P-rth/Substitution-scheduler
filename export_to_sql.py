import mysql.connector
from pyxl import *



def exportsql(connector_info,file_path):
    try:
        mydb = mysql.connector.connect(**connector_info)

        cursor = mydb.cursor()
        cursor.execute('DROP DATABASE IF EXISTS ssa_db;')
        cursor.execute(f"CREATE DATABASE ssa_db")
        cursor.execute(f"USE ssa_db")

        create_time_table_query = '''
        CREATE TABLE time_table(
            name VARCHAR(255) NOT NULL,
            day INT NOT NULL CHECK (day >= 0 AND day <= 4),
            prd1 VARCHAR(255) ,
            prd2 VARCHAR(255) ,
            prd3 VARCHAR(255) ,
            prd4 VARCHAR(255) ,
            prd5 VARCHAR(255) ,
            prd6 VARCHAR(255) ,
            prd7 VARCHAR(255) ,
            prd8 VARCHAR(255) ,
            PRIMARY KEY (name, day));
        '''
        cursor.execute(create_time_table_query)
        mydb.commit()

        create_teacher_data_query = '''
        CREATE TABLE teacher_data(
            name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
            departmet VARCHAR(255) NOT NULL
        );
        '''

        cursor.execute(create_teacher_data_query)
        mydb.commit()

        data = read_data(file_path)[0]
        all_teachers = find_teach(data)


        sql_data = []
        for teach in all_teachers :
            for day in range(0,5):
                sql_temp = [teach,day] + find_free_periods_num(data,day,teach)[1]
                sql_data.append(sql_temp)

        teach_data_dept = find_departments(data,withteach=True)

        sql_com = "INSERT INTO time_table VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

        sql_com_data = "INSERT INTO teacher_data VALUES (%s,%s);"

        cursor.executemany(sql_com, sql_data)
        cursor.executemany(sql_com_data, teach_data_dept)

        mydb.commit()

        return [cursor.rowcount]

        cursor.close()
        mydb.close()

    except Exception as e:
        return ['Error',e]