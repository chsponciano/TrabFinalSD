var nodes = new Map();
var edges = new Map();
var count_edge = 1;
var connect_init = 0;

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

async function refresh_screen() {
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

        var g = {
            nodes: [],
            edges: []
        };

        for (var [key, value] of nodes) {
            g.nodes.push({
                id: key,
                label: key,
                x: Math.random(),
                y: Math.random(),
                size: 10,
                color: '#007bff'
            });
        }

        for (var [key, value] of edges) {
            g.edges.push({
                id: value.edge_name,
                source: value.source,
                target: value.target,
                size: 10,
                color: '#CCC'
            });
        }

        s = new sigma({
            graph: g,
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

var calc_router = function(args) {
    console.log(args);
    refresh_screen();
}

var end_algorithm_callback_message = function(args) {
    console.log(args);
}

var every_node_callback_message = function(args) {
    console.log(args);
}

// function send_message(message) {
//     $(".img-update").addClass('hide');
//     $(".img-updating").removeClass('hide');
//     ws.send(message);
// }

function getAllNodes() {
    // send_message('{"message": "get_all_nodes", "args": {"callback_queue": "frontend-queue", "callback_message": "get_all_nodes"}}');
    $.get("http://localhost:5000/get_all_nodes", function(data) {
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
    idx = $('.id_node').val();
    cust = $('.ms_node').val();

    $.post(
        "http://localhost:5000/create_node", 
        {
            node_name: idx,
            processing_time: cust
        },
        function(data) {
            console.log("createNode: " + JSON.stringify(data));
            if (!nodes.has(args.node_name)) {
                nodes.set(args.node_name, new Node(args.node_name, args.processing_time));
            }
            refresh_screen();
        }
    );

    $('.id_node').val('');
    $('.ms_node').val('');
}

function deleteNode(idx) {
    $.post(
        "http://localhost:5000/delete_node", 
        {
            node: idx,
        },
        function(data) {
            console.log("deleteNode: " + JSON.stringify(data));
            if (nodes.has(data.node_name)) {
                nodes.delete(data.node_name)
            }
            refresh_screen();
        }
    );
}

function createConnection() {
    node1 = $('#cc_origem').val();
    node2 = $('#cc_destino').val();
    $.post(
        "http://localhost:5000/create_connection", 
        {
            node1: node1,
            node2: node2
        },
        function(data) {
            console.log("createConnection: " + JSON.stringify(data));
            edges.set('e' + count_edge, new Edge('e' + count_edge, data.node1, data.node2));
            count_edge++;
            edges.set('e' + count_edge, new Edge('e' + count_edge, data.node1, data.node2));
            count_edge++;
            refresh_screen();
        }
    );
    $('#cc_origem').val('');
    $('#cc_destino').val('');
}

function deleteConnection() {
    node1 = $('#cc_origem').val();
    node2 = $('#cc_destino').val();
    $.post(
        "http://localhost:5000/delete_connection", 
        {
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
    
    var socket = io.connect('http://127.0.0.1:5000');
    socket.on('connect', function() {
        console.log('connect')
        socket.emit(
            "calc_route",
            {
                callback_message: "calcRouteResponse",
                every_node_callback_message: "everyNodeCallbackMessage",
                end_algorithm_callback_message: "endAlgorithmCallbackMessage",
                start_node: node1,
                target_node: node2,
                algorithm : algorithm
            }
        );
    });
    socket.on('calcRouteResponse', function(data) {
        console.log("startou o algoritmo")
        console.log(data);
    });
    socket.on('everyNodeCallbackMessage', function(data) {
        console.log("cai aqui toda vez que passar por um nó")
        console.log(data);
    });
    socket.on('endAlgorithmCallbackMessage', function(data) {
        console.log("cai aqui somente no ultimo nó, e somente uma vez.")
        console.log("impl do controller ainda não concluida, mas já da pra brinca com o frontend")
        console.log(data);
        socket.disconnect();
        alert(JSON.stringify(data));
    });

    $('#cr_origem').val('');
    $('#cr_destino').val('');
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