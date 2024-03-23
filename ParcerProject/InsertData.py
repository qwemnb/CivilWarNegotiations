from tools import logger
import InsertSplitQuestion
import splitQuestion
    
def InsertAllSplitQuestinos():
    
    logger.info("\n\n************Begin Data Insert to Split Tables************\n\n")
    dataHasInsertedCorrectly = False
    currentTable = ""
                
    dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertRebelGroupsFightingByYear(splitQuestion.SplitRebelGroupsFightingByYear())

    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertChangesToGovernment(splitQuestion.SplitQuestionChangesToGovernment())
    
    #if dataHasInsertedCorrectly is True:
        #dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertCeasefireDeclared(splitQuestion.SplitQuestionCeasefireDeclared
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertOfferInducements(splitQuestion.SplitQuestionOfferInducements())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertNegotiationsSuggested(splitQuestion.SplitQuestionNegotiationsSuggested())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertOneOrBothRefuseNegotiate(splitQuestion.SplitQuestionOneOrBothRefuseNegotiate())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertContentOfNegotiations(splitQuestion.SplitQuestionContentOfNegotiations())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertEndWithoutSigning(splitQuestion.SplitQuestionEndWithoutSigning())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertWasAgreementSigned(splitQuestion.SplitQuestionWasAgreementSigned())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertAgreementEndFighting(splitQuestion.SplitQuestionAgreementEndFighting())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertReachedNotSigned(splitQuestion.SplitQuestionReachedNotSigned())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertUnsignedEndFighting(splitQuestion.SplitQuestionUnsignedEndFighting())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertOutsideOfferMediation(splitQuestion.SplitQuestionOutsideOfferMediation())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertDidMediationOccur(splitQuestion.SplitQuestionDidMediationOccur())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertWasUNInvolved(splitQuestion.SplitQuestionWasUNInvolved())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertWereIGOInvolved(splitQuestion.SplitQuestionWereIGOInvolved())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertThirdPartyIntervene(splitQuestion.SplitQuestionThirdPartyIntervene())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertDidGovernmentRecieveAid(splitQuestion.SplitQuestionDidGovernmentReceiveAid())
    
    if dataHasInsertedCorrectly is True:
        dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertDidRebelsRecieveAid(splitQuestion.SplitQuestionDidRebelsReceiveAid())
    
    #if dataHasInsertedCorrectly is True:
        #dataHasInsertedCorrectly, currentTable  = InsertSplitQuestion.InsertDidConflictRecur(splitQuestion.SplitQuestionDidConflictRecur())
    
    if  dataHasInsertedCorrectly is True:
        logger.info("All Data Inserted Correctly")
    else:
        logger.error("!!!!Failed to insert into table: {tablename}!!!!".format(currentTable))
    
    logger.info("\n\n************End Data Insert to Split Tables************\n\n")
    return dataHasInsertedCorrectly
    


InsertAllSplitQuestinos()
'''
TRUNCATE `heather`.`split_agreement_end_fighting`;
TRUNCATE `heather`.`split_agreement_signed`;
TRUNCATE `heather`.`split_content_of_negotiations`;
TRUNCATE `heather`.`split_end_without_signing`;
TRUNCATE `heather`.`split_govt_changes_by_year`;
TRUNCATE `heather`.`split_govt_receive_aid`;
TRUNCATE `heather`.`split_igo_involved`;
TRUNCATE `heather`.`split_mediation_occur`;
TRUNCATE `heather`.`split_negotiations_refused`;
TRUNCATE `heather`.`split_negotiations_suggested`;
TRUNCATE `heather`.`split_offer_inducements`;
TRUNCATE `heather`.`split_outside_offer_mediation`;
TRUNCATE `heather`.`split_reached_not_signed`;
TRUNCATE `heather`.`split_rebel_groups_by_year`;
TRUNCATE `heather`.`split_rebels_receive_aid`;
TRUNCATE `heather`.`split_third_party_intervene`;
TRUNCATE `heather`.`split_un_involved`;
TRUNCATE `heather`.`split_unsigned_end_fighting`;
'''