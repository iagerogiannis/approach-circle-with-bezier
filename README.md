# Approach Circle with Bezier Spline

This project is an example and demonstration of application of numerical methods like Least Squares and Newton-Raphson
in optimization problems. 

The object of the project is the parameterization of a curve with Bezier spline, which tends to approach the circle and
the minimization of the difference between the curve and the circle - target.

## The idea behind

At first a Bezier spline of 6 Control Points gets initialized. Our goal is to calculate the control point coordinates
which minimize the distance between the circle and the spline. The circle - target gets divided in n points which are at
a same distance angularly. For each one of these point, a straight line is being drawn from the center of the circle to
that point Ki. Then we calculate the intercept points Qi of the lines and the Bezier spline. Next we apply the Least
Squares method in order to minimize those radial distances KiQi.

<p align="center">
  <img src="readme/Screenshot_0.png">
</p>

## Mathematical Formulation

### Parameterization

#### Parameterization of Bezier Spline

The curve is parameterized with a Bezier spline of 6 Control Points. In order to simplify the problem and minimize the
variables we exploit geometry symmetries, so that we have to define only 5 unknowns as shown in the graph above.

<p align="center">
  <img src="readme/Screenshot_1.png">
</p>

<p align="center">
  <img src="readme/Screenshot_2.png">
</p>

<p align="center">
  <img src="readme/Screenshot_3.png">
</p>

#### Parameterization of Circle

<p align="center">
  <img src="readme/Screenshot_4.png">
</p>

<p align="center">
  <img src="readme/Screenshot_5.png">
</p>

#### Parameterization of Straight Lines

<p align="center">
  <img src="readme/Screenshot_6.png">
</p>

<p align="center">
  <img src="readme/Screenshot_7.png">
</p>

### Calculation of Point Pairs Ki-Qi

<p align="center">
  <img src="readme/Screenshot_8.png">
</p>

<p align="center">
  <img src="readme/Screenshot_9.png">
</p>

### Minimization of the distances Ki-Qi

<p align="center">
  <img src="readme/Screenshot_10.png">
</p>

<p align="center">
  <img src="readme/Screenshot_11.png">
</p>

<p align="center">
  <img src="readme/Screenshot_12.png">
</p>

## Results

Result

<p align="center">
  <img src="readme/animation.gif">
</p>
