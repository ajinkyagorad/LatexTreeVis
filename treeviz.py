<!DOCTYPE html>
<html>
<head>
    <title>Interactive Tree Visualization with Size, Color, and Highlighting</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://unpkg.com/3d-force-graph"></script>
</head>
<body style="margin: 0; overflow: hidden;">
    <div id="3d-graph" style="width: 100%; height: 100vh;"></div>
    <script>
        const graphData = {"nodes": [], "links": []}; // Replace this with the actual graph data

        const Graph = ForceGraph3D()
            (document.getElementById('3d-graph'))
            .graphData(graphData)
            .nodeAutoColorBy('color')
            .nodeLabel('id')
            .nodeThreeObject(node => {
                const sphere = new THREE.Mesh(
                    new THREE.SphereGeometry(node.size / 2),
                    new THREE.MeshBasicMaterial({ color: node.color, opacity: 1, transparent: true })
                );
                return sphere;
            })
            .linkWidth(2)
            .linkDirectionalArrowLength(3)
            .linkDirectionalArrowRelPos(0.5)
            .linkDirectionalParticles(4)
            .linkDirectionalParticleSpeed(0.01)
            .onNodeHover(node => {
                const highlightedNodes = new Set();
                const opacityMap = {};

                function traverse(currentNode, distance) {
                    if (distance > 4 || !currentNode) return;

                    highlightedNodes.add(currentNode);
                    opacityMap[currentNode.id] = 1 - distance * 0.25;

                    graphData.links.forEach(link => {
                        if (link.source === currentNode.id) {
                            traverse(graphData.nodes.find(n => n.id === link.target), distance + 1);
                        } else if (link.target === currentNode.id) {
                            traverse(graphData.nodes.find(n => n.id === link.source), distance + 1);
                        }
                    });
                }

                traverse(node, 0);

                Graph.nodeThreeObject(node => {
                    const opacity = opacityMap[node.id] || 0.1;
                    const sphere = new THREE.Mesh(
                        new THREE.SphereGeometry(node.size / 2),
                        new THREE.MeshBasicMaterial({ color: node.color, opacity, transparent: true })
                    );
                    return sphere;
                });
            });
    </script>
</body>
</html>
