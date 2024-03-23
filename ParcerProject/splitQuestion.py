import re
import tools
from tools import logger

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
        return (re.match(r'([19]{2}[40-99]{2})', line.lstrip()[0:4]) is not None or re.match(r'([20]{2}[0]{1}[0-9]{1})', line.lstrip()[0:4]) is not None  or re.match(r'([20]{2}1[0-6]{1})', line.lstrip()[0:4]) is not None)
    else:
        logger.warning("LineStartsWithAYear takes a string but was passed a {type} instead!".format(type = type(line)))
        return False
    
#returns the start and end indexes of the year in the given line.
def FindYearInsideString (line):
    
    if isinstance(line, str):
        #date ranges are written as ####-####
        if "-" in line:
            #return the date ranges index.
            return FindYearRangeInsideString(line)
        else:     
            if LineStarsWithAYear(line):
                return 0, 4
            re1 = re.search(r'([19]{2}[40-99]{2})', line)
            if re1 is not None:
                return re1.span(0)
            
            re2 = re.search(r'([20]{2}[0]{1}[0-9]{1})', line)
            if re2 is not None:
                return re2.span(0)
            
            re3 = re.search(r'([20]{2}1[0-6]{1})', line)
            if re3 is not None:
                return re3.span(0)
            
            return None, None        
    else:
        logger.warning("FindYearInsideString takes a string but was passed a {type} instead!".format(type = type(line)))
        return None, None        
    
    
#When a line has a year range this splits it into beginning and end years. and returns a tuple of (begin, end) years
def SplitYearRange(yearString):
    endYearRange = startYearRange = None
    #check that the correct type of variable, String, has been passed in.
    if isinstance(yearString, str):
        i1, i2 = FindYearRangeInsideString(yearString)
        if i1 is not None and i2 is not None:
            startYearRange = yearString[i1:i1+4]
            endYearRange = yearString[i2-4:i2]
                
        return startYearRange, endYearRange
        
            
    
    else:
        logger.warning("SplitYearRange takes a string but was passed a {type} instead!".format(type = type(yearString)))
        return None,None

#return the index of the beginning and end of a date range in the given string
def FindYearRangeInsideString(yearString):
 
    re1 = re2 = re3 = re4 = re5 = re6 = None
    
    if isinstance(yearString, str):
        re1 = re.search(r'[19]{2}[40-99]{2}-[19]{2}[40-99]{2}',yearString)
        if re1 is not None:   
            return re1.span(0)
        re2 = re.search(r'[19]{2}[40-99]{2}-[20]{2}0[0-9]{1}',yearString)
        if re2 is not None:
            return re2.span(0)
        re3 = re.search(r'[19]{2}[40-99]{2}-[20]{2}1[0-6]{1}',yearString)
        if re3 is not None:
            return re3.span(0)
        re4 = re.search(r'[20]{2}0[0-9]{1}-[20]{2}0[0-9]{1}',yearString)
        if re4 is not None:
            return re4.span(0)
        re5 = re.search(r'[20]{2}0[0-9]{1}-[20]{2}1[0-6]{1}',yearString)
        if re5 is not None:
            return re5.span(0)
        re6 = re.search(r'[20]{2}1[0-6]{1}-[20]{2}1[0-6]{1}',yearString)
        if re6 is not None:
            return re6.span(0)
        else:
            return None,None
    
    else:
        logger.warning("FindYearRangeInsideString takes a string but was passed a {type} instead!".format(type = type(yearString)))
        return None,None
    


        
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
                
#this takes a partial question and returns the raw_date table's data for the matching question.              
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
    

    
    for rawDataRow in rawData:
        aims = ""
        splitanswer = rawDataRow[3].splitlines()
        year = ""
           
        for line in splitanswer:
            #skip lines with no data in them (whitespace)
            if (line.isspace() is False):
                splitLine = line.lower().lstrip(" ·")

                if LineStarsWithAYear(splitLine):
                    year = splitLine[0:4]
                if "other" in splitLine:
                    aims = line
                else:
                    splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], year, aims, line.lstrip(" ·")))
    return splitData                 



