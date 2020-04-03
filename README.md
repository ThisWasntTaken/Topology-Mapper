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

Under Construction, check back in a few days!