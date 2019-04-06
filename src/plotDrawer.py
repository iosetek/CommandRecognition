import numpy as np
import matplotlib.pyplot as plt

class PlotDrawer:
    @staticmethod
    def draw(mfcc_data):
        PlotDrawer.__prepare_plot(mfcc_data)
        plt.show()
        # plt.close()

    @staticmethod
    def save(filename, mfcc_data):
        PlotDrawer.__prepare_plot(mfcc_data)
        plt.savefig(filename)
        plt.close()

    @staticmethod
    def __prepare_plot(mfcc_data):
        ig, ax = plt.subplots()
        data= np.swapaxes(mfcc_data, 0 ,1)
        cax = ax.imshow(data, interpolation='nearest', origin='lower', aspect='auto')
        ax.set_title('MFCC')