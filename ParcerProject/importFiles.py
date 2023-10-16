import mysql.connector
import csv
import os
import glob
import hashlib
from logger import getLogger


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
    logger = getLogger()
    def RemoveFileFromFilesTable(fileIdToRemove,fileNameToRemove):
        #check that the id given is for the correct filename
        sqlCheckFile = '''SELECT id FROM files WHERE file_name = "{filenametoremove}"'''.format(filenametoremove = fileNameToRemove)
        cursor.execute(sqlCheckFile)
        
        logger.debug("Executing: {sql}".format(sql = sqlCheckFile ))
        
        databaseFileId = cursor.fetchone()[0]
        
        logger.info("Database File Id: {dbfileid} compared to File Id given in function {fileidtoberemoved}".format(dbfileid = databaseFileId, fileidtoberemoved = fileIdToRemove))
        if (databaseFileId == fileIdToRemove): # if the filename returns the correct file id
            sqlRemoveFileImported = ('''DELETE FROM files WHERE id = {fileidtoremove}'''.format(fileidtoremove = fileIdToRemove))
            cursor.execute(sqlRemoveFileImported)
            
            logger.debug("Executing: {sql}".format(sql = sqlRemoveFileImported))
            
            connection.commit()
            logger.error("Successfully removed FileId:{fileidtoremove} FileName:{filenametoremove}".format(fileidtoremove = fileIdToRemove, filenametoremove = fileNameToRemove))
        else: #if the fileid in the database does not match the given fileid
            logger.error("There was an issue removing FileId:{fileidtoremove} FileName:{filenametoremove]".format(fileidtoremove = fileIdToRemove, filenametoremove = filename))
        return None
        
        
      
    connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    cursor = connection.cursor()

    
    
    filename = fileToBeImported
    
    logger.debug("Starting to process file: {csvfilename}".format(csvfilename = filename))
    
    #Check that the file has not already been imported
    sqlCheckFile = '''SELECT COUNT(*) FROM files WHERE file_name = "{csvfilename}"'''.format(csvfilename = filename)

    cursor.execute(sqlCheckFile)
    fileNameCount = cursor.fetchone()[0]
    
    logger.debug("File Name Count: {count}".format(count = fileNameCount))
    
    if (fileNameCount == 0):
        #add file to list of imported files    
        sqlFileNameInsert = '''INSERT INTO files (file_name) VALUES("{csvfilename}")'''.format(csvfilename = filename)
        
        logger.debug("Executing: {sql}".format(sql = sqlFileNameInsert))
        logger.info("inserting into csvfilename: {sql}".format(sql = sqlFileNameInsert))
        
        cursor.execute(sqlFileNameInsert)
        connection.commit()
        
        
        #retrieve id created for the file being imported
        sqlFileIdSelect = '''SELECT id from files WHERE file_name = "{csvfilename}"'''.format(csvfilename = filename)
        cursor.execute(sqlFileIdSelect)
        
        logger.debug("Executing: {sql}".format(sql = sqlFileIdSelect))
        
        fileId = cursor.fetchone()[0]
        #open csv document
        with open('C:\\Users\\Julie\\Desktop\\HeatherData\\documents\\{csvfilename}'.format(csvfilename=filename), encoding='utf8', newline='') as csvfile:
            rawDataReader = csv.reader(csvfile)
            #skip header row
            next(rawDataReader)
            #insert each row into the raw_data table
            #each row consists of a question: line[0] and an answer: line [1]
            values = []
            dataFileRowCount = 0
            questionErrors = 0
            for line in rawDataReader:
                #create a list of each question/ answer pair with the corresponding file id.
                #hash question to verify each question is the correct value
                questionHash = hashlib.sha256(line[0].encode('utf-8'))
                
                sqlHashCheck = '''SELECT COUNT(*) FROM questions WHERE question_hash = "{hash}"'''.format(hash = questionHash.hexdigest())
                logger.debug("Executing: {sql}".format(sql = sqlHashCheck))
                cursor.execute(sqlHashCheck)
                questionHashCount = cursor.fetchone()[0]
                
                logger.debug("Question Hash Count: {count}".format(count = questionHashCount))
                
                if questionHashCount == 1: #question exists once in questions table
                    values.append((fileId,line[0],line[1]))
                    dataFileRowCount += 1
                else:
                    questionErrors += 1
                    if questionHashCount == 0: #question does not exist in questions table
                        logger.error("Question is not formatted correctly in FileId:{fileid} FileName:{csvfilename} \n INVALID QUESTION: \n {questiontext}".format(fileid = fileId, csvfilename = filename, questiontext = line[0]))

                    else: # Question exists more than once in the questions table
                        logger.error("ERROR IN QUESTIONS TABLE!!! DUPICATE DATA")
            if questionErrors > 0:
                RemoveFileFromFilesTable(fileId,filename)
                logger.error("Finished Processing {csvfilename} in ERROR".format(csvfilename = filename))
                cursor.close()
                connection.close()
                return None



            sqlInsertRawData = '''INSERT INTO raw_data (file_id,question,answer) VALUES (%s,%s,%s)'''
            cursor.executemany(sqlInsertRawData, values)
            logger.debug("Inserting into raw data for file {csvfilename}".format(csvfilename = filename))
        connection.commit()
        #Check that the number of row inserted matches the rows in the file.
        #count rows inserted for the fileid
        sqlRowCount = '''SELECT COUNT(*) FROM raw_data WHERE file_id = {csvfileid}'''.format(csvfileid = fileId)
        cursor.execute(sqlRowCount)
        insertedRowCount = cursor.fetchone()[0]
        
        #if the row counts match log the info
        if (dataFileRowCount == insertedRowCount):
            logger.info("{rowcount} rows inserted into raw_data from fileId {csvfileid} ({csvfilename})".format(rowcount = insertedRowCount, csvfileid = fileId, csvfilename = filename))
            logger.debug("Finished Processing {csvfilename} with SUCCESS".format(csvfilename = filename))
        #if the row counts do not match log error message
        else:
            logger.error("File contains {csvrowcount} lines. {insertedrowcount} in raw_data table for fileId {csvfileid} ({csvfilename}) ".format(csvrowcount = dataFileRowCount, insertedrowcount = insertedRowCount, csvfileid = fileId, csvfilename = filename))
    else:
        logger.warning("File {csvfilename} Already Imported".format(csvfilename = filename))
        logger.debug("Finished Processing {csvfilename} Already Imported".format(csvfilename = filename))
    cursor.close()
    connection.close()
    return None
ImportFile('Myanmar_CPB_1948-1988.csv')
#ImportFile('BadQuestion.csv')
#print(GetFileList('C:\\Users\\Julie\\Desktop\\HeatherData\\documents\\'))

#CreateQuestionList()