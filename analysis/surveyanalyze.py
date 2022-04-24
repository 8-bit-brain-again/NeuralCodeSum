import sys 
import pandas as pd
import numpy as np
import scipy.stats
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind

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

# Sourced from https://www.statology.org/f-test-python/
def f_test(x, y):
    x = np.array(x)
    y = np.array(y)
    f = np.var(x, ddof=1)/np.var(y, ddof=1) #calculate F test statistic 
    dfn = x.size-1 #define degrees of freedom numerator 
    dfd = y.size-1 #define degrees of freedom denominator 
    p = 1-scipy.stats.f.cdf(f, dfn, dfd) #find p-value of F test statistic 
    return f, p


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

    print('For N = {}'.format(len(df[df.columns[0]])))

    for exp in range(numExperiments):
        # print('Rel avgs exp{}: {}'.format(exp, relAvgs[exp]))
        print('Rel avg exp{}: {}'.format(exp, relAvgs[exp].mean()))
        print('Sim avg exp{}: {}'.format(exp, simAvgs[exp].mean()))
        print('Nat avg exp{}: {}'.format(exp, natAvgs[exp].mean()))

        if (exp > 0):
            maxU = len(relAvgs[exp]) * len(relAvgs[exp])
            U1, p = mannwhitneyu(relAvgs[exp], relAvgs[0], method="exact")
            U = min(U1, maxU - U1)
            print('Rel vs baseline U = {}, p = {}'.format(U, p))
            U1, p = mannwhitneyu(simAvgs[exp], simAvgs[0], method="exact")
            U = min(U1, maxU - U1)
            print('Sim vs baseline U = {}, p = {}'.format(U, p))
            U1, p = mannwhitneyu(natAvgs[exp], natAvgs[0], method="exact")
            U = min(U1, maxU - U1)
            print('Nat vs baseline U = {}, p = {}'.format(U, p))

            f, f_p = f_test(relAvgs[exp], relAvgs[0])
            if (p > 0.05):
                s, p = ttest_ind(relAvgs[exp], relAvgs[0], equal_var=True)
                print('Rel vs baseline s = {}, p = {}, F-test p = {}'.format(s, p, f_p))
            else:
                s, p = ttest_ind(relAvgs[exp], relAvgs[0], equal_var=False)
                print('Rel vs baseline s = {}, p = {}, F-test p = {}'.format(s, p, f_p))

            f, f_p = f_test(simAvgs[exp], simAvgs[0])
            if (p > 0.05):
                s, p = ttest_ind(simAvgs[exp], simAvgs[0], equal_var=True)
                print('Rel vs baseline s = {}, p = {}, F-test p = {}'.format(s, p, f_p))
            else:
                s, p = ttest_ind(simAvgs[exp], simAvgs[0], equal_var=False)
                print('Rel vs baseline s = {}, p = {}, F-test p = {}'.format(s, p, f_p))

            f, f_p = f_test(natAvgs[exp], natAvgs[0])
            if (p > 0.05):
                s, p = ttest_ind(natAvgs[exp], natAvgs[0], equal_var=True)
                print('Rel vs baseline s = {}, p = {}, F-test p = {}'.format(s, p, f_p))
            else:
                s, p = ttest_ind(natAvgs[exp], natAvgs[0], equal_var=False)
                print('Rel vs baseline s = {}, p = {}, F-test p = {}'.format(s, p, f_p))



        print()


if __name__ == '__main__':
    sys.exit(main()) 