def SplitQuestionChangesToGovernment ():    

    rawData = GetRawDataForQuestion("WerethereanychangesingovernmentduringtheconflictWerethechangesconstitutionalorunconstitutionalProvidedatesanddetailsabouttypeofgovernmentbeforeandafterchangeincludingleftrightorientationofpartyandhowwhenthegovernmentchanged")

    splitData =  []
    #splitData will contain raw data line, file id, question id, year, each line of text for the year
    year = ""
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
    year = ""
    month = 12
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
    year = ""
    month = 12
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
    year = ""
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
    year = ""
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
    year = ""
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
        year = ""
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
        year = ""
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
        year = ""
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
        year = ""
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
        year = ""
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
        year = ""
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
        year = ""
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
    rawData = GetRawDataForQuestion("WereregionalIGOsinvolvedintheconflictdonotincludemediation")
    splitData = []
    
    for rawDataRow in rawData:
        year = ""
        beginYear = ""
        endYear = ""
        wasIGOInvolved = ""
        
        splitanswer = rawDataRow[3].splitlines()
        
        for line in splitanswer:

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
                                 
                if "n/a" in line.lower():
                    wasIGOInvolved = "N/A"
                #if the line contains information then the answer is Yes
                else:
                    wasIGOInvolved = "Yes"
            elif line.lower() == "no":
                wasIGOInvolved = "No"
                
            if (line.isspace() is False):
                #splitData contains id of raw data line [0], file id [1] , question id [2], year, wasIGOInvolved, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2], beginYear, endYear, wasIGOInvolved, line.lstrip()))
                
    return splitData


def SplitQuestionThirdPartyIntervene ():
    rawData = GetRawDataForQuestion("DidathirdpartystateinterveneintheconflictIfsohowmanyandonwhosebehalfbyyear")
    splitData = []
    
    for rawDataRow in rawData:
        year = ""
        group = "" #this can be Government or Rebels
        beginYear = ""
        endYear = ""
        interventionType = ""
        didThirdPartyIntervene = ""
        
        splitanswer = rawDataRow[3].splitlines()
        
        for line in splitanswer:
            #if the line starts with government or reberls then reset year and intervention type
            if line.lower().lstrip().startswith("government"):
                group = "Government"
                year = ""
                interventionType = ""
            elif line.lower().lstrip().startswith("rebel"):
                group = "Rebels"
                year = ""
                interventionType = ""
            #if the line does not start with Government or Rebel check for a year
            else:
                if LineStarsWithAYear(line):
                    interventionType = ""
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
                    #if the year line contains n/a then no party intervened in that year orr year range. 
                    if "n/a" in line.lower():
                        didThirdPartyIntervene = "N/A"
                        interventionType = "N/A"
                        splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2],group, didThirdPartyIntervene, beginYear, endYear, interventionType, line.lstrip()))
                #The type of intervention starts with a "-" on rows under a year and is labeled with the type of intervention.
                elif line.lower().lstrip().startswith("-"):
                    interventionType = line.lstrip().split("-", 1)[1]
                #if the data does not start with a year or an intervention type then it is data for that group/year/intervention type combination.
                else:
                    if (line.isspace() is False):
                        #splitData contains id of raw data line [0], file id [1] , question id [2], year, wasIGOInvolved, and each lines text with beginning whitespace removed
                        splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2],group, didThirdPartyIntervene, beginYear, endYear, interventionType, line.lstrip()))
    return splitData


