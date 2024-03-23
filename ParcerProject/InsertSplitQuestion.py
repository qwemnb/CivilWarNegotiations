import tools
import mysql.connector
from tools import logger

def TruncateTable (tableName,connection,cursor):
    truncteSQL = '''TRUNCATE heather.{tablename}'''.format(tablename = tableName)
    try:
        cursor.execute(truncteSQL)
        return True
    except mysql.connector.Error as e:
        logger.error("{sql}: {error}".format(sql = truncteSQL, error = e))
        return False
        

def GetMaxIdOfTable(tableName,connection,cursor):
    maxIdsql = '''SELECT MAX(id) FROM  {table}'''. format(table = tableName)
    try:
        cursor.execute(maxIdsql)
        maxId = cursor.fetchone()
        if maxId[0] is None: #if there are no rows in the table
            logger.debug("No Rows in table [tablename]".format(tablename = tableName))
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


#This takes the table name for the split question data and the sql statement and the split data from the split question table.
#sqlInsertStatement must look like below. Except the column names and number of vaolues can be different.
#'''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, line_data)
#              VALUES (%s,%s,%s,%s,%s)'''
def InsertDataWithGivenSQLAndTable (tableName,sqlInsertStatement,data):
    wasDataInsertedCorrectly = None
    tableToInsertInto = tableName
    connection, cursor = tools.DatabaseConnection()
    
    
    TruncatedSuccessfully = TruncateTable(tableToInsertInto, connection, cursor)
    logger.debug("Truncate table {tablename} successful: {success}".format(tablename = tableToInsertInto, success = TruncatedSuccessfully))
    
    
    #get largest rowid in table
    previousMaxId = GetMaxIdOfTable(tableToInsertInto, connection, cursor)
    if previousMaxId == -1: #this only happens if the table does not exist.
        logger.error("Unable to insert into {tablename}. TABLE DOES NOT EXIST").format(tablename=tableToInsertInto)
        return False, tableName
    #adding table name to sql statement. This value is initially separate so that the table can be checked with the GetMaxIdOfTable.
    formattedSQL = sqlInsertStatement.format(tablename = tableToInsertInto)
    
    logger.debug("Running SQL: {sql}".format(sql = formattedSQL))
    cursor.executemany(formattedSQL, data)
    
    #get the new largest row in table
    #the difference between the previous max id and new max id should equal the rows in the data
    newMaxId = GetMaxIdOfTable(tableToInsertInto, connection,cursor)
    
    if DataInsertedCorrectly(tableToInsertInto, newMaxId-previousMaxId, len(data)):
        connection.commit()
        wasDataInsertedCorrectly = True
    else:
        connection.rollback()
        wasDataInsertedCorrectly = False
    cursor.close()
    connection.close()
    return wasDataInsertedCorrectly, tableName





def InsertRebelGroupsFightingByYear (data):
    tableToInsertInto = 'split_rebel_groups_by_year'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, rebel_aims, line_data)
              VALUES (%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)


def InsertChangesToGovernment (data):
    tableToInsertInto = 'split_govt_changes_by_year'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, line_data)
              VALUES (%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)



def InsertCeasefireDeclared (data):
    pass




def InsertOfferInducements (data):
    tableToInsertInto = 'split_offer_inducements'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, line_data)
              VALUES (%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertNegotiationsSuggested (data):
    tableToInsertInto = 'split_negotiations_suggested'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, line_data)
              VALUES (%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)
    

def InsertOneOrBothRefuseNegotiate (data):
    tableToInsertInto = 'split_negotiations_refused'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, refused_to_negotiate, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)


def InsertContentOfNegotiations (data):
    tableToInsertInto = 'split_content_of_negotiations'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, line_data)
              VALUES (%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertEndWithoutSigning (data):
    tableToInsertInto = 'split_end_without_signing'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, who_did_not_sign, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertWasAgreementSigned (data):
    tableToInsertInto = 'split_agreement_signed'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, agreement_signed, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertAgreementEndFighting (data):
    tableToInsertInto = 'split_agreement_end_fighting'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, end_fighting, line_data)
              VALUES (%s,%s,%s,%s,%s,%s, %s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertReachedNotSigned (data):
    tableToInsertInto = 'split_reached_not_signed'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, not_signed, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertUnsignedEndFighting (data):
    tableToInsertInto = 'split_unsigned_end_fighting'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, unsigned_end_fighting, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertOutsideOfferMediation  (data):
    tableToInsertInto = 'split_outside_offer_mediation'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, mediation_offered, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertDidMediationOccur (data):
    tableToInsertInto = 'split_mediation_occur'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_year, answer_month, did_mediation_occur, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertWasUNInvolved (data):
    tableToInsertInto = 'split_un_involved'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_start_year, answer_end_year, un_involved, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertWereIGOInvolved (data):
    tableToInsertInto = 'split_igo_involved'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_start_year, answer_end_year, igo_involved, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertThirdPartyIntervene (data):
    tableToInsertInto = 'split_third_party_intervene'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, group_type, did_third_party_intervene, answer_start_year, answer_end_year, intervention_type, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertDidGovernmentRecieveAid (data):
    tableToInsertInto = 'split_govt_receive_aid'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_start_year, answer_end_year, govt_receive_aid, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)

def InsertDidRebelsRecieveAid (data):
    tableToInsertInto = 'split_rebels_receive_aid'
    sql = '''INSERT INTO {tablename} (raw_data_id, file_id, question_id, answer_start_year, answer_end_year, rebels_receive_aid, line_data)
              VALUES (%s,%s,%s,%s,%s,%s,%s)'''
    return InsertDataWithGivenSQLAndTable (tableToInsertInto, sql, data)


def InsertDidConflictRecur (data):
    pass