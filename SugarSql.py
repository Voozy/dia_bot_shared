import sqlite3

conn =  sqlite3.connect("Sugar.db", check_same_thread= False)
cursor = conn.cursor()


def SugarInsert(user_id, date, time, sugar, insulin, he):

    # Функция для добавление записи в таблицу
    sql_i = "insert into blood_stat values ((select max(seq) from seq_no)+1, ?, ?, ?, ?, ?, ?)  "
    cursor.execute(sql_i, (user_id, date, time, sugar, insulin, he))
    conn.commit()

    # Увеличиваем счетчик на 1. В принципе он не сильно нужен, но в дальнейшем для сбора статистики
    # либо для написания хитрых селектов, упрощения сортировки может пригодиться
    sql_u = "update seq_no set seq = seq + 1"
    cursor.execute(sql_u)
    conn.commit()

def SugarSelect(user_id):
    sql_s = "select * from blood_stat where user_id =" + str(user_id) + " order by seq"
    cursor.execute(sql_s)
#   return cursor.fetchall()
    file = open(str(user_id) + '.txt', 'w', encoding='utf-8-sig')
    file.write('+-----------+---------+---------+---------+---------+' + '\n')
    file.write('|' + '   DATE    ' + '|' + '  TIME   ' + '|' + ' BLOOD   ' + '|' + ' INSULIN ' + '|' + ' CARB    ' + '|'+ '\n')
    for a in cursor.fetchall():
        file.write('+-----------+---------+---------+---------+---------+' + '\n')
        file.write('|' + str(a[2]).rjust(10, ' ') + ' |' + str( a[3]).rjust(8, ' ') + ' |' + str( a[4]).rjust(8, ' ') + ' |'+ str( a[5]).rjust(8, ' ') + ' |' + str( a[6]).rjust(8, ' ') + ' |' '\n')
    file.write('+-----------+---------+---------+---------+---------+' + '\n')




def Report():
    file = open('test.txt', 'w')
    file.write('+-----+--------------+---------+----------+' + '\n')
    file.write('|' + 'seq' + '  |  ' + 'Date' + '        |  ' + 'Blood' + '  |  ' + 'Insulin'+' |'+ '\n')
    for a in SugarSelect():

        file.write('+-----+--------------+---------+----------+'+ '\n')
        file.write('|' + str(a[3]).rjust(4, ' ') + ' |' + str(a[0]).rjust(13, ' ') + ' |' + str(a[1]).rjust(8, ' ') + ' |'+ str( a[2]).rjust(8, ' ') + '  |' + '\n')
    file.write('+-----+--------------+---------+----------+'+ '\n')

def Last_input(user_id):
    sql_s = "select avg(sugar), date as avg_sugar from blood_stat where user_id = 347319738 group by date "
    cursor.execute(sql_s)
    print(cursor.fetchall())

    pass
