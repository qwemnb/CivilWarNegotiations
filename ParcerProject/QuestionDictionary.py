import tools
from tools import logger

def GetQuestionFromDB():
    tempQuestionDictionary = {}
    connection, cursor = tools.DatabaseConnection()
    sql = '''SELECT id,question_text FROM questions'''
    
    logger.debug("Executing: {sqlstatement}".format(sqlstatement = sql ))
    
    cursor.execute(sql)
    
    for (questionId,questionText) in cursor:
        tempQuestionDictionary[questionText] = questionId
        
    cursor.close()
    connection.close()
    return tempQuestionDictionary

questionDictionary = GetQuestionFromDB()






    
    