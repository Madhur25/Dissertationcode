import speech_recognition as sr
import os

from jproperties import Properties

from dao.DBConnection import Dao
from util import Util
import logging
import wave
import contextlib
import re
from pydub import AudioSegment
from pydub.silence import split_on_silence

class HoundifyApi:
    def callHoundifyApi(path,filename):

        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)

        logging.basicConfig(filename=configs.get("houndify_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')

        # Creating an object
        logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        fname = filename.split("\\")[1]
        print(fname)
        fileprocessed, isContentMatched = Dao.dbcall(fname, 'mscdissertation.dbo.Houndify_sr')
        if (fileprocessed == True):
            return isContentMatched
        failedrecord = Dao.dbcallForFailedRecord(fname, 'HoundifyAPI', 'mscdissertation.dbo.FailedRecords')
        if (failedrecord == True):
            return -1
        r = sr.Recognizer()
        HOUNDIFY_CLIENT_ID = path.__contains__("HOUNDIFY_CLIENT_ID")
        HOUNDIFY_CLIENT_KEY = path.__contains__("HOUNDIFY_CLIENT_KEY")

        logger.info("Checking test file exists Houndify")
        if (path.__contains__("dataset2")):
            i = filename.split("\\")[1].split('-')[1].split('.')[0].lstrip('0')
            if (len(i) == 0):
                i = 0
        try:
            logger.info("Calling Houndify API")
            #i = 3587



            with contextlib.closing(wave.open(filename, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                print(duration)
                if(duration<25):
                    with sr.AudioFile(filename) as source:
                        audio = r.listen(source)
                        text = r.recognize_houndify(audio,client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
                        text = text.lower()
                        text = re.sub(r'[^\w\s]', '', text)
                        text = text.replace("'", "")
                        print(text)
                        audiotxtarr = text.split()
                    logger.info("Calling util Compare Function Houndify")
                    if(path.__contains__("dataset1")):
                        isContentMatched,listToStr = Util.Util.compareText(audiotxtarr)
                    else:
                        filename = filename.split('\\')[1].split('.')[0]
                        isContentMatched, listToStr = Util.Util.compareDataFromExcel(audiotxtarr,filename,int(i))
                        logger.info('calling on db conn')
                    Dao.insertrecord(fname, text, isContentMatched, listToStr, 'mscdissertation.dbo.Houndify_sr')

                else:
                    t = ''
                    print(filename + ": duration is more than 25")
                    parent = 'C:/Dissertationcode/houndify/split'
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
                        with sr.AudioFile(out_file) as source:
                            audio = r.listen(source)
                            text = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID,
                                                            client_key=HOUNDIFY_CLIENT_KEY)
                            text = text.lower()
                            text = re.sub(r'[^\w\s]', '', text)
                            text = text.replace("'", "")
                            print(text)
                            t = t + ' ' + text
                            print(t)
                    audiotxtarr = t.split()
                    logging.info("Calling util Compare Function wit")
                    if (path.__contains__("dataset1")):
                        isContentMatched, listToStr = Util.Util.compareText(audiotxtarr)
                    else:
                        filename = filename.split('\\')[1].split('.')[0]
                        isContentMatched, listToStr = Util.Util.compareDataFromExcel(audiotxtarr, filename,int(i))
                        logging.info('calling on db conn wit')
                    Dao.insertrecord(fname, t, isContentMatched, listToStr, 'mscdissertation.dbo.Houndify_sr')
                    return isContentMatched

        except Exception as e:
            Dao.insertFailRecords(fname, 'HoundifyAPI', " Houndify API fail")
            return -1
            logger.error(fname + ": Houndify API fail")






