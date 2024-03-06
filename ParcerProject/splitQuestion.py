import re
import tools
import InsertSplitQuestion
from tools import logger
from QuestionDictionary import questionDictionary

def CheckQuestionExists ():
    pass

def GetFileName (fileId):
    connection, cursor = tools.DatabaseConnection()
    sql = '''Select file_name from files where id = {fileid}'''.format(fileid = fileId)
    logger.debug("Executing SQL: {sqlstatement}".format(sqlstatement = sql))
    cursor.execute(sql)
    fileName = cursor.fetchone()
    cursor.close()
    connection.close() 
    return fileName[0]

def LineStarsWithAYear (line):
    #check that the correct type of variable, String, has been passed in.
    if isinstance(line, str): 
    #check if the beginning of the string provided are a year from 1941 to 2016
        return (re.match(r'.*([19][40-99]{2})', line.lstrip()[0:4]) is not None or re.match(r'.*([20][00-16]{2})', line.lstrip()[0:4]) is not None)
    else:
        logger.warning("LineStartsWithAYear takes a string but was passed a {type} instead!".format(type = type(line)))
        return False
    
    
#When a line has a year range this splits it into beginning and end years. and returns a tuple of (begin, end) years
def SplitYearRange(yearString):
    #check that the correct type of variable, String, has been passed in.
    if isinstance(yearString, str):
        if yearString.lstrip().split("-", 1)[1] is not None:
            startYearRange = yearString.lstrip().split("-", 1)[0]
            if LineStarsWithAYear(yearString.lstrip().split("-", 1)[1]):
                endYearRange = yearString.lstrip().split("-", 1)[1]
            else:
                endYearRange = startYearRange
        return startYearRange, endYearRange
    
    else:
        logger.warning("SplitYearRange takes a string but was passed a {type} instead!".format(type = type(yearString)))
        return "",""
        
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
                    JOIN questions q ON rd.question_id = q.id
                    WHERE q.question_text LIKE "{question}%"'''.format(question = questionText)   
    
    logger.debug("Executing SQL: {sqlstatement}".format(sqlstatement = sql))
    cursor.execute(sql)
    rawQuestionData = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return rawQuestionData



def SplitRebelGroupsFightingByYear():
    rawData = GetRawDataForQuestion("Numbersandnamesofotherrebelgroupsfightingbyyear")
    #splitData will contain raw data line, file id, question id, the aim, the number and list of rebel groups
    splitData =  []
    
    aims = ''
    
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            #skip lines with no data in them (whitespace)
            if (line.isspace() is False):
                if "other" in line.lower():
                    aims = line
                else:
                    splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], aims, line.lstrip(" ·")))
    return splitData                 



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
    rawData = GetRawDataForQuestion("Didthegovernmentoffertherebelsanyinducements")
    
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
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, line.lstrip()))    

    return splitData



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
    rawData = GetRawDataForQuestion("ForeachnegotiationsuggesteddidoneorbothbelligerentsrefusetonegotiateWhorefusedtonegotiate")
    splitData = []
    year = ''
    #stores month number default is always 12
    month = 12
    #contains Yes or No 
    refused = ''
    
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            if LineStarsWithAYear(line):
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                month = CheckMonth(line)
                if "No," in line:
                    refused = "No"
                else:
                    refused = "Yes"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, refused, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, refused, line.lstrip()))
    return splitData 
    

def SplitQuestionContentOfNegotiations ():
    
    rawData = GetRawDataForQuestion("Ifbothpartiesagreedtonegotiateandnegotiationoccurredwhatwasthecontentofnegotiations")
    splitData = []
    year = ''
    #stores month number default is always 12
    month = 12
    
    for rawDataRow in rawData:
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            if LineStarsWithAYear(line):
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                month = CheckMonth(line)
                
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, line.lstrip()))
    return splitData     

def SplitQuestionEndWithoutSigning ():
    
    rawData = GetRawDataForQuestion("Ifbothpartiesagreedtonegotiateandnegotiationoccurreddideitherorbothbelligerentsendthenegotiationswithoutsigninganagreement")
    splitData = []
    year = ''
    #stores month number default is always 12
    month = 12
    potentialError = "" #holds error message until a new year is found, if there is no whoDidNotSign information error is thrown
    
    for rawDataRow in rawData: #each file has a single raw data line for each question
        splitanswer = rawDataRow[3].splitlines() #split the full question answer into individual lines
        for line in splitanswer:
            if (line.isspace() is False):
                #reset who did not sign variable
                whoDidNotSign = ""
                linealnum = ''.join(i for i in line if i.isalnum()) #remove all special characters and spaces
                if LineStarsWithAYear(line):
                    if potentialError != "": #this means there was no whoDidNotSign info found between 2 year sections of the answer
                        logger.warning(potentialError)
    
                    year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                    month = CheckMonth(line)
                    potentialError = ""
                if "n/a" in line.lower():
                    whoDidNotSign ="n/a"
                elif "continuedinto" in linealnum.lower():
                    whoDidNotSign = "Continued"
                elif "both" in linealnum.lower():
                            whoDidNotSign = "Both"
                elif "govt" in linealnum.lower() or "government" in linealnum.lower():
                            whoDidNotSign = "Government"
                elif "rebels" in linealnum.lower():
                            whoDidNotSign = "Rebels"
                elif ":" in line:
                    if "no" in line.lstrip().split(":", 1)[1].lstrip().split(" ", 1)[0].lower(): #remove leading date, see if no is before the next space.
                        whoDidNotSign ="n/a"  
                    
                if whoDidNotSign == "":
                    potentialError = "QUESTION ID {questionid} - Unable to determine who did not sign agreement: {linetext} in file {fileid}: {filename}. \nRAW DATA ID {rawdataid}:\n{rawdatatext}".format(questionid = rawDataRow[2], linetext = line, fileid = rawDataRow[1], filename = GetFileName(rawDataRow[1]), rawdataid = rawDataRow[0], rawdatatext =  rawDataRow[3])
                else:
                    potentialError = ""
                    #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, who did not sign (government/rebels/both) and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, whoDidNotSign, line.lstrip()))
    return splitData                     

    
def SplitQuestionWasAgreementSigned ():
    

    rawData = GetRawDataForQuestion("WasanagreementsignedIfsowhatwasthecontentofthesignedagreement")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        #stores month number default is always 12
        month = 12
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            agreementSigned = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                month = CheckMonth(line)
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                agreementSigned = "No"
            elif "yes" in lineWithYearMonthRemoved:
                agreementSigned = "Yes"
            elif "n/a" in lineWithYearMonthRemoved:
                agreementSigned = "N/A"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, agreementSigned, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, agreementSigned, line.lstrip()))
    return splitData 


def SplitQuestionAgreementEndFighting ():
    rawData = GetRawDataForQuestion("DidthesignedagreementendthefightingIfnotwhoresumedcontinuedfighting")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        #stores month number default is always 12
        month = 12
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            endFighting = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                month = CheckMonth(line)
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                endFighting = "No"
            elif "yes" in lineWithYearMonthRemoved:
                endFighting = "Yes"
            elif "n/a" in lineWithYearMonthRemoved:
                endFighting = "N/A"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, endFighting, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, endFighting, line.lstrip()))
    return splitData


def SplitQuestionReachedNotSigned ():
    
    rawData = GetRawDataForQuestion("WasanagreementreachedbutnotsignedieaverbalagreementIfsowhatwasthecontentoftheverbalagreement")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        #stores month number default is always 12
        month = 12
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            agreementNotSigned = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                month = CheckMonth(line)
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                agreementNotSigned = "No"
            elif "yes" in lineWithYearMonthRemoved:
                agreementNotSigned = "Yes"
            elif "n/a" in lineWithYearMonthRemoved:
                agreementNotSigned = "N/A"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, agreementNotSigned, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, agreementNotSigned, line.lstrip()))
    return splitData

def SplitQuestionUnsignedEndFighting ():
    rawData = GetRawDataForQuestion("DidtheunsignedieverbalagreementendthefightingIfnotwhoresumedcontinuedfighting")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        #stores month number default is always 12
        month = 12
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            notSignedEndFighting = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                month = CheckMonth(line)
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                notSignedEndFighting = "No"
            elif "yes" in lineWithYearMonthRemoved:
                notSignedEndFighting = "Yes"
            elif "n/a" in lineWithYearMonthRemoved:
                notSignedEndFighting = "N/A"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, notSignedEndFighting, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, notSignedEndFighting, line.lstrip()))
    return splitData


def SplitQuestionOutsideOfferMediation ():
    rawData = GetRawDataForQuestion("Didsomeoneoutsidetheconflictoffertomediatebetweenthebelligerents")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        #stores month number default is always 12
        month = 12
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            mediationOffer = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                month = CheckMonth(line)
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                mediationOffer = "No"
            elif "yes" in lineWithYearMonthRemoved:
                mediationOffer = "Yes"
            elif "n/a" in lineWithYearMonthRemoved:
                mediationOffer = "N/A"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, mediationOffer, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, mediationOffer, line.lstrip()))
    return splitData


def SplitQuestionDidMediationOccur ():
    rawData = GetRawDataForQuestion("Didmediationbyanoutsideactoractuallyoccur")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        #stores month number default is always 12
        month = 12
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            didMediatinOccur = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                year = line.lstrip().split(" ", 1)[0]#set year equal to the year in the line, including trailing letters which distinguish negotiations in same year.
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                month = CheckMonth(line)
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                didMediatinOccur = "No"
            elif "yes" in lineWithYearMonthRemoved:
                didMediatinOccur = "Yes"
            elif "n/a" in lineWithYearMonthRemoved:
                didMediatinOccur = "N/A"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, month, didMediatinOccur, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, month, didMediatinOccur, line.lstrip()))
    return splitData


def SplitQuestionWasUNInvolved ():
    rawData = GetRawDataForQuestion("WastheUNinvolvedintheconflictdonotincludemediation")
    splitData = []
    
    for rawDataRow in rawData:
        year = ''
        beginYear = ""
        endYear = ""
        splitanswer = rawDataRow[3].splitlines()
        for line in splitanswer:
            wasUNInvolved = ""
            if LineStarsWithAYear(line): 
                #line = line.lstrip() # remove beginning whitespace
                #set year equal to the year data in the line, including trailing letters which distinguish negotiations in same year.
                year = line.lstrip().split(" ", 1)[0]
                if ":" in year:
                    # "year:" is used of no month is given. This removes the : if it is included before the first space.
                    year = year.replace(":", "")
                if "-" in year:
                    #this answer can contain year ranges.
                    beginYear, endYear = SplitYearRange(year)
                else:
                    beginYear = year
                    endYear = year
                
            #Lines with year are separated by a : after the year and month information.
            if ":" in line:
                #set to lower case, remove leading spaces, split at the : and take the remaining data
                lineWithYearMonthRemoved = line.lower().lstrip().split(":", 1)[1]
            else:
                lineWithYearMonthRemoved = line.lower()
                
            if "no" in lineWithYearMonthRemoved:
                wasUNInvolved = "No"
            elif "n/a" in lineWithYearMonthRemoved:
                wasUNInvolved = "N/A"
            #if the line contains information then the answer is Yes as "No" and "N/A" are already accounted for.
            elif lineWithYearMonthRemoved != "":
                wasUNInvolved = "Yes"
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, wasUNInvolved, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], beginYear, endYear, wasUNInvolved, line.lstrip()))
    return splitData


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


#print ('1980: No, continued into 1981'.lstrip().split(":", 1)[1].lstrip().split(" ", 1)[0].lower())

print (SplitQuestionWasUNInvolved())
#print(GetRawDataForQuestion("WerethereanychangesingovernmentduringtheconflictWerethechangesconstitutionalorunconstitutionalProvidedatesanddetailsabouttypeofgovernmentbeforeandafterchangeincludingleftrightorientationofpartyandhowwhenthegovernmentchanged"))
#print (SplitQuestionOfferInducements())

#print(SplitQuestionChangesToGovernment())
#print(SplitQuestionNegotiationsSuggested())
#print(LineStarsWithAYear(3))
#InsertSplitQuestion.InsertNegotiationsSuggested(SplitQuestionNegotiationsSuggested())
#InsertSplitQuestion.InsertChangesToGovernment(SplitQuestionChangesToGovernment())