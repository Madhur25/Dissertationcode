import re
import os
import pandas as pd
from jproperties import Properties

configs = Properties()
with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
    configs.load(config_file)


class Util:

    def convertfiletolower ():
        readfile = open(configs.get("reading_passage").data, "r")
        res = re.sub(r'[^\w\s]', '', readfile.read())
        res.replace("'","")
        print(res.lower())
        file = open({configs.get("test_file").data}, "w")
        file.write(res.lower())
        file.close()

    def compareText(audiotxtarr):
        isContentMatched = 0
        with open(configs.get("test_file").data) as f1:
            for line in f1:
                orginalarr = line.split()
                finalarr = list(set(orginalarr) - set(audiotxtarr)) + list(set(audiotxtarr) - set(orginalarr))
                print(finalarr)
                listToStr = ' '.join(map(str, finalarr))
                if (len(listToStr) != 0):
                    isContentMatched = 0
                else:
                    isContentMatched = 1
        return (isContentMatched,listToStr)

    def checkForFile():
        print("Checking test file exists")
        if (os.path.isfile(configs.get("test_file").data)):
            pass
        else:
            Util.convertfiletolower()

    def compareDataFromExcel(audiotxtarr,filename,i):
        df = pd.read_csv(configs.get("cv_valid_dev").data)
        text = df['text'].where(df['filename'] == f'cv-valid-dev/{filename}.mp3'.format(filename))
        text = text[i].lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = text.replace("'", '')
        print(text.split())
        orginalarr = text.split()
        finalarr = list(set(orginalarr) - set(audiotxtarr)) + list(set(audiotxtarr) - set(orginalarr))
        print(finalarr)
        listToStr = ' '.join(map(str, finalarr))
        if (len(listToStr) != 0):
            isContentMatched = 0
        else:
            isContentMatched = 1
        return (isContentMatched, listToStr)

