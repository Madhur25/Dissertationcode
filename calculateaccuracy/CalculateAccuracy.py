import pandas as pd
import os
from jproperties import Properties
import csv

class CalculateAccuracy:

    def calAccuracyAPI():
        configs = Properties()
        with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
            configs.load(config_file)

        with open(configs.get("singleapiaccuracy").data, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['APIName', 'True Recognition', 'False Recognition', 'File Error/Reject'])

            if (os.path.isfile(configs.get("amazon_azure_google_trio_combine").data)):
                df = pd.read_csv(configs.get("amazon_azure_google_trio_combine").data)
                print((df['AmazonAPI'] == True).sum())
                trueCount = (df['AmazonAPI'] == True).sum()
                accurary = (trueCount / df['AmazonAPI'].count()) * 100
                falseCount = (df['AmazonAPI'] == False).sum()
                falseaccurary = (falseCount / df['AmazonAPI'].count()) * 100
                errorCount = (df['AmazonAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['AmazonAPI'].count()) * 100
                writer.writerow(['Amazon', accurary, falseaccurary,erroraccurary])

                print('amazon api accuracy {}'.format(accurary))
                print((df['GoogleAPI'] == 'True').sum())
                trueCount = (df['GoogleAPI'] == 'True').sum()
                accurary = (trueCount / df['GoogleAPI'].count()) * 100
                print('google api accuracy {}'.format(accurary))
                falseCount = (df['GoogleAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['GoogleAPI'].count()) * 100
                errorCount = (df['GoogleAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['GoogleAPI'].count()) * 100
                writer.writerow(['Google', accurary, falseaccurary, erroraccurary])


                print((df['AzureAPI'] == True).sum())
                trueCount = (df['AzureAPI'] == True).sum()
                accurary = (trueCount / df['AzureAPI'].count()) * 100
                print('azure api accuracy {}'.format(accurary))
                falseCount = (df['AzureAPI'] == False).sum()
                falseaccurary = (falseCount / df['AzureAPI'].count()) * 100
                errorCount = (df['AzureAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['AzureAPI'].count()) * 100
                writer.writerow(['Azure', accurary, falseaccurary, erroraccurary])

            else:
                path1 = configs.get("amazon_azure_google_trio_dataset1").data
                path2 = configs.get("amazon_azure_google_trio_dataset2").data
                df1 = pd.read_csv(path1)
                df2 = pd.read_csv(path2)
                out = df1.append(df2)
                with open(configs.get("amazon_azure_google_trio_combine").data, 'a', newline='') as f:
                    out.to_csv(f, index=False)
                df = pd.read_csv(configs.get("amazon_azure_google_trio_combine").data)
                print((df['AmazonAPI'] == True).sum())
                trueCount = (df['AmazonAPI'] == True).sum()
                accurary = (trueCount / df['AmazonAPI'].count()) * 100
                falseCount = (df['AmazonAPI'] == False).sum()
                falseaccurary = (falseCount / df['AmazonAPI'].count()) * 100
                errorCount = (df['AmazonAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['AmazonAPI'].count()) * 100
                writer.writerow(['Amazon', accurary, falseaccurary, erroraccurary])

                print('amazon api accuracy {}'.format(accurary))
                print((df['GoogleAPI'] == 'True').sum())
                trueCount = (df['GoogleAPI'] == 'True').sum()
                accurary = (trueCount / df['GoogleAPI'].count()) * 100
                print('google api accuracy {}'.format(accurary))
                falseCount = (df['GoogleAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['GoogleAPI'].count()) * 100
                errorCount = (df['GoogleAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['GoogleAPI'].count()) * 100
                writer.writerow(['Google', accurary, falseaccurary, erroraccurary])

                print((df['AzureAPI'] == True).sum())
                trueCount = (df['AzureAPI'] == True).sum()
                accurary = (trueCount / df['AzureAPI'].count()) * 100
                print('azure api accuracy {}'.format(accurary))
                falseCount = (df['AzureAPI'] == False).sum()
                falseaccurary = (falseCount / df['AzureAPI'].count()) * 100
                errorCount = (df['AzureAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['AzureAPI'].count()) * 100
                writer.writerow(['Azure', accurary, falseaccurary, erroraccurary])

            if(os.path.isfile(configs.get("google_ibm_wit_trio_combine").data)):
                df = pd.read_csv(configs.get("google_ibm_wit_trio_combine").data)
                print((df['IBMAPI'] == 'True').sum())
                trueCount = (df['IBMAPI'] == 'True').sum()
                accurary = (trueCount / df['IBMAPI'].count()) * 100
                print('ibm api accuracy {}'.format(accurary))
                falseCount = (df['IBMAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['IBMAPI'].count()) * 100
                errorCount = (df['IBMAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['IBMAPI'].count()) * 100
                writer.writerow(['IBM', accurary, falseaccurary, erroraccurary])

                print((df['WitAPI'] == 'True').sum())
                trueCount = (df['WitAPI'] == 'True').sum()
                accurary = (trueCount / df['WitAPI'].count()) * 100
                print('wit api accuracy {}'.format(accurary))
                falseCount = (df['WitAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['WitAPI'].count()) * 100
                errorCount = (df['WitAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['WitAPI'].count()) * 100
                writer.writerow(['Wit', accurary, falseaccurary, erroraccurary])

            else:
                path1 = configs.get("google_ibm_wit_trio_dataset1").data
                path2 = configs.get("google_ibm_wit_trio_dataset2").data
                df1 = pd.read_csv(path1)
                df2 = pd.read_csv(path2)
                out = df1.append(df2)
                with open(configs.get("google_ibm_wit_trio_combine").data, 'a', newline='') as f:
                    out.to_csv(f, index=False)
                df = pd.read_csv(configs.get("google_ibm_wit_trio_combine").data)
                print((df['IBMAPI'] == 'True').sum())
                trueCount = (df['IBMAPI'] == 'True').sum()
                accurary = (trueCount / df['IBMAPI'].count()) * 100
                print('ibm api accuracy {}'.format(accurary))
                falseCount = (df['IBMAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['IBMAPI'].count()) * 100
                errorCount = (df['IBMAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['IBMAPI'].count()) * 100
                writer.writerow(['IBM', accurary, falseaccurary, erroraccurary])

                print((df['WitAPI'] == 'True').sum())
                trueCount = (df['WitAPI'] == 'True').sum()
                accurary = (trueCount / df['WitAPI'].count()) * 100
                print('wit api accuracy {}'.format(accurary))
                falseCount = (df['WitAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['WitAPI'].count()) * 100
                errorCount = (df['WitAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['WitAPI'].count()) * 100
                writer.writerow(['Wit', accurary, falseaccurary, erroraccurary])

            if (os.path.isfile(configs.get("sphinx_azure_houndify_trio_combine").data)):
                df = pd.read_csv(configs.get("sphinx_azure_houndify_trio_combine").data)
                print((df['SphinxAPI'] == 'True').sum())
                trueCount = (df['SphinxAPI'] == 'True').sum()
                accurary = (trueCount / df['SphinxAPI'].count()) * 100
                print('SphinxAPI api accuracy {}'.format(accurary))
                falseCount = (df['SphinxAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['SphinxAPI'].count()) * 100
                errorCount = (df['SphinxAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['SphinxAPI'].count()) * 100
                writer.writerow(['Sphinx', accurary, falseaccurary, erroraccurary])

                print((df['HoundifyAPI'] == 'True').sum())
                trueCount = (df['HoundifyAPI'] == 'True').sum()
                accurary = (trueCount / df['HoundifyAPI'].count()) * 100
                print('HoundifyAPI api accuracy {}'.format(accurary))
                falseCount = (df['HoundifyAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['HoundifyAPI'].count()) * 100
                errorCount = (df['HoundifyAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['HoundifyAPI'].count()) * 100
                writer.writerow(['Houndify', accurary, falseaccurary, erroraccurary])

            else:
                path1 = configs.get("sphinx_azure_houndify_trio_dataset1").data
                path2 = configs.get("sphinx_azure_houndify_trio_dataset2").data
                df1 = pd.read_csv(path1)
                df2 = pd.read_csv(path2)
                out = df1.append(df2)
                with open(configs.get("sphinx_azure_houndify_trio_combine").data, 'a', newline='') as f:
                    out.to_csv(f, index=False)
                df = pd.read_csv(configs.get("sphinx_azure_houndify_trio_combine").data)
                print((df['SphinxAPI'] == 'True').sum())
                trueCount = (df['SphinxAPI'] == 'True').sum()
                accurary = (trueCount / df['SphinxAPI'].count()) * 100
                print('SphinxAPI api accuracy {}'.format(accurary))
                falseCount = (df['SphinxAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['SphinxAPI'].count()) * 100
                errorCount = (df['SphinxAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['SphinxAPI'].count()) * 100
                writer.writerow(['Sphinx', accurary, falseaccurary, erroraccurary])

                print((df['HoundifyAPI'] == 'True').sum())
                trueCount = (df['HoundifyAPI'] == 'True').sum()
                accurary = (trueCount / df['HoundifyAPI'].count()) * 100
                print('HoundifyAPI api accuracy {}'.format(accurary))
                falseCount = (df['HoundifyAPI'] == 'False').sum()
                falseaccurary = (falseCount / df['HoundifyAPI'].count()) * 100
                errorCount = (df['HoundifyAPI'] == str(-1)).sum()
                erroraccurary = (errorCount / df['HoundifyAPI'].count()) * 100
                writer.writerow(['Houndify', accurary, falseaccurary, erroraccurary])
        f.close()




