from pyxl import rotate,test_data
import mysql.connector


def read_data_from_sql(connector_info):
  try:
    mydb = mysql.connector.connect(**connector_info)

    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM time_table")
    myresult = cursor.fetchall()

    names_ = set()
    for i in myresult:
        names_.add(i[0])

    out = []

    for i in names_:
      _ = []
      cursor.execute(f'SELECT * FROM time_table WHERE name = "{i}" ORDER BY day;')
      t_t_raw = cursor.fetchall()
      
      cursor.execute(f'SELECT * FROM teacher_data WHERE name = "{i}";')
      t_d_raw = cursor.fetchall()

      for j in t_t_raw:
            _.append(j[2:])
      _ = rotate(_)
      _.append(list(t_d_raw[0]))
      out.append(_)
    # test_data(_,chunk=True)

    return out

  except Exception as e:
    return ['Error',e]

'''
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ssa_db'
}

out = read_data_from_sql(db_config)

'''