
import collections
import re
import tools
import InsertSplitQuestion



def CheckQuestionExists ():
    pass

def LineStarsWithAYear (line):
    logger = tools.getLogger()
    if isinstance(line, str): #check that the correct type of variable, String, has been passed in.
    #check if the beginning of the string provided are a year from 1941 to 2016
        return (re.match(r'.*([19][40-99]{2})', line.lstrip()[0:4]) is not None or re.match(r'.*([20][00-16]{2})', line.lstrip()[0:4]) is not None)
    else:
        logger.warning("LineStartsWithAYear takes a string but was passed a {type} instead!".format(type = type(line)))
        return False
    
def CheckMonth(line):
    
    lineToCheck = line.lower() #set line to include only lowercase letters
    
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
        #when no month is given we are setting that to December so that the whole year is included.
        return 12 
                
    

def SplitQuestionChangesToGovernment ():    
    #connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    #cursor = connection.cursor()
    connection, cursor = tools.DatabaseConnection()
    
    
    rawData = []
    sql = '''SELECT rd.id, rd.file_id, q.id, rd.answer 
                    FROM raw_data rd 
                    JOIN questions q ON rd.question = q.question_text
                    WHERE q.question_text LIKE "Were there any changes in government during the conflict%"'''

    cursor.execute(sql)
    rawData = cursor.fetchall()
    #pull data from select statement into rawData

    splitData =  []
    year = ''
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            #find years between 1940 and 2016. the range of the current data sets
            if LineStarsWithAYear(line):
                year = line
            if year != line:
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, line.lstrip() ))
      

    cursor.close()
    connection.close()
    #Insert_govt_changes_by_year_Data(splitData)
    return splitData



def SplitQuestionNegotiationsSuggested():
    #tools = getLogger()
    #connection = mysql.connector.connect(user='root', password ='root', host='localhost', database='heather')
    #cursor = connection.cursor()
    connection, cursor = tools.DatabaseConnection()
    ##Selecting all rows for "negotiations suggested" question from the raw data input
    sql = '''SELECT rd.id, rd.file_id, q.id, rd.answer 
                    FROM raw_data rd 
                    JOIN questions q ON rd.question = q.question_text
                    WHERE q.question_text LIKE "Were negotiations suggested?%"'''
    cursor.execute(sql)
    rawData = cursor.fetchall()

    splitData =  []
    #splitData will contain id of raw data line, file id, question id, year, month and each lines text
    year = ''
    month = ''
    #cycle through the lines in the rawDAta and label each row with the correct year and month.
    #each set of data starts with a line that is between 1941 and 2016
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines() #split the raw data into a list of individual lines
        for line in splitanswer:
            if LineStarsWithAYear(line): #this function returns true if the line starts with a year between 1941 and 2016
                year = line.lstrip()[0:4] #set year equal to the year in the line. remove and whitespace before the year
                month = CheckMonth(line)
            if (line.isspace() is False): #remove lines with no data in them (whitespace)
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month and each lines text with begining whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, line.lstrip()))    

    
    
    cursor.close()
    connection.close()
    return splitData



#print(SplitQuestionChangesToGovernment())
#print(LineStarsWithAYear(3))
#InsertSplitQuestion.InsertNegotiationsSuggested(SplitQuestionNegotiationsSuggested())
InsertSplitQuestion.InsertChangesToGovernment(SplitQuestionChangesToGovernment())