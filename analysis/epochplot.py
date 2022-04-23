import os
import glob
import sys
import zipfile
import csv
import pathlib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Relative paths = run this module from where it lives
dataDir = '../tmp'
plotsDir = 'epochplots'

experiments = {
    'full_java':'Java Full',
    'full_java_nosym':'Java Full NoBrackets',
    'full_java_2':'Java Full SplitDecoder',
    # 'full_py':'Python Full',
    # 'rnn_py':'Python RNN',
    # 'full_php':'PHP Full',
    # 'full_go':'Go Full',
    # 'full_go_2':'Go Full LR=5e-5',
    # 'full_go_3':'Go Full LR=1e-5',
    # 'full_go_4':'Go Full short tgt_len',
    # 'full_go_5':'Go Full long src_len,tgt_len & small vocab',
    # 'full_go_6':'Go Full 5 but split decoder',
}

fields = [
    'BLEU',
    # 'ROUGE-L',
]

color_list = [
    [0,0,255], 
    [255,0,0],
    [0,255,0],
    [255,0,255],
    [255,255,0],
    [0,255,255],
]


def readFile(filename):
    print('  PARSING: {}'.format(filename))
    data = []
    with open(filename) as f:
        for line in f:
            # Parse the file with naive methods. Using regexs might be more elegant 
            # but those are hurting my head at the moment.
            if ('train: Epoch' in line):
                elements = line.strip().split()
                epochnum = int(elements[6])
                perplexity = float(elements[10])
                ml_loss = float(elements[14])
                time = float(elements[20])
                epochData = [epochnum, perplexity, ml_loss, time]
            if ('dev valid official' in line):
                elements = line.strip().split()
                bleu = float(elements[13])
                rouge_l = float(elements[17])
                precision = float(elements[21])
                recall = float(elements[25])
                f1 = float(elements[29])
                epochData.extend([bleu, rouge_l, precision, recall, f1])
                data.append(epochData)
    df = pd.DataFrame(data, columns = ['Epoch', 'Perplexity', 'ML Loss', 'Time', 'BLEU', 'ROUGE-L', 'Precision', 'Recall', 'F1'])
    # print(df)
    return df


def colorToPlotlyString(color):
    return 'rgb({},{},{})'.format(color[0], color[1], color[2])


def plot(fig, name, data, color):
    fig.add_trace(go.Scatter(x=list(range(len(data))), y=data, 
                    name=name,
                    mode='lines',
                    # mode='lines+markers',
                    marker=dict(size=5, color=colorToPlotlyString(color)),
                    line=dict(color=colorToPlotlyString(color))))
    

def main():
    traceNum = 0
    fig = go.Figure()

    for experiment in experiments.keys():

        filename = os.path.join(dataDir, experiment + '.txt')
        df = readFile(filename)

        for field in fields:
            color = color_list[traceNum % len(color_list)]
            plot(fig, experiments[experiment] + '-' + field, df[field], color)
            traceNum += 1

    fig.update_layout(title='Experiment 2',
                    #   title=' vs. '.join(experiments.values()),
                      xaxis_title='Epoch',
                      yaxis_title='BLEU', 
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

    if not(os.path.exists(plotsDir)): os.makedirs(plotsDir)
    figfilename = os.path.join(plotsDir, ('-'.join(experiments.keys())) + '.png')
    print('WRITING:', figfilename)
    fig.write_image(figfilename)


if __name__ == '__main__':
    sys.exit(main()) 

