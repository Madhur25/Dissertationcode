import speech_recognition as sr
from jproperties import Properties

from dao.DBConnection import Dao
from util import Util
import logging
import re


class SphixAPI:
    def callSphixAPI(path,filename):
        r = sr.Recognizer()
        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)

        logging.basicConfig(filename=configs.get("sphix_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.info("Checking test file exists Google")
        if (path.__contains__("dataset2")):
            i = filename.split("\\")[1].split('-')[1].split('.')[0].lstrip('0')
            if (len(i) == 0):
                i = 0
        try:
            fname = filename.split("\\")[1]
            fileprocessed,isContentMatched = Dao.dbcall(fname,'mscdissertation.dbo.Sphinx_sr')
            if(fileprocessed == True):
                return isContentMatched
            failedrecord = Dao.dbcallForFailedRecord(fname, 'SphixAPI', 'mscdissertation.dbo.FailedRecords')
            if(failedrecord == True):
                return -1
            with sr.AudioFile(filename) as source:
                audio = r.listen(source)
                text = r.recognize_sphinx(audio)
                text = text.lower()
                text = re.sub(r'[^\w\s]', '', text)
                text = text.replace("'", "")
                print(text)
                audiotxtarr = text.split()
                logger.info("Calling util Compare Function Sphix")
            if(path.__contains__("dataset1")):
                isContentMatched, listToStr = Util.Util.compareText(audiotxtarr)
            else:
                filename = filename.split('\\')[1].split('.')[0]
                isContentMatched, listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
            logger.info('calling on db conn Sphix')
            Dao.insertrecord(fname, text, isContentMatched, listToStr, 'mscdissertation.dbo.Sphinx_sr')
            return isContentMatched
        except Exception as e:
            Dao.insertFailRecords(fname, 'SphixAPI', " Sphix API fail")
            logger.error(filename + ": Sphix API fail")
            return -1


