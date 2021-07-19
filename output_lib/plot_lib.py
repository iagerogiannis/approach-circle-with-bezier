import os
import matplotlib.pyplot as plt


class PlotExporter:

    def __init__(self, path=None, file_type="png"):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.file_type = file_type

    def create_plot(self, *plots, title=None, x_label=None, y_label=None,
                    axes_equal=False, x_lim=[-.5, 4.], y_lim=[-2., 2.]):
        plt.xlim(*x_lim)
        plt.ylim(*y_lim)
        if axes_equal:
            plt.axis('square')
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