def SplitQuestionDidGovernmentReceiveAid ():
    rawData = GetRawDataForQuestion("Didthegovernmentreceivenonconflictspecificforeigndevelopmentaid")
    splitData = []
    
    for rawDataRow in rawData:
        wasAidGiven = ""
        beginYear = ""
        endYear = ""
        alphaNumLine = None
        splitanswer = rawDataRow[3].splitlines()
        
        
        for line in splitanswer:
            startYearIndex = endYearIndex = None
            #this holds that part of the line string that would contain a year if one or a range exist.
            yearString = ""
            lineToInsert = None
            
            
            if len(line.lower().lstrip()) > 0 and line.lower().lstrip()[0] == "-":
                line = line.split("-",1)[1]
            #does the line start with Yes
            if line == "Yes":
                wasAidGiven = "Yes"
                
            elif line.lower().lstrip()[0:4] == "yes," or line.lower().lstrip()[0:4] == "yes ":
                #This will return None if the line ends after the comma
                splitLine = line.lower().lstrip().split(", ", 1)[1]
                logger.debug("splitLineOnCommaLine: {splitline}".format(splitline = splitLine))
                
                #this removes all special characters including spaces
                alphaNumLine = ''.join(i for i in splitLine if i.isalnum())
                logger.debug("alphaNumLine: {alphaline}".format(alphaline = alphaNumLine))
                
                wasAidGiven = "Yes"
                yearString = splitLine
            #If it does not start with Yes
            else:
                alphaNumLine = ''.join(i for i in line.lower().lstrip() if i.isalnum())
                logger.debug("alphaNumLine: {alphaline}".format(alphaline = alphaNumLine))
                yearString = line.lower().lstrip().split(" ", 1)[0]
            
            
            #if the line starts with a 4 digit year between 1941 and 2016   
            if  alphaNumLine is not None and LineStarsWithAYear(alphaNumLine):
                wasAidGiven = "Yes"
                logger.debug("yearString: {yearstring}".format(yearstring = yearString))
                
                #if the yearString contains a range
                if len(yearString) > 4 and yearString[4] == "-":
                    beginYear, endYear = SplitYearRange(yearString)
                    logger.debug(SplitYearRange(yearString))
                    logger.debug("beginYear: {begin} \n EndYear: {end}".format(begin = beginYear, end = endYear))
                else:
                    beginYear = endYear = alphaNumLine[0:4]
                    logger.debug("beginYear: {begin} \n EndYear: {end}".format(begin = beginYear, end = endYear))
            
                          
            #alphaNumLine is not used here because it does not contain the "/" that we need to look for.
            
            if "n/a" in line.lower():
                wasAidGiven = "N/A"
            
            if alphaNumLine is not None and ((len(alphaNumLine) > 2 and alphaNumLine[0:2] == "no") or alphaNumLine == "no"):
                wasAidGiven = "No"
            #if there is more than just the year data in the row we want to include it in the split data.
            #if the yearString is the samne as the line then we want to exclude it.
            logger.debug("line: {line}\nyearString: {yearstring}".format(line = line, yearstring = yearString))
            if len(line) >= len(yearString) and line.isspace() is False:
                #splitData contains id of raw data line [0], file id [1] , question id [2], begin year range ,end year range, wasAidGiven, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2],beginYear, endYear, wasAidGiven, line.lstrip()))
    return splitData
            


