var nodes = new Map();
var edges = new Map();
var graph_model = null;
var node_old_color = null;
var logs_path = [];
var count_edge = 1;
var connect_init = 0;
var serverIp = "http://localhost:5000";
// var serverPort = "5000";

class Node {
    constructor(node_name, processing_time) {
        this.node_name = node_name;
        this.processing_time = processing_time;
    }
}

class Edge {
    constructor(edge_name, source, target) {
        this.edge_name = edge_name;
        this.source = source;
        this.target = target;
    }
}

function existEdge(source, target) {
    for (var [key, value] of edges) {
        if ((value.source == source && value.target == target) || (value.source == target && value.target == source)) {
            return true;
        }
    }

    return false;
}

function draw_node_visited(node) {
    for (let i = 0; i < graph_model.nodes.length; i++) {
        if (node_old_color != null && node_old_color == graph_model.nodes[i].id) {
            graph_model.nodes[i].color = '#007bff';
        }

        if (node == graph_model.nodes[i].id) {
            graph_model.nodes[i].color = '#DE1738';
        }
    }

    node_old_color = node;

    var el;

    for (let index = 0; index < 3; index++) {
        el = document.getElementsByTagName('canvas')[0];
        el.parentNode.removeChild(el);
    }

    s = new sigma({
        graph: graph_model,
        container: 'graph-container'
    });
}

function draw_path(nodes) {
    var node_prev = null;

    for (let i = 0; i < graph_model.nodes.length; i++) {
        if (node_old_color == graph_model.nodes[i].id) {
            graph_model.nodes[i].color = '#007bff';
        }
    }

    for (let i = 0; i < nodes.length; i++) {
        for (let j = 0; j < graph_model.nodes.length; j++) {
            if (nodes[i] == graph_model.nodes[j].id) {
                graph_model.nodes[j].color = '#DE1738';
                break;
            }
        }

        if (node_prev != null) {
            for (let j = 0; j < graph_model.edges.length; j++) {
                if ((graph_model.edges[j].source == node_prev && graph_model.edges[j].target == nodes[i]) || (graph_model.edges[j].source == nodes[i] && graph_model.edges[j].target == node_prev)) {
                    graph_model.edges[j].color = '#DE1738';
                    break;
                }
            }
        }

        node_prev = nodes[i];
    }

    var el;

    for (let index = 0; index < 3; index++) {
        el = document.getElementsByTagName('canvas')[0];
        el.parentNode.removeChild(el);
    }

    s = new sigma({
        graph: graph_model,
        container: 'graph-container'
    });
}

function init_path() {
    for (let i = 0; i < graph_model.nodes.length; i++) {
        graph_model.nodes[i].color = '#007bff';
    }
    for (let i = 0; i < graph_model.edges.length; i++) {
        graph_model.edges[i].color = '#CCC';
    }

    init_logs_path();

    var el;

    for (let index = 0; index < 3; index++) {
        el = document.getElementsByTagName('canvas')[0];
        el.parentNode.removeChild(el);
    }

    s = new sigma({
        graph: graph_model,
        container: 'graph-container'
    });
}

async function refresh_screen() {
    init_logs_path();

    if (connect_init == 0) {
        connect_init = 1;
        await sleep(1000);
        console.log('auto getAllNodes');
        getAllNodes();
    } else {
        if (connect_init == 2) {
            var el;

            for (let index = 0; index < 3; index++) {
                el = document.getElementsByTagName('canvas')[0];
                el.parentNode.removeChild(el);
            }
        } else {
            connect_init = 2;
        }

        graph_model = {
            nodes: [],
            edges: []
        };

        for (var [key, value] of nodes) {
            graph_model.nodes.push({
                id: key,
                label: key,
                x: Math.random(),
                y: Math.random(),
                size: 10,
                color: '#007bff'
            });
        }

        for (var [key, value] of edges) {
            graph_model.edges.push({
                id: value.edge_name,
                source: value.source,
                target: value.target,
                size: 10,
                color: '#CCC'
            });
        }

        s = new sigma({
            graph: graph_model,
            container: 'graph-container'
        });

        list_server();

        $(".img-updating").addClass('hide');
        $(".img-update").removeClass('hide');

    }
}

function list_server() {
    $('#control-area-list').html('');
    $('.custom-select-node').html("<option selected></option>");
    for (var [key, value] of nodes) {
        $('#control-area-list').append('<article><div class="row"><div class="col-sm-8 ds-node"><div id="content">' + key + '<br>' + value.processing_time +
            'ms</div></div><div class="col-sm-4 control-area-list-chk"><button type="button" class="btn btn-primary" onclick="deleteNode(\'' + key + '\')">Excluir</button></div></div></article>');
        $('.custom-select-node').append("<option value='" + key + "'>" + key + "</option>");
    }

}

