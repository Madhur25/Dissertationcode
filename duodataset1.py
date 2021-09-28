import csv
import glob
import os

import boto3
from jproperties import Properties

import speechApi.AmazonApi

configs = Properties()
with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
    configs.load(config_file)


def duoMainDataset1():
    # amazon ibm duo dataset1
    # checking file 'ibm_amazon_duo_dataset1' exits
    if (os.path.isfile(configs.get("ibm_amazon_duo_dataset1").data)):
        pass
    else:
        #Calling Amazon api
        path = configs.get("aws_s3_dataset").data
        z = []
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(path.split('/')[3])
        summaries = my_bucket.objects.all()
        job_name = 'mscdissertation'
        for file in summaries:
            b = speechApi.AmazonApi.AmazonApi
            c = b.callAmazonApi(path, file, job_name)
            # Adding result to list
            z.append(c)
        print(z)
        #Calling IBM API
        path1 = configs.get("dataset1").data
        y = []
        fname = []
        for filename in glob.glob(os.path.join(path1, '*.mp3')):
            x = speechApi.IbmApi.IbmApi
            a = x.callIbmAPI(path1, filename)
            # Adding the result to list
            y.append(a)
            fname.append(filename.split("\\")[1])
        print(y)
        print(fname)
        # writing the results to file
        with open(configs.get("ibm_amazon_duo_dataset1").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'IBMAPI', 'AmazonAPI'])
            i = 0
            for fn in fname:
                print(fn)
                writer.writerow([fn, y[i], z[i]])
                i = i + 1

        f.close()


    # google azure duo dataset1
    # Checking file 'google_azure_duo_dataset1' exists or not
    if (os.path.isfile(configs.get("google_azure_duo_dataset1").data)):
        pass
    else:
        # Calling Google and Azure APIs
        path = configs.get("dataset1Converted").data
        with open(configs.get("google_azure_duo_dataset1").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'GoogleAPI', 'AzureAPI'])

            for filename in glob.glob(os.path.join(path, '*.wav')):
                x = speechApi.GoogleApi.GoogleApi
                y = x.callGoogleAPI(path, filename)
                print(y)
                az = speechApi.AzureApi.AzureApi
                z = az.callAzureApi(path, filename)
                print(z)
                # writing the results to file
                writer.writerow([filename.split("\\")[1], y, z])

        f.close()


    # wit sphix duo dataset1
    # Checking file 'wit_sphix_duo_dataset1' exits or not
    if (os.path.isfile(configs.get("wit_sphix_duo_dataset1").data)):
        pass
    else:
        # Calling Wit and Sphinx API
        path = configs.get("dataset1Converted").data
        with open(configs.get("wit_sphix_duo_dataset1").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'WitAPI', 'SphixAPI'])

            for filename in glob.glob(os.path.join(path, '*.wav')):
                x = speechApi.WitApi.WitApi
                y = x.callWitApi(path, filename)
                print(y)
                az = speechApi.SphixApi.SphixAPI
                z = az.callSphixAPI(path, filename)
                print(z)
                # writing the results of both APIs in file
                writer.writerow([filename.split("\\")[1], y, z])

        f.close()


    # azure houndify duo dataset1
    #Checking file 'houndify_azure_duo_dataset1' exits or not
    if (os.path.isfile(configs.get("houndify_azure_duo_dataset1").data)):
        pass
    else:
        # Calling Azure and Houndify API
        path = configs.get("dataset1Converted").data
        with open(configs.get("houndify_azure_duo_dataset1").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'HoundifyAPI', 'AzureAPI'])

            for filename in glob.glob(os.path.join(path, '*.wav')):
                x = speechApi.HoundifyApi.HoundifyApi
                y = x.callHoundifyApi(path, filename)
                print(y)
                az = speechApi.AzureApi.AzureApi
                z = az.callAzureApi(path, filename)
                print(z)
                #writng the results of both APIs in file
                writer.writerow([filename.split("\\")[1], y, z])

        f.close()

    # azure amazon duo dataset1
    # Checking  file 'amazon_azure_duo_dataset1' exits or not
    if (os.path.isfile(configs.get("amazon_azure_duo_dataset1").data)):
        pass
    else:
        # Calling Amazon API
        path = configs.get("aws_s3_dataset").data
        z = []
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(path.split('/')[3])
        summaries = my_bucket.objects.all()
        job_name = 'mscdissertation'
        for file in summaries:
            b = speechApi.AmazonApi.AmazonApi
            c = b.callAmazonApi(path, file, job_name)
            # Adding the result to list
            z.append(c)
        print(z)
        # Calling Azure API
        path1 = configs.get("dataset1Converted").data
        y = []
        fname = []
        for filename in glob.glob(os.path.join(path1, '*.wav')):
            x = speechApi.AzureApi.AzureApi
            a = x.callAzureApi(path1, filename)
            # Adding the result to list
            y.append(a)
            fname.append(filename.split("\\")[1])
        print(y)
        print(fname)
        # Writing both APIs result into file
        with open(configs.get("amazon_azure_duo_dataset1").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Filename', 'AzureAPI', 'AmazonAPI'])
            i = 0
            for fn in fname:
                print(fn)
                writer.writerow([fn, y[i], z[i]])
                i = i + 1

        f.close()



