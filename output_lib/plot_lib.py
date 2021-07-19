import os
import matplotlib.pyplot as plt


class PlotExporter:

    def __init__(self, path=None, file_type="png"):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.file_type = file_type

    def create_plot(self, *plots, title=None, x_label=None, y_label=None,
                    axes_equal=False, x_lim=None, y_lim=None):
        if axes_equal:
            plt.axis('square')
        if x_lim:
            plt.xlim(*x_lim)
        if y_lim:
            plt.ylim(*y_lim)
        for plot in plots:
            plt.plot(plot[0], plot[1])
        if title:
            plt.title(title)
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)

    def show_plot(self):
        plt.show()

    def export_plot(self, fname):
        fname = r"{}/{}.{}".format(self.path, fname, self.file_type)
        plt.savefig(fname)
        plt.clf()