function getAllNodes() {
    $(".img-update").addClass('hide');
    $(".img-updating").removeClass('hide');

    $.get(serverIp + "/get_all_nodes", function(data) {
        console.log("getAllNodes: " + JSON.stringify(data));
        nodes.clear();
        edges.clear();
        count_edge = 1;

        for (let i = 0; i < data.length; i++) {
            nodes.set(data[i]["node_name"], new Node(data[i]["node_name"], data[i]["processing_time"]));

            for (let j = 0; j < data[i]["connections"].length; j++) {
                if (!existEdge(data[i]["node_name"], data[i]["connections"][j])) {
                    edges.set("e" + count_edge, new Edge("e" + count_edge, data[i]["node_name"], data[i]["connections"][j]));
                    count_edge++;
                }
            }
        }

        refresh_screen();
    });
}

function createNode() {
    $(".img-update").addClass('hide');
    $(".img-updating").removeClass('hide');

    idx = $('.id_node').val();
    cust = $('.ms_node').val();

    $.post(
        serverIp + "/create_node", {
            node_name: idx,
            processing_time: cust
        },
        function(data) {
            console.log("createNode: " + JSON.stringify(data));
            if (!nodes.has(data.node_name)) {
                nodes.set(data.node_name, new Node(data.node_name, data.processing_time));
            }
            refresh_screen();
        }
    );

    $('.id_node').val('');
    $('.ms_node').val('');
}

function deleteNode(idx) {
    $(".img-update").addClass('hide');
    $(".img-updating").removeClass('hide');

    $.post(
        serverIp + "/delete_node", {
            node: idx,
        },
        function(data) {
            console.log("deleteNode: " + JSON.stringify(data));
            if (nodes.has(data.node.node_name)) {
                nodes.delete(data.node.node_name)
            }
            refresh_screen();
        }
    );
}

function createConnection() {
    $(".img-update").addClass('hide');
    $(".img-updating").removeClass('hide');

    node1 = $('#cc_origem').val();
    node2 = $('#cc_destino').val();
    $.post(
        serverIp + "/create_connection", {
            node1: node1,
            node2: node2
        },
        function(data) {
            console.log("createConnection: " + JSON.stringify(data));
            edges.set('e' + count_edge, new Edge('e' + count_edge, data.node1, data.node2));
            count_edge++;
            // edges.set('e' + count_edge, new Edge('e' + count_edge, data.node2, data.node1));
            // count_edge++;
            refresh_screen();
        }
    );
    $('#cc_origem').val('');
    $('#cc_destino').val('');
}

function deleteConnection() {
    $(".img-update").addClass('hide');
    $(".img-updating").removeClass('hide');

    node1 = $('#cc_origem').val();
    node2 = $('#cc_destino').val();
    $.post(
        serverIp + "/delete_connection", {
            node1: node1,
            node2: node2
        },
        function(data) {
            for (var [key, value] of edges) {
                if ((value.source == data.node1 && value.target == data.node2) || (value.source == data.node2 && value.target == data.node1)) {
                    edges.delete(key);
                }
            }
            refresh_screen();
        }
    );
    $('#cc_origem').val('');
    $('#cc_destino').val('');
}

function startCalcRoute() {
    console.log("startCalcRoute");
    node1 = $('#cr_origem').val();
    node2 = $('#cr_destino').val();
    algorithm = $('#cr_algoritmo').val();

    var socket = io.connect(serverIp);
    socket.on('connect', function() {
        console.log('connect')
        socket.emit(
            "calc_route", {
                callback_message: "calcRouteResponse",
                every_node_callback_message: "everyNodeCallbackMessage",
                end_algorithm_callback_message: "endAlgorithmCallbackMessage",
                start_node: node1,
                target_node: node2,
                algorithm: algorithm
            }
        );
    });
    socket.on('calcRouteResponse', function(data) {
        //init_path();
        //print_logs('Inciando ' + data.algorithm);
        console.log(data);
    });
    socket.on('everyNodeCallbackMessage', function(data) {
        //draw_node_visited(data.current_node);
        //print_logs(data.current_node + ": " + data.total_dist);
        console.log(data);
    });
    socket.on('endAlgorithmCallbackMessage', function(data) {
        //draw_path(data.visited_nodes)
        //print_logs("Total do percurso: " + data.total_dist);
        console.log(data);
        socket.close();
    });

    $('#cr_origem').val('');
    $('#cr_destino').val('');
    $('#cr_algoritmo').val('');
}

function init_logs_path() {
    logs_path = [];
    document.getElementById('logs-path').innerHTML = '';
}

function print_logs(content) {
    logs_path.push(content);

    var logs_out = '';
    for (let i = logs_path.length - 1; i >= logs_path.length - 6; i--) {
        if (i < 0) {
            break;
        }
        logs_out += logs_path[i] + "<br>";
    }

    document.getElementById('logs-path').innerHTML = logs_out;
}

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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

refresh_screen(true);