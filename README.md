# Mapper - Topological Data Analysis

## Requirements
* [python 3.x](https://www.python.org/)
* [numpy](https://numpy.org/)
* [networkx](https://networkx.github.io/)
* [pyvis](https://pyvis.readthedocs.io/en/latest/)
* [scikit-learn](https://scikit-learn.org/stable/)

## What is Mapper?
Mapper is an unsupervised algorithm that is used to construct a simplicial complex (a graph) that represents the structure of data. It reveals topological features of the data so that the data can be explored better.

To construct the graph, we require:
1. A Filter function
2. A cover of the domain of the Filter function.

The filter function is used to represent the data in a lower dimension space. Dimensionality-reduction techniques like PCA or t-SNE could be used here if required for data in very high dimensions.

## An Example
Below is the data on the left, and the data as seen through the filter function, which is f(x, y) = y here, on the right.
![Scatter plot of the data](content/scatter.png "Data") ![Scater plot of data observed through the filter function](content/scatter_through_lens.png "Data through filter")

A cover of the domain (say, (-1.3, 1.3)) of the filter function could be the overlapping intervals (-1.3, -0.6), (-0.8, -0.1), (-0.3, 0.4), (0.2, 0.9), (0.7, 1.3). The points that belong to an interval as given by the filter function are collected from the original data and a clustering algorithm is run on each set of points. The below plot shows the data being split by the cover (overlaps are not shown).
![Scatter plot of the data segregated by the cover](content/scatter_cover.png "Data after split by cover")

After forming clusters, each cluster is represented by a node in a graph, with edges connecting two nodes only if the clusters corresponding to the nodes have a non-empty set intersection. The final result of this operation is shown [here](https://thiswasnttaken.github.io//assets/html/mapper.html). It can be seen that there are two cycles in the graph that correspond to the two circles in the data. However, the feature that the two circles are concentric is NOT captured by Mapper.

<html>
<head>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis.css" type="text/css" />
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>

<!-- <link rel="stylesheet" href="../node_modules/vis/dist/vis.min.css" type="text/css" />
<script type="text/javascript" src="../node_modules/vis/dist/vis.js"> </script>-->

<style type="text/css">

        #mynetwork {
            width: 1366;
            height: 768;
            background-color: #222222;
            border: 1px solid lightgray;
            position: relative;
            float: left;
        }

        

        

        
</style>

</head>

<body>
<div id = "mynetwork"></div>


<script type="text/javascript">

    // initialize global variables.
    var edges;
    var nodes;
    var network; 
    var container;
    var options, data;

    
    // This method is responsible for drawing the graph, returns the drawn network
    function drawGraph() {
        var container = document.getElementById('mynetwork');
        
        

        // parsing and collecting nodes and edges from the python
        nodes = new vis.DataSet([{"color": "#ff5200", "id": 0, "label": " ", "shape": "dot", "size": 24.333333333333332, "title": "Contains 292 elements"}, {"color": "#ffb000", "id": 1, "label": " ", "shape": "dot", "size": 11.083333333333334, "title": "Contains 133 elements"}, {"color": "#ff0000", "id": 2, "label": " ", "shape": "dot", "size": 35.666666666666664, "title": "Contains 428 elements"}, {"color": "#ffb500", "id": 3, "label": " ", "shape": "dot", "size": 10.416666666666666, "title": "Contains 125 elements"}, {"color": "#ffba00", "id": 4, "label": " ", "shape": "dot", "size": 9.666666666666666, "title": "Contains 116 elements"}, {"color": "#ff7100", "id": 5, "label": " ", "shape": "dot", "size": 20.0, "title": "Contains 240 elements"}, {"color": "#ffbc00", "id": 6, "label": " ", "shape": "dot", "size": 9.5, "title": "Contains 114 elements"}, {"color": "#ff6b00", "id": 7, "label": " ", "shape": "dot", "size": 20.833333333333332, "title": "Contains 250 elements"}, {"color": "#ffa900", "id": 8, "label": " ", "shape": "dot", "size": 12.083333333333334, "title": "Contains 145 elements"}, {"color": "#ffa800", "id": 9, "label": " ", "shape": "dot", "size": 12.25, "title": "Contains 147 elements"}, {"color": "#ff2400", "id": 10, "label": " ", "shape": "dot", "size": 30.75, "title": "Contains 369 elements"}, {"color": "#ff6a00", "id": 11, "label": " ", "shape": "dot", "size": 20.916666666666668, "title": "Contains 251 elements"}]);
        edges = new vis.DataSet([{"color": "#ffdd00", "from": 0, "to": 1}, {"color": "#ffdd00", "from": 0, "to": 3}, {"color": "#ffdd00", "from": 1, "to": 4}, {"color": "#ffdd00", "from": 2, "to": 5}, {"color": "#ffdd00", "from": 2, "to": 7}, {"color": "#ffdd00", "from": 3, "to": 6}, {"color": "#ffdd00", "from": 4, "to": 9}, {"color": "#ffdd00", "from": 5, "to": 10}, {"color": "#ffdd00", "from": 6, "to": 8}, {"color": "#ffdd00", "from": 7, "to": 10}, {"color": "#ffdd00", "from": 8, "to": 11}, {"color": "#ffdd00", "from": 9, "to": 11}]);

        // adding nodes and edges to the graph
        data = {nodes: nodes, edges: edges};

        var options = {"nodes": {"shadow": {"enabled": true}}, "edges": {"color": {"inherit": true}, "smooth": true}, "physics": {"barnesHut": {"centralGravity": 0, "springLength": 50, "springConstant": 0.01, "avoidOverlap": 0.5}, "minVelocity": 0.75}};
        
        

        

        network = new vis.Network(container, data, options);

        


        

        return network;

    }

    drawGraph();

</script>
</body>
</html>