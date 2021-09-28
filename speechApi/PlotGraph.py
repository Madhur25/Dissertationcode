import matplotlib.pyplot as plt
from jproperties import Properties
import csv
import glob
import pandas as pd

def plotGraph():
    configs = Properties()
    with open('C:/Dissertationcode/path.properties', 'rb') as config_file:
        configs.load(config_file)
    path = configs.get("accuracyfile").data
    all_files = glob.glob(path + "/*.csv")
    for filename in all_files:
        fname = filename.split('\\')[1].split('.')[0]
        if (fname == 'singleapiaccuracy'):
            df = pd.read_csv(filename)
            print(df)
            plt.figure(figsize=(20, 10))
            plt.plot(df['APIName'], df['True Recognition'], label="True Recognition")
            plt.plot(df['APIName'], df['False Recognition'], label="False Recognition")
            plt.plot(df['APIName'], df['File Error/Reject'], label="File Error")
            plt.xlabel('x - axis')
            # naming the y axis
            plt.ylabel('y - axis')
            # giving a title to my graph
            plt.title('Individual API Accuracy')
            # show a legend on the plot
            plt.legend()
            plt.savefig(path+'singleapi.png')
            # function to show the plot
            plt.show()


        else:
            df = pd.read_csv(filename)
            fname = filename.split('\\')[1].split('.')[0].split('a')[0].upper()
            print(df)
            plt.figure(figsize=(20,10))
            plt.plot(df['Ensemble'], df['True Recognition'], label="True Recognition")
            plt.plot(df['Ensemble'], df['False Recognition'], label="False Recognition")
            plt.plot(df['Ensemble'], df['File Error/Reject'], label="File Error")
            plt.xlabel('x - axis')
            # naming the y axis
            plt.ylabel('y - axis')
            # giving a title to my graph
            plt.title('{} Ensemble Accuracy'.format(fname))
            # show a legend on the plot
            plt.legend()

            plt.savefig(path+'{}.png'.format(fname))
            # function to show the plot

            plt.show()


