import pandas as pd
import csv
import glob
from jproperties import Properties

configs = Properties()
with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
    configs.load(config_file)

 # function Adjudicate the results of duo ensemble method
def duoAdjudicate():
    # calculte the majority in the result of ensemble and return the adjudicate result.
    def calVote(api1, api2):
        lst = []
        api1Result = 0 if (api1 == 'False') else (-1 if (api1 == '-1') else 1)
        api2Result = 0 if str(api2) == 'False' else (-1 if (api2 == '-1') else 1)
        lst.append(api1Result)
        lst.append(api2Result)
        sum = api1Result + api2Result
        if (sum == -2):
            return 'Reject'
        if (sum == 2):
            return True
        if (sum == 0):
            return True if lst.__contains__(-1) else False
        if (sum == 1):
            return "Don't Know"
        if (sum == -1):
            return False if lst.__contains__(-1) else 'Reject'
        return False

    # reading the ensemble results file and call calvote funtion
    path = configs.get("duoresult").data # use your path
    all_files = glob.glob(path + "/*.csv")
    for filename in all_files:
        if(filename.__contains__('google')):
            df = pd.read_csv(filename)
            with open(configs.get("google_azure_duo_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['GoogleAPI'], row['AzureAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if(filename.__contains__('houndify')):
            df = pd.read_csv(filename)
            with open(configs.get("houndify_azure_duo_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['HoundifyAPI'], row['AzureAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if (filename.__contains__('ibm')):
            df = pd.read_csv(filename)
            with open(configs.get("ibm_amazon_duo_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['IBMAPI'], row['AmazonAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if (filename.__contains__('wit')):
            df = pd.read_csv(filename)
            with open(configs.get("wit_sphinx_duo_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['WitAPI'], row['SphixAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if (filename.__contains__('amazon') and filename.__contains__('azure')):
            df = pd.read_csv(filename)
            with open(configs.get("amazon_azure_duo_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['AzureAPI'], row['AmazonAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()

# This funtion calculate the accuracies
def calAccuracy():
    with open(configs.get("duoaccuracy").data, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ensemble', 'True Recognition','False Recognition','File Error/Reject','Dont Know'])
        path = configs.get("adjudicateResultduo").data  # use your path
        all_files = glob.glob(path + "/*.csv")
        for filename in all_files:
            print(filename)
            df = pd.read_csv(filename)
            print((df['Result'] == 'True').sum())
            trueCount = (df['Result'] == 'True').sum()
            accurary = (trueCount / df['Result'].count()) * 100
            print(accurary)
            print((df['Result'] == 'False').sum())
            falseCount = (df['Result'] == 'False').sum()
            falseaccurary = (falseCount / df['Result'].count()) * 100
            print(falseaccurary)
            print((df['Result'] == "Don't Know").sum())
            dontKnowCount = (df['Result'] == "Don't Know").sum()
            dontKnowAccuracy = (dontKnowCount / df['Result'].count()) * 100
            print(dontKnowAccuracy)
            writer.writerow([filename.split('\\')[1].split('.')[0],accurary,falseaccurary,0,dontKnowAccuracy])
    f.close()









