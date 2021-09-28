
import os
import glob
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from jproperties import Properties

from dao.DBConnection import Dao
from util import Util
import logging
import re



class IbmApi:
    def callIbmAPI(path1,filename):

        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)

        logging.basicConfig(filename=configs.get("ibm_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.info("Checking test file exists IBM")
        if (path1.__contains__("dataset2")):
            i = filename.split("\\")[1].split('-')[1].split('.')[0].lstrip('0')
            if (len(i) == 0):
                i = 0
        try:
            fname = filename.split("\\")[1]
            fileprocessed, isContentMatched = Dao.dbcall(fname, 'mscdissertation.dbo.IBM_sr')
            if (fileprocessed == True):
                return isContentMatched
            failedrecord = Dao.dbcallForFailedRecord(fname, 'IBMAPI', 'mscdissertation.dbo.FailedRecords')
            if (failedrecord == True):
                return -1;
            logger.info("Authenticate the Connection")
            apikey = path1.__contains__("apikey")
            url = path1.__contains__("url")
            authenticator = IAMAuthenticator(apikey)
            stt = SpeechToTextV1(authenticator=authenticator)
            stt.set_service_url(url)
            logger.info("Callinf IBM API")

            with open(filename, 'rb') as f:
                text = stt.recognize(audio=f,content_type='audio/mp3').get_result()
                if(len(text['results']) != 0):
                    result = text['results'][0]['alternatives'][0]['transcript']
                    result = result.lower()
                    result = re.sub(r'[^\w\s]', '', result)
                    result = result.replace("'", '')
                    audiotxtarr = result.split()
                    logger.info("Calling util Compare Function IBM")
                    if(path1.__contains__("dataset1")):
                        isContentMatched,listToStr = Util.Util.compareText(audiotxtarr)
                    else:
                        filename = filename.split('\\')[1].split('.')[0]
                        isContentMatched, listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
                    logger.info('calling on db conn IBM')
                    Dao.insertrecord(fname, result, isContentMatched, listToStr, 'mscdissertation.dbo.IBM_sr')
                else:
                    Dao.insertFailRecords(fname, 'IBMAPI', " No result returned")
                    logger.error(filename + "No result returned")
                    return -1
                return isContentMatched
        except:
            Dao.insertFailRecords(fname, 'IBMAPI', " IBM API fail")
            logger.error(filename + ": IBM API fail")
            return -1

