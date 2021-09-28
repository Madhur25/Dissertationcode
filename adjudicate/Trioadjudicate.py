import pandas as pd
import csv
import glob
from jproperties import Properties


#  Adjudicate the results of trio ensemble method
def trioAdjudicate():
    configs = Properties()
    with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
        configs.load(config_file)
        # calculte the majority in the result of ensemble and return the adjudicate result.
    def calVote(api1, api2, api3):
        lst = []
        api1Result = 0 if (api1 == 'False') else (-1 if (api1 == '-1') else 1)
        api2Result = 0 if str(api2) == 'False' else (-1 if (api2 == '-1') else 1)
        api3Result = 0 if api3 == 'False' else (-1 if (api3 == '-1') else 1)
        lst.append(api1Result)
        lst.append(api2Result)
        lst.append(api3Result)
        sum = api1Result + api2Result + api3Result
        if (sum <= -2):
            return 'Reject'
        if (sum >= 2):
            return True
        if (sum == 0):
            return "Don't Know" if lst.__contains__(-1) else False
        if (sum == 1):
            return True if lst.__contains__(-1) else False
        if (sum == -1):
            return 'Reject' if lst.count(-1) == 2 else False
        return False

    # reading the ensemble results file and call calvote funtion
    path = configs.get("trioresult").data
    all_files = glob.glob(path + "/*.csv")
    for filename in all_files:
        print(filename)
        if(filename.__contains__('google') and filename.__contains__('amazon')):
            df = pd.read_csv(filename)
            with open(configs.get("amazon_azure_google_trio_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['AmazonAPI'], row['AzureAPI'], row['GoogleAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if (filename.__contains__('houndify') and filename.__contains__('amazon')):
            df = pd.read_csv(filename)
            with open(configs.get("amazon_azure_houndify_trio_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['AmazonAPI'], row['AzureAPI'], row['HoundifyAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if (filename.__contains__('google') and filename.__contains__('ibm')):
            df = pd.read_csv(filename)
            with open(configs.get("google_ibm_wit_trio_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['GoogleAPI'], row['IBMAPI'], row['WitAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()
        if(filename.__contains__('sphinx') and filename.__contains__('azure')):
            df = pd.read_csv(filename)
            with open(configs.get("sphinx_azure_houndify_trio_adjudicate").data, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Filename', 'Result'])
                for index, row in df.iterrows():
                    vote = calVote(row['SphinxAPI'], row['AzureAPI'], row['HoundifyAPI'])
                    print(row['Filename'], vote)
                    writer.writerow([row['Filename'], vote])
            f.close()

# This function calculate the accuracies
def calAccuracy():
    configs = Properties()
    with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
        configs.load(config_file)
    with open(configs.get("trioaccuracy").data, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ensemble', 'True Recognition','False Recognition','File Error/Reject','Dont Know'])
        path = configs.get("adjudicateResult").data
        all_files = glob.glob(path + "/*.csv")

        for filename in all_files:
            print(filename)
            df = pd.read_csv(filename)
            print(df.dtypes['Result'])
            if(df.dtypes['Result'] == 'bool'):
                print((df['Result'] == True).sum())
                trueCount = (df['Result'] == True).sum()
            else:
                print((df['Result'] == 'True').sum())
                trueCount = (df['Result'] == 'True').sum()
            accurary = (trueCount / df['Result'].count()) * 100
            print('True accuract {}'.format(accurary))

            print((df['Result'] == 'False').sum())
            falsecount = (df['Result'] == 'False').sum()
            falseaccurary = (falsecount / df['Result'].count()) * 100
            print(falseaccurary)

            print((df['Result'] == 'Reject').sum())
            rejectCount= (df['Result'] == 'Reject').sum()
            rejectaccurary = (rejectCount / df['Result'].count()) * 100
            print(rejectaccurary)

            print((df['Result'] ==  "Don't Know").sum())
            dnCount = (df['Result'] ==  "Don't Know").sum()
            dnAccuracy = (dnCount / df['Result'].count()) * 100
            print(dnAccuracy)
            writer.writerow([filename.split('\\')[1].split('.')[0], accurary, falseaccurary,rejectaccurary , dnAccuracy])
    f.close()




