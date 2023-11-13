import re
import tools
import InsertSplitQuestion
from tools import logger
from QuestionDictionary import questionDictionary

def CheckQuestionExists ():
    pass

def LineStarsWithAYear (line):
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
                
#this takes a partial test question and returns the raw_date tables data for the matching question.              
def GetRawDataForQuestion (questionText):
    connection, cursor = tools.DatabaseConnection()
    sql = '''SELECT rd.id, rd.file_id, q.id, rd.answer 
                    FROM raw_data rd 
                    JOIN questions q ON rd.question = q.question_text
                    WHERE q.question_text LIKE "{question}%"'''.format(question = questionText)   
    
    logger.debug("Executing SQL: {sqlstatement}".format(sqlstatement = sql))
    cursor.execute(sql)
    rawQuestionData = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rawQuestionData





def SplitRebelGroupsFightingByYear():
    pass
            
    

def SplitQuestionChangesToGovernment ():    

    rawData = GetRawDataForQuestion("WerethereanychangesingovernmentduringtheconflictWerethechangesconstitutionalorunconstitutionalProvidedatesanddetailsabouttypeofgovernmentbeforeandafterchangeincludingleftrightorientationofpartyandhowwhenthegovernmentchanged")

    splitData =  []
    #splitData will contain raw data line, file id, question id, year, each line of text for the year
    year = ''
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            #find years between 1940 and 2016. the range of the current data sets
            if LineStarsWithAYear(line):
                year = line
            if year != line: #skip the year header on each block of text
                #add each line to splitData 
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, line.lstrip()))

    return splitData


def SplitQuestionCeasefireDeclared():
    pass


def SplitQuestionOfferInducements():
    pass


def SplitQuestionNegotiationsSuggested():
    
    
    rawData = GetRawDataForQuestion("Werenegotiationssuggested")
    
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

    return splitData


def SplitQuestionOneOrBothRefuseNegotiate ():
    pass


def SplitQuestionContentOfNegotiations ():
    pass


def SplitQuestionEndWithoutSigning ():
    pass


def SplitQuestionWasAgreementSigned ():
    pass


def SplitQuestionAgreementEndFighting ():
    pass


def SplitQuestionReachedNotSigned ():
    pass


def SplitQuestionUnsignedEndFighting ():
    pass


def SplitQuestionOutsideOfferMediation ():
    pass


def SplitQuestionDidMediationOccur ():
    pass


def SplitQuestionWasUNInvolved ():
    pass


def SplitQuestionWereIGOInvolved ():
    pass


def SplitQuestionThirdPartyIntervene ():
    pass


def SplitQuestionDidGovernmentRecieveAid ():
    pass


def SplitQuestionDidRebelsRecieveAid ():
    pass


def SplitQuestionDidConflictRecur ():
    pass


#print(questionDictionary)

print(GetRawDataForQuestion("WerethereanychangesingovernmentduringtheconflictWerethechangesconstitutionalorunconstitutionalProvidedatesanddetailsabouttypeofgovernmentbeforeandafterchangeincludingleftrightorientationofpartyandhowwhenthegovernmentchanged"))

#print(SplitQuestionChangesToGovernment())
#print(SplitQuestionNegotiationsSuggested())
#print(LineStarsWithAYear(3))
#InsertSplitQuestion.InsertNegotiationsSuggested(SplitQuestionNegotiationsSuggested())
#InsertSplitQuestion.InsertChangesToGovernment(SplitQuestionChangesToGovernment())