import sys
import json
import random
import numpy as np

# Relative paths = run this module from where it lives
codeFile = '../data/java/test/code.original'
truthFile = '../data/java/test/javadoc.original'
predictionFiles = [
    '../tmp/generated/full_java_beam20220417222507.json',
    '../tmp/generated/full_java_nosym_beam20220417220804.json',
    '../tmp/generated/full_java_2_beam20220419222018.json',
]


def readTextFile(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line)
    return data


def readJsonFile(filename):
    datadict = None
    with open(filename, 'r') as f:
        datadict = json.load(f)
    return list(datadict.values())


def main():
    codes = readTextFile(codeFile)
    truths = readTextFile(truthFile)
    predsList = []
    for predictionFile in predictionFiles:
        predsList.append(readJsonFile(predictionFile))

    # total = 0
    # total2 = 0
    # for code in codes:
    #     total += len(code)
    #     if (len(code) < 300):
    #         print(code)
    #         total2 += 1
    # print('avg:', total / len(codes))
    # print('blah:', total2)

    # print('File lengths:')
    # print('Code:', len(codes))
    # print('Ground truth:', len(truths))
    # for preds in predsList:
    #     print('Prediction:', len(preds))

    # print('=========================')
    limit = len(predsList[0])
    codeLens = []
    dupes = 0
    for candidate in range(limit):
        codeLens.append(len(codes[candidate]))
        truthCandidate = truths[candidate]
        summariesCandidate = [truthCandidate]
        for preds in predsList:
            summariesCandidate.append(preds[candidate])

        dupeFound = False
        for i in range(len(summariesCandidate) - 1):
            for j in range(i+1, len(summariesCandidate)):
                if summariesCandidate[i] == summariesCandidate[j]:
                    dupeFound = True
        if dupeFound: 
            dupes += 1

        # print(codeCandidate)
        # for summary in summariesCandidate:
        #     print(summary)
        # print('=========================')
        # surveyQuestions.append([codeCandidate, summariesCandidate])

    print('Avg code length:', np.array(codeLens).mean())
    print('Dupes: {} out of {}'.format(dupes, limit))


if __name__ == '__main__':
    sys.exit(main()) 

