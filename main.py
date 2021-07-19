import math
from approach_circle_with_bezier.circle_approacher import CircleApproacher


R = 1.5
C = [R, 0]

circle_parameters = {"center": C,
                     "radius": R}

initial_parameters = [0., 0., 3., 8., 2.]

d_phi = 2 * math.pi / 200

approacher = CircleApproacher(circle_parameters, initial_parameters)
approacher.solve(d_phi, iterations=3000, error=1e-12, csv_fname="results200")
