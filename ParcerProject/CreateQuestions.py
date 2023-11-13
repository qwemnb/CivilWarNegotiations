import csv
import hashlib
import mysql.connector
import tools
from tools import logger



def AddQuestion(questionText):
    connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    cursor = connection.cursor()
    
    #hash each question and store that with the question text into the questions table
    questionHash = hashlib.sha256(questionText.encode('utf-8'))
        #ignore questions that have already been added to the list
    sqlInsertQuestion = '''INSERT IGNORE INTO questions (question_text,question_hash) values(%s,%s)'''
    cursor.execute(sqlInsertQuestion, (questionText,questionHash.hexdigest()))
    connection.commit()
    cursor.close()
    connection.close()
    return None


    
    
def ReadQuestions(filename):   
    with open('C:\\Users\\Julie\\Desktop\\HeatherData\\documents\\{csvfilename}'.format(csvfilename=filename), encoding='utf8', newline='') as csvfile:
            rawDataReader = csv.reader(csvfile)
            #skip header row
            next(rawDataReader)
            #insert each row into the raw_data table
            #each row consists of a question: line[0] and an answer: line [1]
            values = []
            for line in rawDataReader:
                questionTextToImport = ''.join(i for i in line[0] if i.isalnum())
                questionHash = hashlib.sha256(questionTextToImport.encode('utf-8'))
                values.append([questionTextToImport,questionHash.hexdigest(),line[0]])
    
    return values

def InsertQuestions(values):
    connection, cursor = tools.DatabaseConnection()
    
    sqlInsertQuestion = '''INSERT IGNORE INTO questions (question_text,question_hash,question_display_text) values(%s,%s,%s)'''
    cursor.executemany(sqlInsertQuestion, values)
    connection.commit()
    cursor.close()
    connection.close()
    return None
                
                


InsertQuestions(ReadQuestions("Myanmar_CPB_1948-1988.csv"))
            
