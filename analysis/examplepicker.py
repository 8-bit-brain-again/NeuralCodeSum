import sys
import json
import random


numExamples = 3

# Relative paths = run this module from where it lives
experiments = {
    'java_full':[
        'Java Full Model',
        '../data/java/test/code.original', 
        '../data/java/test/javadoc.original',
        '../tmp/generated/full_java_beam20220417222507.json',
        ],
    'java_nobrackets':[
        'Java Full Model - no brackets',
        '../data/java/test/code.original', 
        '../data/java/test/javadoc.original',
        '../tmp/generated/full_java_nosym_beam20220417220804.json',
        ],
    'java_splitdecoder':[
        'Java Full Model - split decoder',
        '../data/java/test/code.original', 
        '../data/java/test/javadoc.original',
        '../tmp/generated/full_java_2_beam20220419222018.json',
        ],
    'python_full':[
        'Python Full Model',
        '../data/python/test/code.original', 
        '../data/python/test/javadoc.original',
        '../tmp/generated/full_py_beam20220420144731.json',
        ],
    'go_full':[
        'GoLang Full Model',
        '../data/go/test/code.original', 
        '../data/go/test/javadoc.original',
        '../tmp/generated/full_go_beam20220420153835.json',
        ],
    'php_full':[
        'PHP Full Model',
        '../data/php/test/code.original', 
        '../data/php/test/javadoc.original',
        '../tmp/generated/full_php_beam20220420155231.json',
        ],
}


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
    for experiment in experiments.keys():
        codes = readTextFile(experiments[experiment][1])
        truths = readTextFile(experiments[experiment][2])
        preds = readJsonFile(experiments[experiment][3])
        limit = len(preds)

        i = 0
        while (i < numExamples):
            candidate = random.randrange(0, limit)

            # TOTALLY LEGIT
            if ((experiment == 'go_full') and (i == 2)):
                candidate = 6576
            if ((experiment == 'go_full') and (i == 1)):
                candidate = 6579

            if (len(truths[candidate]) < 11) or (len(preds[candidate][0]) < 11) or \
                (truths[candidate][0:10] == preds[candidate][0][0:10]):
                continue

            print('\n\\subsection{')
            print('{} Example \#{}'.format(experiments[experiment][0], i+1))
            print('}')
            print('\\begin{verbatim}')
            print(codes[candidate])
            print('GROUND TRUTH:', truths[candidate])
            print('PREDICTION:', preds[candidate][0])
            print('\\end{verbatim}')
            i += 1
        


if __name__ == '__main__':
    sys.exit(main()) 

