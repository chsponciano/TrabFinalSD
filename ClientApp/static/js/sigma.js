var i,
    s,
    N = 10,
    E = 15,
    g = {
        nodes: [],
        edges: []
    };

// Generate a random graph:
for (i = 0; i < N; i++)
    g.nodes.push({
        id: 'n' + i,
        label: 'Node ' + i,
        x: Math.random(),
        y: Math.random(),
        size: 10,
        color: '#007bff'
    });

for (i = 0; i < E; i++)
    g.edges.push({
        id: 'e' + i,
        source: 'n' + (Math.random() * N | 0),
        target: 'n' + (Math.random() * N | 0),
        size: 10,
        color: '#CCC'
    });

s = new sigma({
    graph: g,
    container: 'graph-container'
});

$(function() {
    $("#graph-container").mouseenter(function() {
        document.querySelector('#graph-container').style.cursor = 'grab';
    });
});

$(function() {
    $("#graph-container").mouseout(function() {
        document.querySelector('#graph-container').style.cursor = 'default';
    });
});

$(function() {
    $("#graph-container").mousedown(function() {
        document.querySelector('#graph-container').style.cursor = 'grabbing';
    });
});

$(function() {
    $("#graph-container").mouseup(function() {
        document.querySelector('#graph-container').style.cursor = 'grab';
    });
});