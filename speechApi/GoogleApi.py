import speech_recognition as sr
import os
import glob

from jproperties import Properties

from dao.DBConnection import Dao
from util import Util
import logging
import re


class GoogleApi:
    def callGoogleAPI(path,filename):
        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)
        r = sr.Recognizer()
        logging.basicConfig(filename=configs.get("google_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        if(path.__contains__("dataset2")):
            i = filename.split("\\")[1].split('-')[1].split('.')[0].lstrip('0')
            if (len(i) == 0):
                i = 0
        # Create and configure logger

        try:
            fname = filename.split("\\")[1]
            fileprocessed,isContentMatched = Dao.dbcall(fname, 'mscdissertation.dbo.Google_sr')
            print(fname)
            if(fileprocessed  == True):
                return isContentMatched
            failedrecord = Dao.dbcallForFailedRecord(fname,'GoogleAPI', 'mscdissertation.dbo.FailedRecords')
            if(failedrecord == True):
                return -1;
            with sr.AudioFile(filename) as source:
                audio = r.listen(source)
                text = r.recognize_google(audio)
                text = text.lower()
                text = re.sub(r'[^\w\s]', '', text)
                text = text.replace("'", "")
                print(text)
                audiotxtarr = text.split()
            logger.info("Calling util Compare Function Google")
            if(path.__contains__("dataset1")):
                isContentMatched,listToStr = Util.Util.compareText(audiotxtarr)
            else:
                filename = filename.split('\\')[1].split('.')[0]
                isContentMatched,listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
            logger.info('calling on db conn Google')
            Dao.insertrecord(fname, text, isContentMatched, listToStr, 'mscdissertation.dbo.Google_sr')
            return isContentMatched
        except Exception as e:
            Dao.insertFailRecords(fname,'GoogleAPI'," Google API fail")
            return -1
            logger.error(fname + ": Google API fail")
















