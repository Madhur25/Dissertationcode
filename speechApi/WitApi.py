import os

from jproperties import Properties

from dao.DBConnection import Dao
from util import Util
import requests
import json
import wave
import contextlib
import re
from pydub import AudioSegment
from pydub.silence import split_on_silence
import logging

class WitApi:
    def callWitApi(path,filename):
        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)

        logging.basicConfig(filename=configs.get("wit_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')

        # Creating an object
        logger = logging.getLogger()
        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        logger.info("Checking test file exists wit")
        if (path.__contains__("dataset2")):
            i = filename.split("\\")[1].split('-')[1].split('.')[0].lstrip('0')
            if (len(i) == 0):
                i = 0
        try:
            logger.info("Making connection to wit API")
            fname = filename.split("\\")[1]
            fileprocessed, isContentMatched = Dao.dbcall(fname, 'mscdissertation.dbo.Wit_sr')
            if (fileprocessed == True):
                return isContentMatched
            failedrecord = Dao.dbcallForFailedRecord(fname, 'WitAPI', 'mscdissertation.dbo.FailedRecords')
            if (failedrecord == True):
                return -1
            API_ENDPOINT = path.__contains__("API_ENDPOINT")
            ACCESS_TOKEN = path.__contains__("ACCESS_TOKEN")
            headers = {'authorization': 'Bearer ' + ACCESS_TOKEN,
                       'Content-Type': 'audio/wav'}

            logger.info("Calling wit API")


            with contextlib.closing(wave.open(filename, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                print(duration)
                if(duration<18):
                    with open(filename, 'rb') as f:
                        audio = f.read()
                        resp = requests.post(API_ENDPOINT, headers=headers,data=audio)
                        data = json.loads(resp.content)
                        text = data['text'].lower()
                        text = re.sub(r'[^\w\s]', '', text)
                        text = text.replace("'", "")
                        print(text)
                        audiotxtarr = text.split()
                        logging.info("Calling util Compare Function wit")
                    if(path.__contains__("dataset1")):
                        isContentMatched, listToStr = Util.Util.compareText(audiotxtarr)
                    else:
                         filename = filename.split('\\')[1].split('.')[0]
                         isContentMatched,listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
                    logging.info('calling on db conn wit')
                    Dao.insertrecord(fname, text, isContentMatched, listToStr,
                                             'mscdissertation.dbo.Wit_sr')
                    return isContentMatched
                else:
                    t =''
                    print(filename + ": duration is more than 18")
                    parent = 'C:/Dissertationcode/wit/split'
                    directory = filename.split('\\')[1]
                    path1 = os.path.join(parent, directory)
                    if (os.path.isdir(path1) != True):
                        os.mkdir(path1)
                    print("Directory '% s' created" % path1)
                    sound_file = AudioSegment.from_wav(filename)
                    audio_chunks = split_on_silence(sound_file, min_silence_len=600, silence_thresh=-40)
                    for j, chunk in enumerate(audio_chunks):
                        out_file = path1 + "/chunk{0}.wav".format(j)
                        print("exporting", out_file)
                        if (os.path.isfile(out_file) != True):
                            chunk.export(out_file, format="wav")
                        with open(out_file, 'rb') as f:
                            audio = f.read()
                            resp = requests.post(API_ENDPOINT, headers=headers, data=audio)
                            data = json.loads(resp.content)
                            text = data['text'].lower()
                            text = re.sub(r'[^\w\s]', '', text)
                            text = text.replace("'", "")
                            t = t +' '+text
                            print(t)
                    audiotxtarr = t.split()
                    logging.info("Calling util Compare Function wit")
                    if(path.__contains__("dataset1")):
                        isContentMatched, listToStr = Util.Util.compareText(audiotxtarr)
                    else:
                        filename = filename.split('\\')[1].split('.')[0]
                        isContentMatched,listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
                    logging.info('calling on db conn wit')
                    Dao.insertrecord(fname, t, isContentMatched, listToStr,'mscdissertation.dbo.Wit_sr')
                    return isContentMatched
        except Exception as e:
            Dao.insertFailRecords(fname, 'WitAPI', " WIT API fail")
            logger.error(fname + ": WIT API fail")
            return -1




