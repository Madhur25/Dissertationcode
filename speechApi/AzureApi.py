import azure.cognitiveservices.speech as speechsdk
import logging
from jproperties import Properties
from dao.DBConnection import Dao
from util import Util
import re

class AzureApi:
    def callAzureApi(path,filename):
        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)

        logging.basicConfig(filename=configs.get("azure_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.info("Checking test file exists Azure")
        if (path.__contains__("dataset2")):
            i = filename.split("\\")[1].split('-')[1].split('.')[0].lstrip('0')
            if (len(i) == 0):
                i = 0
        try:
            logger.info("Caling Azure API")
            fname = filename.split("\\")[1]
            fileprocessed,isContentMatched = Dao.dbcall(fname, 'mscdissertation.dbo.Azure_sr')
            if(fileprocessed == True):
                return isContentMatched
            failedrecord = Dao.dbcallForFailedRecord(fname, 'AzureAPI', 'mscdissertation.dbo.FailedRecords')
            if(failedrecord == True):
                return isContentMatched
            logger.info("Making Connection from Azure")
            speech_config = speechsdk.SpeechConfig(subscription=path.__contains__("azure_subscription"),
                                                           region=path.__contains__("azure_region"))
            audio_input = speechsdk.AudioConfig(filename=filename)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
            result = speech_recognizer.recognize_once_async().get()
            text = result.text
            text = text.lower()
            text = re.sub(r'[^\w\s]', '', text)
            text = text.replace("'","")
            print(text)
            audiotxtarr = text.split()
            print("Calling util Compare Function Azure")
            if(path.__contains__("dataset1")):
                isContentMatched,listToStr = Util.Util.compareText(audiotxtarr)
            else:
                filename = filename.split('\\')[1].split('.')[0]
                isContentMatched, listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
            print('calling on db conn Azure')
            Dao.insertrecord(fname, text, isContentMatched, listToStr, 'mscdissertation.dbo.Azure_sr')
            return isContentMatched
        except:
            Dao.insertFailRecords(fname, 'AzureAPI', " Azure API fail")
            return -1
            print(fname  + ": Azure API fail")