def SplitQuestionDidRebelsReceiveAid ():
    rawData = GetRawDataForQuestion("Didtherebelgroupreceivenonconflictspecificforeigndevelopmentaid")
    splitData = []
    
    for rawDataRow in rawData:
        wasAidGiven = ""
        beginYear = ""
        endYear = ""
        alphaNumLine = None
        splitanswer = rawDataRow[3].splitlines()
        
        
        for line in splitanswer:
            startYearIndex = endYearIndex = None
            #this holds that part of the line string that would contain a year if one or a range exist.
            yearString = ""
            lineToInsert = None
            
            if len(line.lower().lstrip()) > 0 and line.lower().lstrip()[0] == "-":
                line = line.split("-",1)[1]
            #does the line start with Yes
            if line == "Yes":
                wasAidGiven = "Yes"
                
            elif line.lower().lstrip()[0:4] == "yes," or line.lower().lstrip()[0:4] == "yes ":
                #This will return None if the line ends after the comma
                splitLine = line.lower().lstrip().split(", ", 1)[1]
                logger.debug("splitLineOnCommaLine: {splitline}".format(splitline = splitLine))
                
                #this removes all special characters including spaces
                alphaNumLine = ''.join(i for i in splitLine if i.isalnum())
                logger.debug("AlphaNumLine: {alphaline}".format(alphaline = alphaNumLine))
                
                wasAidGiven = "Yes"
                yearString = splitLine
            #If it does not start with Yes
            else:
                alphaNumLine = ''.join(i for i in line.lower().lstrip() if i.isalnum())
                logger.debug("AlphaNumLine: {alphaline}".format(alphaline = alphaNumLine))
                yearString = line.lower().lstrip().split(" ", 1)[0]
            
            
            #if the line starts with a 4 digit year between 1941 and 2016   
            if  alphaNumLine is not None and LineStarsWithAYear(alphaNumLine):
                wasAidGiven = "Yes"
                logger.debug("yearString: {yearstring}".format(yearstring = yearString))
                
                #if the yearString contains a range
                if len(yearString) > 4 and yearString[4] == "-":
                    beginYear, endYear = SplitYearRange(yearString)
                    logger.debug(SplitYearRange(yearString))
                    logger.debug("beginYear: {begin} \n EndYear: {end}".format(begin = beginYear, end = endYear))
                else:
                    beginYear = endYear = alphaNumLine[0:4]
                    logger.debug("beginYear: {begin} \n EndYear: {end}".format(begin = beginYear, end = endYear))
            
                          
            #alphaNumLine is not used here because it does not contain the "/" that we need to look for.
            
            if "n/a" in line.lower():
                wasAidGiven = "N/A"
            
            if alphaNumLine is not None and ((len(alphaNumLine) > 2 and alphaNumLine[0:2] == "no") or alphaNumLine == "no"):
                wasAidGiven = "No"
            #if there is more than just the year data in the row we want to include it in the split data.
            #if the yearString is the samne as the line then we want to exclude it.
            logger.debug("line: {line}\nyearString: {yearstring}".format(line = line, yearstring = yearString))
            if len(line) >= len(yearString) and line.isspace() is False:
                #splitData contains id of raw data line [0], file id [1] , question id [2], begin year range ,end year range, wasAidGiven, and each lines text with beginning whitespace removed
                splitData.append((rawDataRow[0],rawDataRow[1], rawDataRow[2],beginYear, endYear, wasAidGiven, line.lstrip()))
    return splitData
            


def SplitQuestionDidConflictRecur ():
    pass


'''
def TEST (splitanswer):    
    for line in splitanswer:
        year1 = year2 = None
        if LineStarsWithAYear(line.lstrip()):
            if "-" in line:
                year1, year2 = SplitYearRange(line.lstrip())
            else:
                year1 = year2 = line.lstrip()[0:4]               
        else:
            i1 , i2 = FindYearRangeInsideString(line)
            if i1 is not None and i2 is not None:
                year1, year2 = SplitYearRange(line[i1:i2])
        print(year1, year2)'''
        
        
#print(GetRawDataForQuestion("WerethereanychangesingovernmentduringtheconflictWerethechangesconstitutionalorunconstitutionalProvidedatesanddetailsabouttypeofgovernmentbeforeandafterchangeincludingleftrightorientationofpartyandhowwhenthegovernmentchanged"))
#print(SplitRebelGroupsFightingByYear())
#print(FindYearInsideString("1235232342015asd"))
#print(SplitQuestionChangesToGovernment())
#print(SplitQuestionNegotiationsSuggested())
#print(LineStarsWithAYear(3))
#InsertSplitQuestion.InsertNegotiationsSuggested(SplitQuestionNegotiationsSuggested())
#InsertSplitQuestion.InsertChangesToGovernment(SplitQuestionChangesToGovernment())