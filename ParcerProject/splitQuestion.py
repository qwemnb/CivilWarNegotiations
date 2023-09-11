import mysql.connector
import collections
import re

def DatabaseConnection():
    connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    cursor = connection.cursor()
    
    return connection, cursor

def CheckQuestionExists ():
    pass

def CheckMonth(line):
    
    lineToCheck = line.lower()
    
    if 'jan' in lineToCheck or 'january' in lineToCheck:
        return 1
    if 'feb' in lineToCheck or 'february' in lineToCheck:
        return 2
    if 'mar' in lineToCheck or 'march' in lineToCheck:
        return 3
    if 'apr' in lineToCheck or 'april' in lineToCheck:
        return 4
    if 'may' in lineToCheck:
        return 5
    if 'jun' in lineToCheck or 'june' in lineToCheck:
        return 6
    if 'jul' in lineToCheck or 'july' in lineToCheck:
        return 7
    if 'aug' in lineToCheck or 'august' in lineToCheck:
        return 8
    if 'sept' in lineToCheck or 'september' in lineToCheck:
        return 9
    if 'oct' in lineToCheck or 'october' in lineToCheck:
        return 10
    if 'nov' in lineToCheck or 'november' in lineToCheck:
        return 11
    if 'dec' in lineToCheck or 'december' in lineToCheck:
        return 12
    else:
        return None
                
    

def SplitQuestion8 ():
    rawData = collections.namedtuple('rawData', ['raw_data_id', 'file_id', 'question_id', 'answer'])
    
    #connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    #cursor = connection.cursor()
    connection, cursor = DatabaseConnection()
    
    
    
    sql = '''SELECT rd.id, rd.file_id, q.id, rd.answer 
                    FROM raw_data rd 
                    JOIN questions q ON rd.question = q.question_text
                    WHERE q.question_text LIKE "Were there any changes in government during the conflict%"'''

    cursor.execute(sql)
    rawData = cursor.fetchall()
    #pull data from select statement into rawData namedtuple
    for row in cursor:
        rawData.append(row[0],row[1],row[2],row[3])
        
    splitData =  []
    year = ''
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            #find years between 1940 and 2016. the range of the current data sets
            if re.match(r'.*([19][40-99]{2})', line[0:4]) is not None or re.match(r'.*([20][00-16]{2})', line[0:4]) is not None:
                year = line
            if year != line:
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, line ))
      

    cursor.close()
    connection.close()
    Insert_govt_changes_by_year_Data(splitData)
    return splitData

def Insert_govt_changes_by_year_Data (data):
    #connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    #cursor = connection.cursor()
    connection, cursor = DatabaseConnection()
    maxIdsql = '''SELECT MAX(id) FROM  govt_changes_by_year'''
    cursor.execute(maxIdsql)
    previousMaxId = cursor.fetchone()
    previousMaxIdInt = 0
    if previousMaxId[0] is None:
        previousMaxIdInt = 0
    else:
        previousMaxIdInt = previousMaxId[0]
    sql = '''INSERT INTO govt_changes_by_year (raw_data_id, file_id, question_id, answer_year, year_data)
              VALUES (%s,%s,%s,%s,%s)'''
    
    cursor.executemany(sql, data)
    
    connection.commit()
    cursor.execute(maxIdsql)
    maxId =  cursor.fetchone()
    maxIdInt = maxId[0]
    
    print('{rowCount} rows inserted of {dataLength}'.format(rowCount = maxIdInt - previousMaxIdInt, dataLength = len(data)) )
    

    cursor.close()
    connection.close()
    return None

def SplitQuestion11 ():
    #connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    #cursor = connection.cursor()
    connection, cursor = DatabaseConnection()
    ##Selecting all rows for "negotiations suggested" question from the raw data input
    sql = '''SELECT rd.id, rd.file_id, q.id, rd.answer 
                    FROM raw_data rd 
                    JOIN questions q ON rd.question = q.question_text
                    WHERE q.question_text LIKE "Were negotiations suggested?%"'''
    cursor.execute(sql)
    rawData = cursor.fetchall()

    splitData =  []
    year = ''
    month = ''
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines() 
        for line in splitanswer:
            #find years between 1940 and 2016. the range of the current data sets
            if re.match(r'.*([19][40-99]{2})', line[0:4]) is not None:
                year = line.lstrip()[0:4]
                month = CheckMonth(line)
                # split data contains id of raw data line, file id, question id, year month and each lines text

            elif re.match(r'.*([20][00-16]{2})', line[0:4]) is not None:
                year = line.lstrip()[0:4]
                month = CheckMonth(line)
            splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, line ))        

    
    
    cursor.close()
    connection.close()
    return(splitData)
    
#SplitQuestion8 ()
#print(SplitQuestion11())
