import tools
import mysql.connector

def GetMaxIdOfTable(tableName,connection,cursor):
    logger = tools.getLogger()
    maxIdsql = '''SELECT MAX(id) FROM  {table}'''. format(table = tableName)
    try:
        cursor.execute(maxIdsql)
        maxId = cursor.fetchone()
        if maxId[0] is None:
           return 0
        else:
            return maxId[0]
    except mysql.connector.Error as e:
        logger.error("Get Max Id {error}".format(error = e))
        return -1
    
def DataInsertCorrectly(tableName, idChange, dataLength, logger):
    if idChange == dataLength:
        logger.debug('{rowcount} rows inserted into {tablename} of {datalength} rows of data'.format(rowcount = idChange,tablename = tableName, datalength = dataLength))
        return True
    else:    
        logger.error('{rowcount} rows inserted into {tablename} of {datalength} rows of data. Data is being removed!'.format(rowcount = idChange,tablename = tableName, datalength = dataLength))   
        return False
    

def InsertChangesToGovernment (data):
    logger = tools.getLogger()
    tableToInsertInto = 'govt_changes_by_year'
    connection, cursor = tools.DatabaseConnection()
    #get largest rowid in table
    previousMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    if previousMaxId == -1: #this only happens if the table does not exist.
        logger.error("Unable to insert into {tablename}. TABLE DOES NOT EXIST").format(tablename=tableToInsertInto)
        return None
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, year_data)
              VALUES (%s,%s,%s,%s,%s)'''.format(tablename = tableToInsertInto)
    
    cursor.executemany(sql, data)
    
    connection.commit()
    
    #get the new largest row in table
    #the difference between the previous max id and new max id should equal the rows in the data
    newMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    if DataInsertCorrectly(tableToInsertInto, newMaxId-previousMaxId, len(data), logger):
        connection.commit()
    else:
        connection.rollback()
    
    cursor.close()
    connection.close()
    return None

def InsertNegotiationsSuggested (data):
    logger = tools.getLogger()
    tableToInsertInto = 'negotiations_suggested'
    connection, cursor = tools.DatabaseConnection()
    #get largest row in table
    previousMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    if previousMaxId == -1: #this only happens if the table does not exist.
        logger.error("Unable to insert into {tablename}. TABLE DOES NOT EXIST").format(tablename = tableToInsertInto)
        return None
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, year_data)
              VALUES (%s,%s,%s,%s,%s,%s)'''.format(tablename = tableToInsertInto)
    
    cursor.executemany(sql, data)
    newMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    #this returns true if the rows inserted match the number of rows in the data given to the function
    if DataInsertCorrectly(tableToInsertInto, newMaxId-previousMaxId, len(data), logger):
        connection.commit()
    #if the row counts do not match remove the inserted rows.
    else:
        connection.rollback()
    cursor.close()
    connection.close()
    return None