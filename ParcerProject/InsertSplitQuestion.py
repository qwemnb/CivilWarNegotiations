import tools
import mysql.connector
from tools import logger


def GetMaxIdOfTable(tableName,connection,cursor):
    maxIdsql = '''SELECT MAX(id) FROM  {table}'''. format(table = tableName)
    try:
        cursor.execute(maxIdsql)
        maxId = cursor.fetchone()
        if maxId[0] is None: #if there are no rows in the table
           return 0
        else:
            return maxId[0]
    except mysql.connector.Error as e:
        logger.error("Get Max Id {error}".format(error = e))
        return -1
    
def DataInsertedCorrectly(tableName, idChange, dataLength):
    if idChange == dataLength:
        logger.debug('{rowcount} rows inserted into {tablename} of {datalength} rows of data'.format(rowcount = idChange,tablename = tableName, datalength = dataLength))
        return True
    else:
        logger.error('{rowcount} rows inserted into {tablename} of {datalength} rows of data. Data is being removed!'.format(rowcount = idChange,tablename = tableName, datalength = dataLength))   
        return False
    

def DataInsertedCorrectlyTest(tableName, idChange, dataLength):
    if idChange == dataLength:
        print('{rowcount} rows inserted into {tablename} of {datalength} rows of data'.format(rowcount = idChange,tablename = tableName, datalength = dataLength))
        return True
    else:    
        print('{rowcount} rows inserted into {tablename} of {datalength} rows of data. Data is being removed!'.format(rowcount = idChange,tablename = tableName, datalength = dataLength))   
        return False


def InsertRebelGroupsFightingByYear (data):
    pass

def InsertChangesToGovernment (data):
    tableToInsertInto = 'split_govt_changes_by_year'
    connection, cursor = tools.DatabaseConnection()
    #get largest rowid in table
    previousMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    if previousMaxId == -1: #this only happens if the table does not exist.
        logger.error("Unable to insert into {tablename}. TABLE DOES NOT EXIST").format(tablename=tableToInsertInto)
        return None
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, line_data)
              VALUES (%s,%s,%s,%s,%s)'''.format(tablename = tableToInsertInto)
    
    cursor.executemany(sql, data)
    
    connection.commit()
    
    #get the new largest row in table
    #the difference between the previous max id and new max id should equal the rows in the data
    newMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    if DataInsertedCorrectly(tableToInsertInto, newMaxId-previousMaxId, len(data)):
        connection.commit()
    else:
        connection.rollback()
    
    cursor.close()
    connection.close()
    return None

def InsertCeasefireDeclared (data):
    pass

def InsertOfferInducements (data):
    pass

def InsertNegotiationsSuggested (data):
    tableToInsertInto = 'split_negotiations_suggested'
    connection, cursor = tools.DatabaseConnection()
    #get largest row in table
    previousMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    if previousMaxId == -1: #this only happens if the table does not exist.
        logger.error("Unable to insert into {tablename}. TABLE DOES NOT EXIST").format(tablename = tableToInsertInto)
        return None
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, line_data)
              VALUES (%s,%s,%s,%s,%s,%s)'''.format(tablename = tableToInsertInto)
    
    cursor.executemany(sql, data)
    newMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    #this returns true if the rows inserted match the number of rows in the data given to the function
    if DataInsertedCorrectly(tableToInsertInto, newMaxId-previousMaxId, len(data)):
        connection.commit()
    #if the row counts do not match remove the inserted rows.
    else:
        connection.rollback()
    cursor.close()
    connection.close()
    return None

def InsertOneOrBothRefuseNegotiate (data):
    pass

def InsertContentOfNegotiations (data):
    pass

def InsertEndWithoutSigning (data):
    pass

def InsertWasAgreementSigned (data):
    pass

def InsertAgreementEndFighting (data):
    pass

def InsertReachedNotSigned (data):
    pass

def InsertUnsignedEndFighting (data):
    pass

def InsertOutsideOfferMediation  (data):
    pass

def InsertDidMediationOccur (data):
    pass

def InsertWasUNInvolved (data):
    pass

def InsertWereIGOInvolved (data):
    pass

def InsertThirdPartyIntervene (data):
    pass

def InsertDidGovernmentRecieveAid (data):
    pass

def InsertDidRebelsRecieveAid (data):
    pass

def InsertDidConflictRecur (data):
    pass