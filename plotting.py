# Shabnam Nazmi.
# Graduate research assistant at electrical and computer engineering department,
# North Carolina A&T State University, Greensboro, NC.
# snazmi@aggies.ncat.edu.
#
# ------------------------------------------------------------------------------
import os.path

import numpy as np
import matplotlib.pyplot as plt

from config import *


class PlotTrack:
    def __init__(self):
        self.records = np.zeros([int(MAX_ITERATION/TRACK_FREQ), 3])

    def plot_records(self, records):
        for i in range(records.__len__()):
            record = records[i]
            for j in range(int(MAX_ITERATION / TRACK_FREQ)):
                try:
                    self.records[j] += record[j]
                except IndexError:
                    self.records[j] += record[-1]
        self.records /= float(records.__len__())

        iterations = range(TRACK_FREQ, MAX_ITERATION + TRACK_FREQ, TRACK_FREQ)
        train_f = self.records[:, 1]
        test_f = self.records[:, 2]
        plt.plot(iterations, train_f, label='train f-score')
        plt.plot(iterations, test_f, label='test f-score')
        plt.xlabel('Iteration')
        plt.ylabel('F-score')
        plt.legend()
        fig_name = str(MAX_CLASSIFIER) + '-' + str(PROB_HASH) + '.png'
        plt.savefig(os.path.join(os.path.curdir, REPORT_PATH, DATA_HEADER, 'params-' + str(MAX_CLASSIFIER) +
                                 '-' + str(PROB_HASH), fig_name), bbox_inches='tight')
        plt.close()
