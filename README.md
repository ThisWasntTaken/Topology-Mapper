# Mapper - Topological Data Analysis

## Requirements
* [python 3.x](https://www.python.org/)
* [numpy](https://numpy.org/)
* [networkx](https://networkx.github.io/)
* [pyvis](https://pyvis.readthedocs.io/en/latest/)
* [scikit-learn](https://scikit-learn.org/stable/)

Refer to requirements.txt for a complete list of packages and libraries.

## What is Mapper?
Mapper is an unsupervised algorithm that is used to construct a simplicial complex (a graph) that represents the structure of data. It reveals topological features of the data so that the data can be explored better.

To construct the graph, we require:
1. A Filter function that maps the data to a lower dimension (this implementation requires the range of the Filter funcion to be the space of real numbers)
2. A cover of the range of the Filter function with overlapping between each pair of consecutive intervals.

The filter function is used to represent the data in a lower dimension space. Dimensionality-reduction techniques like PCA or t-SNE could be used here if required for data in very high dimensions.

## An Example
Consider a data created using the following function on sklearn.
```python
make_circles(n_samples = 10000, noise = 0.05, random_state = 44, factor = 0.5)
```
The data is a pair of concentric circles as shown below on the left. The filter function (lens) is `f(x, y) = y`. The data as seen through the lens is shown on the right.

![Data](content/make_circles_scatter.png "Data") ![Data through lens](content/make_circles_scatter_through_lens.png "Data through lens")

Consider the cover of the range of the filter function to be the set of overlapping intervals {(-1.3, -1.2), (-1.23, -1.13), (-1.16, -1.06), (-1.09, -0.99), (-1.02, -0.92), (-0.95, -0.85), (-0.88, -0.78), (-0.81, -0.71), (-0.74, -0.64), (-0.67, -0.57), (-0.6, -0.5), (-0.53, -0.43), (-0.46, -0.36), (-0.39, -0.29), (-0.32, -0.22), (-0.25, -0.15), (-0.18, -0.08), (-0.11, -0.01), (-0.04, 0.06), (0.03, 0.13), (0.1, 0.2), (0.17, 0.27), (0.24, 0.34), (0.31, 0.41), (0.38, 0.48), (0.45, 0.55), (0.52, 0.62), (0.59, 0.69), (0.66, 0.76), (0.73, 0.83), (0.8, 0.9), (0.87, 0.97), (0.94, 1.04), (1.01, 1.11), (1.08, 1.18), (1.15, 1.25), (1.22, 1.3)}