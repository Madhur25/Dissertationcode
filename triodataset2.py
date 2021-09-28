import csv
import glob
import os
import boto3
from jproperties import Properties

import speechApi.IbmApi
import speechApi.WitApi
import speechApi.GoogleApi



configs = Properties()
with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
    configs.load(config_file)


def trioMainDatset2():
    # Google,IBM,wit trio ensemble
    # Creating lists to store the results from different APIs

    go = []
    ib = []
    wi = []
    fname = []
    # checking file 'google_ibm_wit_trio_dataset2' exits
    if (os.path.isfile(configs.get("google_ibm_wit_trio_dataset2").data)):
        pass
    else:
        # Calling Google API
        path = configs.get("dataset2Converted").data
        for filename in glob.glob(os.path.join(path, '*.wav')):
            x = speechApi.GoogleApi.GoogleApi
            a = x.callGoogleAPI(path, filename)
            # Adding Result to list
            go.append(a)

            # Calling Wit API
            y = speechApi.WitApi.WitApi
            b = y.callWitApi(path, filename)
            # Adding Result to list
            wi.append(b)
            fname.append(filename.split("\\")[1])
        print(go)
        print(wi)
        print(fname)
        # Calling IBM API
        path = configs.get("dataset2").data
        for filename in glob.glob(os.path.join(path, '*.mp3')):
            x = speechApi.IbmApi.IbmApi
            a = x.callIbmAPI(path, filename)
            # Adding result to list
            ib.append(a)
        print(ib)
        # writing the all three APIs into file
        with open(configs.get("google_ibm_wit_trio_dataset2").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'GoogleAPI', 'IBMAPI', 'WitAPI'])
            i = 0
            for fn in fname:
                print(fn)
                writer.writerow([fn, go[i], wi[i], ib[i]])
                i = i + 1

        f.close()


    # amazon,azure,houndify trio
    # # Creating lists to store the results from different APIs
    az = []
    am = []
    ho = []
    fname = []
    # checking file 'amazon_azure_houndify_trio_dataset2' exits
    if (os.path.isfile(configs.get("amazon_azure_houndify_trio_dataset2").data)):
        pass
    else:
        # Calling Amazon API
        path = configs.get("aws_s3_dataset2").data
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(path.split('/')[3])
        summaries = my_bucket.objects.all()
        job_name = 'mscdissertation'
        for file in summaries:
            b = speechApi.AmazonApi.AmazonApi
            c = b.callAmazonApi(path, file, job_name)
            # Adding result to list
            am.append(c)
        print(am)
        # Calling the Houndify API and Azure API
        path = configs.get("dataset2Converted").data
        for filename in glob.glob(os.path.join(path, '*.wav')):
            x = speechApi.HoundifyApi.HoundifyApi
            a = x.callHoundifyApi(path, filename)
            # Adding result to list
            ho.append(a)

            y = speechApi.AzureApi.AzureApi
            b = y.callAzureApi(path, filename)
            # Adding result to list
            az.append(b)
            fname.append(filename.split("\\")[1])
        print(ho)
        print(az)
        print(fname)
        # writing the all three APIs into file
        with open(configs.get("amazon_azure_houndify_trio_dataset2").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'AmazonAPI', 'AzureAPI', 'HoundifyAPI'])
            i = 0
            for fn in fname:
                print(fn)
                writer.writerow([fn, am[i], az[i], ho[i]])
                i = i + 1

        f.close()


    # sphinx azure houndify
    # creating list to store the results from different APIs
    az1 = []
    sp = []
    ho1 = []
    fname = []
    # checking file 'sphinx_azure_houndify_trio_dataset2' exits
    if (os.path.isfile(configs.get("sphinx_azure_houndify_trio_dataset2").data)):
        pass
    else:
        # Calling Houndify API, Azure API, Sphinx API
        path = configs.get("dataset2Converted").data
        for filename in glob.glob(os.path.join(path, '*.wav')):
            x = speechApi.HoundifyApi.HoundifyApi
            a = x.callHoundifyApi(path, filename)
            # Adding result to list
            ho1.append(a)

            y = speechApi.AzureApi.AzureApi
            b = y.callAzureApi(path, filename)
            # Adding result to list
            az1.append(b)
            fname.append(filename.split("\\")[1])

            z = speechApi.SphixApi.SphixAPI
            c = z.callSphixAPI(path, filename)
            # Adding result to list
            sp.append(c)

        print(ho1)
        print(az1)
        print(fname)
        # writing the all three APIs into file
        with open(configs.get("sphinx_azure_houndify_trio_dataset2").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'SphinxAPI', 'AzureAPI', 'HoundifyAPI'])
            i = 0
            for fn in fname:
                print(fn)
                writer.writerow([fn, sp[i], az1[i], ho1[i]])
                i = i + 1

        f.close()


    # amazon,azure,google trio
    # creating list to store the results from different APIs
    az2 = []
    am1 = []
    go1 = []
    fname = []
    # checking file 'amazon_azure_google_trio_dataset2' exits
    if (os.path.isfile(configs.get("amazon_azure_google_trio_dataset2").data)):
        pass
    else:
        # Calling Amazon API
        path = configs.get("aws_s3_dataset2").data
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(path.split('/')[3])
        summaries = my_bucket.objects.all()
        job_name = 'mscdissertation'
        for file in summaries:
            b = speechApi.AmazonApi.AmazonApi
            c = b.callAmazonApi(path, file, job_name)
            # Adding result to list
            am1.append(c)
        print(am1)
        # Calling Google API and Azure API
        path = configs.get("dataset2Converted").data
        for filename in glob.glob(os.path.join(path, '*.wav')):
            x = speechApi.GoogleApi.GoogleApi
            a = x.callGoogleAPI(path, filename)
            # Adding result to list
            go1.append(a)

            y = speechApi.AzureApi.AzureApi
            b = y.callAzureApi(path, filename)
            # Adding result to list
            az2.append(b)
            fname.append(filename.split("\\")[1])
        print(go1)
        print(az2)
        print(fname)
        # writing the all three APIs into file
        with open(configs.get("amazon_azure_google_trio_dataset2").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'AmazonAPI', 'AzureAPI', 'GoogleAPI'])
            i = 0
            for fn in fname:
                print(fn)
                writer.writerow([fn, am1[i], az2[i], go1[i]])
                i = i + 1

        f.close()






