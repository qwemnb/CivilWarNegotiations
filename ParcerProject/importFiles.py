import mysql.connector
import csv
import os
import glob
import hashlib
import tools
from tools import logger

#pull list of csv files in the given directory
def GetFileList(directory):
    path = directory

    extension = 'csv'
    os.chdir(path)
    csvList = glob.glob('*.{}'.format(extension))
    return csvList

#Run ImportFile for each filename in the given list
def ImportFileList(fileNames):
    #iterate through list of filenames
    for fileName in fileNames:
        logger.info('''\n\n************STARTING IMPORT OF {filename}************\n\n'''.format(filename = fileName))
        ImportFile(fileName)
    return None

def GetQuestionID(questionText):
    connection, cursor = tools.DatabaseConnection()
    sqlSelectQuestionId = '''SELECT id FROM questions where question_text = "{questiontext}"'''.format(questiontext = questionText)
    cursor.execute(sqlSelectQuestionId)
    questionId = cursor.fetchone()
    if questionId is None:
        logger.error("Duplicate Question in Question Table:\n{questiontext}").format(questiontext = questionText)
        cursor.close()
        connection.close()
        return None
    else:
        cursor.close()
        connection.close()
        return questionId[0]
   
   
    
        
    

def ImportFile(fileToBeImported):
    def RemoveFileFromFilesTable(fileIdToRemove,fileNameToRemove):
        #check that the id given is for the correct filename
        sqlCheckFile = '''SELECT id FROM files WHERE file_name = "{filenametoremove}"'''.format(filenametoremove = fileNameToRemove)
        cursor.execute(sqlCheckFile)
        
        logger.debug("Executing: {sql}".format(sql = sqlCheckFile ))
        
        databaseFileId = cursor.fetchone()[0]
        
        logger.debug("Database File Id: {dbfileid} compared to File Id given in function {fileidtoberemoved}".format(dbfileid = databaseFileId, fileidtoberemoved = fileIdToRemove))
        if (databaseFileId == fileIdToRemove): # if the filename returns the correct file id
            sqlRemoveFileImported = ('''DELETE FROM files WHERE id = {fileidtoremove}'''.format(fileidtoremove = fileIdToRemove))
            cursor.execute(sqlRemoveFileImported)
            
            logger.debug("Executing: {sql}".format(sql = sqlRemoveFileImported))
            
            connection.commit()
            logger.error("Successfully removed FileId:{fileidtoremove} FileName:{filenametoremove}".format(fileidtoremove = fileIdToRemove, filenametoremove = fileNameToRemove))
        else: #if the fileid in the database does not match the given fileid
            logger.error("There was an issue, removing FileId:{fileidtoremove} FileName:{filenametoremove]".format(fileidtoremove = fileIdToRemove, filenametoremove = filename))
        return None
        
        
      
    
    connection, cursor = tools.DatabaseConnection()

    
    
    filename = fileToBeImported
    
    #logger.info("Starting to process file: {csvfilename}".format(csvfilename = filename))
    
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
                formatedQuestionText = ''.join(i for i in line[0] if i.isalnum())
                questionId = GetQuestionID(formatedQuestionText)
                questionHash = hashlib.sha256(formatedQuestionText.encode('utf-8'))
                
                sqlHashCheck = '''SELECT COUNT(*) FROM questions WHERE question_hash = "{hash}"'''.format(hash = questionHash.hexdigest())
                logger.debug("Executing: {sql}".format(sql = sqlHashCheck))
                cursor.execute(sqlHashCheck)
                questionHashCount = cursor.fetchone()[0]
                
                logger.debug("Question Hash Count: {count}".format(count = questionHashCount))
                
                if questionHashCount == 1: #question exists once in questions table
                    values.append((fileId,questionId,line[1]))
                    dataFileRowCount += 1
                else:
                    questionErrors += 1
                    if questionHashCount == 0: #question does not exist in questions table
                        logger.error("Question is not formatted correctly in FileId:{fileid} FileName:{csvfilename} \n INVALID QUESTION: \n {questiontext}".format(fileid = fileId, csvfilename = filename, questiontext = line[0]))

                    else: # Question exists more than once in the questions table
                        logger.error("ERROR IN QUESTIONS TABLE!!! DUPICATE DATA")
            if questionErrors > 0:
                RemoveFileFromFilesTable(fileId,filename)
                logger.error("\n\n************Finished Processing {csvfilename} in ERROR************\n\n".format(csvfilename = filename))
                cursor.close()
                connection.close()
                return None


            
            sqlInsertRawData = '''INSERT INTO raw_data (file_id,question_id,answer) VALUES (%s,%s,%s)'''
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
            logger.info("\n\n************Finished Processing {csvfilename} with SUCCESS************".format(csvfilename = filename))
        #if the row counts do not match log error message
        else:
            logger.error("File contains {csvrowcount} lines. {insertedrowcount} in raw_data table for fileId {csvfileid} ({csvfilename}) ".format(csvrowcount = dataFileRowCount, insertedrowcount = insertedRowCount, csvfileid = fileId, csvfilename = filename))
    else:
        logger.warning("File {csvfilename} Already Imported".format(csvfilename = filename))
        logger.info('''\n\n************Finished Processing {csvfilename} Already Imported************'''.format(csvfilename = filename))
    cursor.close()
    connection.close()
    return None

#ImportFile('Myanmar_MujahidParty_1948-1961.csv')
#ImportFile('BadQuestion.csv')
ImportFileList((GetFileList('C:\\Users\\Julie\\Desktop\\HeatherData\\documents\\')))
