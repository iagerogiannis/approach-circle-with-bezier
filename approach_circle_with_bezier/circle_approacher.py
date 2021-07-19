import math
import numpy as np

from numerical_analysis.splines.bezier import Bezier
from numerical_analysis.dependencies import Polynomial
from numerical_analysis.root_finding import newton_raphson_2x2
from numerical_analysis.dependencies.geometry import StraightLine, Circle

from output_lib.csv_lib import ScvExporter
from output_lib.plot_lib import PlotExporter
from output_lib.screen_lib import ScreenPrinter


# Provides a more appropriate parameterization for the specific application
class CustomCircle(Circle):
    def x_t(self, t): return self.R * math.cos(math.pi - 2 * math.pi * t) + self.C[0]
    def y_t(self, t): return self.R * math.sin(math.pi - 2 * math.pi * t) + self.C[1]


class CircleApproacher:

    def __init__(self, circle_parameters, initial_parameters, num_of_parameters=5):
        self.r = circle_parameters["radius"]
        self.c = circle_parameters["center"]
        self.circle = CustomCircle(self.c, self.r)
        self.circle_graph = self.circle.graph(0.01)
        self.line = StraightLine([[0, [0, 0]], [1, [1, 1]]])
        self.parameters = initial_parameters
        self.bezier = self.initialize_bezier()
        self.num_of_parameters = num_of_parameters

    def initialize_bezier(self):
        a, b, c, d, e = self.parameters
        cp = np.array([[a, 0], [b, c], [d, e], [d, -e], [b, -c], [a, 0]])
        return Bezier(cp)

    def refresh_bezier(self):
        a, b, c, d, e = self.parameters
        CP = np.array([[a, 0], [b, c], [d, e], [d, -e], [b, -c], [a, 0]])
        self.bezier.refresh_control_points(CP)

    def refresh_parameters(self, new_parameters):
        self.parameters = new_parameters

    def least_squares(self, point_pairs):

        def p0(t): return Polynomial(np.array([1, -5, 10, -10, 5])).value(t)
        def p1(t): return Polynomial(np.array([0, 1, -4, 6, -3])).value(t)
        def p2(t): return Polynomial(np.array([0, 0, 1, -2, 1])).value(t)
        def p3(t): return Polynomial(np.array([0, 1, -4, 6, -5, 2])).value(t)
        def p4(t): return Polynomial(np.array([0, 0, 1, -4, 5, -2])).value(t)

        def sigma1(f, g, table): return sum([f(table[i][0]) * g(table[i][0]) for i in range(len(table))])
        def sigma2(f, index, table): return sum([table[i][1][0][index] * f(table[i][0]) for i in range(len(table))])

        if self.num_of_parameters == 5:

            A11 = sigma1(p0, p0, point_pairs)
            A12 = sigma1(p0, p1, point_pairs)
            A13 = sigma1(p0, p2, point_pairs)
            A21 = A12
            A22 = sigma1(p1, p1, point_pairs)
            A23 = sigma1(p1, p2, point_pairs)
            A31 = A13
            A32 = A23
            A33 = sigma1(p2, p2, point_pairs)

            A = [[A11, A12, A13],
                 [A21, A22, A23],
                 [A31, A32, A33]]

            B11 = sigma2(p0, 0, point_pairs)
            B21 = sigma2(p1, 0, point_pairs)
            B31 = sigma2(p2, 0, point_pairs)

            B = [B11, B21, B31]

            solution_0 = np.linalg.solve(A, B)

            a_new = solution_0[0]
            b_new = solution_0[1] / 5
            d_new = solution_0[2] / 10

        elif self.num_of_parameters == 3:

            a_new = 0
            b_new = 0
            d_new = 0.1 * sigma2(p2, 0, point_pairs) / sigma1(p2, p2, point_pairs)

        else: return

        C11 = sigma1(p3, p3, point_pairs)
        C12 = sigma1(p3, p4, point_pairs)
        C21 = C12
        C22 = sigma1(p4, p4, point_pairs)

        C = [[C11, C12], [C21, C22]]

        D11 = sigma2(p3, 1, point_pairs)
        D21 = sigma2(p4, 1, point_pairs)

        D = [D11, D21]

        solution_1 = np.linalg.solve(C, D)

        c_new = solution_1[0] / 5
        e_new = solution_1[1] / 10

        return [a_new, b_new, c_new, d_new, e_new]

    def calculate_point_pairs(self, d_phi):

        def dx(tb, tl): return self.bezier.x_t(tb) - self.line.x_t(tl)
        def dy(tb, tl): return self.bezier.y_t(tb) - self.line.y_t(tl)
        def dxb(tb, tl): return Polynomial(self.bezier.c[0]).derivative().value(tb)
        def dxl(tb, tl): return - Polynomial(self.line.c[0]).derivative().value(tl)
        def dyb(tb, tl): return Polynomial(self.bezier.c[1]).derivative().value(tb)
        def dyl(tb, tl): return - Polynomial(self.line.c[1]).derivative().value(tl)

        point_pairs = []

        dt = d_phi / (2 * math.pi)
        for t in np.arange(0., 1., dt):
            self.line.modify_points([[0, [self.r, 0]], [1, self.circle.point_t(t)]])
            tb, tl = newton_raphson_2x2(dx, dy, dxb, dxl, dyb, dyl, t, 1, 1.e-12)

            K = self.line.point_t(1)
            Q = self.bezier.point_t(tb)
            point_pairs.append([tb, [K, Q]])

        return point_pairs

    @staticmethod
    def error_function(point_pairs, divisions):
        # 1st Approach
        # Ex = sum([(pair[1][0][0] - pair[1][1][0]) ** 2 for pair in point_pairs])
        # Ey = sum([(pair[1][0][1] - pair[1][1][1]) ** 2 for pair in point_pairs])
        # return math.sqrt(Ex + Ey)

        # 2nd Approach
        return sum([math.sqrt((pair[1][0][0] - pair[1][1][0]) ** 2 + (pair[1][0][1] - pair[1][1][1]) ** 2)
                    for pair in point_pairs]) / divisions

    def solve(self, d_phi, iterations=3000, error=1e-12, csv_fname=None, plots_path=None):

        def convergence():
            nonlocal new_parameters
            for i in range(len(self.parameters)):
                if abs(self.parameters[i] - new_parameters[i]) > error:
                    return False
            return True

        def create_csv():
            nonlocal csv_exporter
            csv_exporter.create_csv()
            csv_exporter.write_headers("Iter", "Parameter a", "Parameter b", "Parameter c", "Parameter d",
                                       "Parameter e", "Error Function")

        def give_output(i, error_f):
            screen_printer.print_results(i, self.parameters, error_f)
            if csv_fname:
                csv_exporter.append_row(i, *self.parameters, error_f)
            if plots_path and (i < 20 or i % 10 == 0.):
                bezier_graph = self.bezier.graph(0.01)
                plot_exporter.create_plot(self.circle_graph, bezier_graph,
                                          title="Approach Circle w/ Bezier (Iteration {})".format(i), axes_equal=True)
                plot_exporter.export_plot("gen_{}".format(str(i).zfill(4)))

        divisions = 2 * math.pi / d_phi

        csv_exporter = None
        if csv_fname:
            csv_exporter = ScvExporter(csv_fname, r"results/")
            create_csv()
        screen_printer = ScreenPrinter()

        plot_exporter = None
        if plots_path:
            plot_exporter = PlotExporter(plots_path)

        for i in range(iterations):
            point_pairs = self.calculate_point_pairs(d_phi)
            error_f = self.error_function(point_pairs, divisions)
            give_output(i, error_f)
            new_parameters = self.least_squares(point_pairs)
            if convergence():
                self.refresh_parameters(new_parameters)
                point_pairs = self.calculate_point_pairs(d_phi)
                error_f = self.error_function(point_pairs, divisions)
                give_output(i, error_f)
                break
            else:
                self.refresh_parameters(new_parameters)
                self.refresh_bezier()
