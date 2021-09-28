import boto3
import time
import urllib
import json
import re
from dao.DBConnection import Dao
from util import Util
import logging
from jproperties import Properties

class AmazonApi:

    def callAmazonApi(path,file,job_name):
        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)
        logging.basicConfig(filename=configs.get("amazon_log").data,
                            format='%(asctime)s %(message)s',
                            filemode='a')
        logging.info("Checking test file exists amazon")
        try:
            print(file.key)
            filename = path + file.key
            fname = filename.split("/")[4]
            fileprocessed,isContentMatched = Dao.dbcall(fname, 'mscdissertation.dbo.Amazon_sr')
            if(fileprocessed == True):
                return isContentMatched
            failedrecord = Dao.dbcallForFailedRecord(fname, 'GoogleAPI', 'mscdissertation.dbo.FailedRecords')
            if (failedrecord == True):
                return -1;
            transcribe_client = boto3.client('transcribe')
            transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': filename},
            MediaFormat='mp3',
            LanguageCode='en-US')
            max_tries = 7
            while max_tries > 0:
                max_tries -= 1
                job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
                job_status = job['TranscriptionJob']['TranscriptionJobStatus']
                if job_status in ['COMPLETED', 'FAILED']:
                    logging.info(f"Job {job_name} is {job_status}.")
                    if job_status == 'COMPLETED':
                        response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                        data = json.loads(response.read())
                        text = data['results']['transcripts'][0]['transcript']
                        text = text.lower()
                        text = re.sub(r'[^\w\s]', '', text)
                        text = text.replace("'", "")
                        print(text)
                        audiotxtarr = text.split()
                    logging.info("Calling util Compare Function amazon")
                    if(path.__contains__("mscdataset1")):
                        isContentMatched, listToStr = Util.Util.compareText(audiotxtarr)
                    else:
                        filename = filename.split('/')[4].split('.')[0]
                        i = filename.split('-')[1].lstrip('0')
                        if (len(i) == 0):
                            i = 0
                        isContentMatched, listToStr = Util.Util.compareDataFromExcel(audiotxtarr, filename,int(i))

                    logging.info('calling on db conn amazon')
                    Dao.insertrecord(fname, text, isContentMatched, listToStr, 'mscdissertation.dbo.Amazon_sr')
                    transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)
                    time.sleep(2)
                    return isContentMatched
                    break
                else:
                    logging.error(f"Waiting for {job_name}. Current status is {job_status}.")
                    time.sleep(10)
        except:
            Dao.insertFailRecords(fname, 'AmazonAPI', " Amazon API fail")
            return -1
            logger.error(fname + ": Google API fail")




