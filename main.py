import adjudicate.Trioadjudicate
import adjudicate.DuoAdjudicate
import duodataset1
import duodataset2
import triodataset1
import triodataset2
import calculateaccuracy.CalculateAccuracy
from util import Util
import speechApi.PlotGraph


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Util.Util.checkForFile()
    triodataset1.trioMainDatset1()
    triodataset2.trioMainDatset2()
    duodataset1.duoMainDataset1()
    duodataset2.duoMainDataset2()
    adjudicate.Trioadjudicate.trioAdjudicate()
    adjudicate.Trioadjudicate.calAccuracy()
    adjudicate.DuoAdjudicate.duoAdjudicate()
    adjudicate.DuoAdjudicate.calAccuracy()
    calculateaccuracy.CalculateAccuracy.CalculateAccuracy.calAccuracyAPI()
    speechApi.PlotGraph.plotGraph()


























