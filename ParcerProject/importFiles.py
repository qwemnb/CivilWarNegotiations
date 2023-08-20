import mysql.connector
import csv
import os
import glob
import hashlib

#pull list of csv files in the given directory
def GetFileList(directory):
    path = directory

    extension = 'csv'
    os.chdir(path)
    csvList = glob.glob('*.{}'.format(extension))
    return csvList

#create the questions key table with hashes of each question.
def CreateQuestionList():
    connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    cursor = connection.cursor()
    
    #get list of questions from raw data input
    sqlQuestionList = '''SELECT DISTINCT question from raw_data'''
    cursor.execute(sqlQuestionList)
    questions = cursor.fetchall()
    #hash each question and store that with the question text into the questions table
    for question in questions:
        questionHash = hashlib.sha256(question[0].encode('utf-8'))
        #ignore questions that have already been added to the list
        sqlInsertQuestion = '''INSERT IGNORE INTO questions (question_text,question_hash) values(%s,%s)'''
        cursor.execute(sqlInsertQuestion, (question[0],questionHash.hexdigest()))
    connection.commit()
    cursor.close()
    connection.close()
    return None   

def ImportFile(fileToBeImported):    
    connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    cursor = connection.cursor()
    
    
    filename = fileToBeImported
    
    #Check that the file has not already been imported
    sqlCheckFile = '''SELECT COUNT(*) FROM files WHERE file_name = "{csvfilename}"'''.format(csvfilename = filename)

    cursor.execute(sqlCheckFile)
    fileNameCount = cursor.fetchone()
    
    if (fileNameCount[0] == 0):
        #add file to list of imported files    
        sqlFileNameInsert = '''INSERT INTO files (file_name) VALUES("{csvfilename}")'''.format(csvfilename = filename)
        print(sqlFileNameInsert)
        cursor.execute(sqlFileNameInsert)
        connection.commit()
        
        #retrieve id created for the file being imported
        sqlFileIdSelect = '''SELECT id from files WHERE file_name = "{csvfilename}"'''.format(csvfilename = filename)
        cursor.execute(sqlFileIdSelect)
        fileId = cursor.fetchone()[0]
        #open csv document
        with open('C:\\Users\\Julie\\Desktop\\HeatherData\\documents\\{csvfilename}'.format(csvfilename=filename), encoding='utf8', newline='') as csvfile:
            rawDataReader = csv.reader(csvfile)
            #skip header
            next(rawDataReader)
            #insert each row into the raw_data table
            values = []
            for line in rawDataReader:
                values.append((fileId,line[0],line[1]))
            sql = '''INSERT INTO raw_data (file_id,question,answer) VALUES (%s,%s,%s)'''
            cursor.executemany(sql, values)
        connection.commit()
    else:
        print("File Already Imported")
        #sqlRowCount = '''SELECT COUNT(*) FROM raw_data'''
        #print (cursor.execute(sqlRowCount))
    cursor.close()
    connection.close()
    return None
#ImportFile('TestData2.csv')

#print(GetFileList('C:\\Users\\Julie\\Desktop\\HeatherData\\documents\\'))

#CreateQuestionList()