import sys 
import pandas as pd
import numpy as np


# Relative paths = run this module from where it lives
datafilename = 'Automatically Generated Code Summary Survey (Responses) - Form Responses 1.csv'

numFuncs = 15

numExperiments = 3


# def readCSVFile(filename):
#     codingExps = []
#     javaExps = []
#     comments = []
#     with open(filename) as f:
#         for line in f:
#             if (line[0] == 'T'): continue  # dumb way to skip header line
#             values = line.split(',')
#             codingExps.append(float(values[1]))
#             javaExps.append(float(values[2]))
#             comments.append(values[-1])


def main():
    df = pd.read_csv(datafilename)

    # for col in df.columns:
    #     print(col)    
    #     print(df[col])

    relAvgs = np.zeros((numExperiments, numFuncs))
    simAvgs = np.zeros((numExperiments, numFuncs))
    natAvgs = np.zeros((numExperiments, numFuncs))

    col = 3
    for func in range(numFuncs):
        for exp in range(numExperiments):
            relAvgs[exp][func] = df[df.columns[col]].mean()
            col += 1
            simAvgs[exp][func] = df[df.columns[col]].mean()
            col += 1
            natAvgs[exp][func] = df[df.columns[col]].mean()
            col += 1

    for exp in range(numExperiments):
        # print('Rel avgs exp{}: {}'.format(exp, relAvgs[exp]))
        print('Rel avg exp{}: {}'.format(exp, relAvgs[exp].mean()))
        print('Sim avg exp{}: {}'.format(exp, simAvgs[exp].mean()))
        print('Nat avg exp{}: {}'.format(exp, natAvgs[exp].mean()))
        print()



if __name__ == '__main__':
    sys.exit(main()) 

