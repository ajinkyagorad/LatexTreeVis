# Reprocess the complete tree and ensure all levels are included correctly for HTML visualization

# Build graph data from the tree
def build_graph_data(node, level=0, graph=None):
    if graph is None:
        graph = {"nodes": [], "links": []}
    size = max(20 - level * 2, 4)  # Decrease size for deeper levels
    color = (
        0xff0000 if level == 0 else
        0x00ff00 if level == 1 else
        0x0000ff if level == 2 else
        0x999999  # Default color for deeper levels
    )
    graph["nodes"].append({"id": node.name, "size": size, "color": color})
    for child in node.children:
        graph["links"].append({"source": node.name, "target": child.name})
        build_graph_data(child, level + 1, graph)
    return graph

# Generate the graph data from the corrected tree
graph_data = build_graph_data(root)

# Create HTML with the tree visualization
html_content_tree = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Ball Tree Visualization</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/3d-force-graph"></script>
</head>
<body style="margin: 0; overflow: hidden;">
    <div id="3d-graph" style="width: 100%; height: 100vh;"></div>
    <script>
        const graphData = {graph_data};

        const Graph = ForceGraph3D()
            (document.getElementById('3d-graph'))
            .graphData(graphData)
            .nodeAutoColorBy('color')
            .nodeLabel('id')
            .nodeThreeObject(node => {{
                const sphere = new THREE.Mesh(
                    new THREE.SphereGeometry(node.size / 2),
                    new THREE.MeshBasicMaterial({{ color: node.color }})
                );
                return sphere;
            }})
            .linkWidth(2)
            .linkDirectionalArrowLength(3)
            .linkDirectionalArrowRelPos(0.5)
            .linkDirectionalParticles(4)
            .linkDirectionalParticleSpeed(0.01);
    </script>
</body>
</html>
"""

# Save the HTML content to a file
html_tree_path = "/mnt/data/interactive_ball_tree_complete.html"
with open(html_tree_path, "w") as html_file:
    html_file.write(html_content_tree)

html_tree_path
