$(document).ready(function () {

    $('input:radio[name="optionConnectionRadios"]').change(
        function () {
            if ($(this).is(':checked') && $(this).val() == 'file') {
                $('#data-connection-from').removeClass('show');
                $('#data-connection-from').addClass('hidden');
                $('#sheet-upload-from').addClass('show');
                $('#sheet-upload-from').removeClass('hidden');
            } else {
                $('#sheet-upload-from').removeClass('show');
                $('#sheet-upload-from').addClass('hidden');
                $('#data-connection-from').addClass('show');
                $('#data-connection-from').removeClass('hidden');
            }
        });

    $('#uploadConnectionCSV').change(function () {
        var val = $(this).val().toLowerCase(),
            regex = new RegExp("(.*?)\.(csv|xlsx|xls|xlsm)$");

        if (!(regex.test(val))) {
            $(this).val('');
            $("#upload-connection-btn").attr('disabled', true);
            alert('Please select correct file format. Supported: CSV, EXCEL');
        }
        else {
            $("#upload-connection-btn").attr('disabled', false);
        }
    });

    $('#jstree2').on('changed.jstree', (e, data) => {
        var newSummaryList = $("#jstree2").jstree().get_selected(true);
        if (newSummaryList != "") {
            // generateWorkboardCallData();
            toggleFetchingDataButton();
        }
    });


    $('#jstree1').on('select_node.jstree', (e, data) => {
        data.instance.toggle_node(data.node);
        if (data.node.parent != "#") {
            var collectionName = data.instance.get_node(data.node.parent).data.obj.collection_name;
            var eachData = data.node;
            createSingleNode("#jstree2", eachData.id, eachData.text, eachData.data, eachData.state, eachData.icon, collectionName, "last");
        }
    });

    $('#jstree1').on('deselect_node.jstree', (e, data) => {

        if (data.node.parent != "#") {
            var collectionName = data.instance.get_node(data.node.parent).data.obj.collection_name;
            var eachData = data.node;
            deleteSingleNode(eachData);
        }
    });

    $("#fetch-data-btn").click(function () {
        generateWorkboardCallData();
    });

    $("#save-workboard-btn").click(function () {
        var variables = getSummaryListSelectedVariables();
        updateWorkboard(variables);
    });

    $("#analysis-types li").click(function () {
        $('#analysis-types li').each(function () {
            $(this).removeClass('text-warning');
        });
        $(this).addClass('text-warning');
        // generateWorkboardCallData();
        toggleFetchingDataButton();
    });

    $('.check-link').click(function () {
        var button = $(this).find('i');
        var label = $(this).next('span');
        button.toggleClass('fa-check-square').toggleClass('fa-square');
        button.toggleClass('fas').toggleClass('far');
        if($('.small-list').find(".fas").length > 0){
            $("#save-dashboard-btn").attr('disabled', false);
        }else{
            $("#save-dashboard-btn").attr('disabled', true);
        }
        return false;
    });

});

function getSummaryListSelectedVariables() {
    var summaryList = $("#jstree2").jstree().get_selected(true);
    var variables = {};

    summaryList.forEach(function (node) {
        var valueHash = {'name': node.text, 'type': node.data.objId.Var_Type, 'id': node.id};
        if (variables[node.original.collection_name] == undefined) {
            variables[node.original.collection_name] = [];
            variables[node.original.collection_name].push(valueHash);
        }
        else variables[node.original.collection_name].push(valueHash);
    });

    return variables;
}

function toggleFetchingDataButton() {
    var summaryList = $("#jstree2").jstree().get_selected(true);
    if (summaryList == "") {
        $("#fetch-data-btn").attr('disabled', true);
        $("#save-workboard-btn").attr('disabled', true);
    } else {
        $("#fetch-data-btn").attr('disabled', false);
        $("#save-workboard-btn").attr('disabled', false);
    }

}

function toastrMessages(message, type) {
    setTimeout(function () {
        toastr.options = {
            closeButton: true,
            progressBar: true,
            showMethod: 'slideDown',
            timeOut: 4000
        };
        if (type == 'error')
            toastr.error(encodeURIComponent(message));
        else if (type == 'success')
            toastr.success(message);
        else if (type == 'info')
            toastr.info(message);

    }, 500);
}

function customLoader(selector) {
    $(selector).waitMe({
        effect: 'stretch',
        text: 'Crunching Data....',
        bg: 'rgba(255, 255, 255, 0.7)',
        color: '#000'
    });
}

function loadEmptyJSTree() {
    $('#jstree2').jstree({
        "core": {
            "animation": 0,
            "check_callback": true,
            "themes": {"stripes": true},
            'data': ""
        },
        "checkbox": {"keep_selected_style": false},
        "plugins": [
            "checkbox", "search",
            "types", "crrm"
        ]
    });
}

function loadJSTreeWithData(data) {
    $('#jstree1').jstree({
        'plugins': ["wholerow", "checkbox"], 'core': {
            'data': JSON.parse(data)
        }
    });
}

function createSingleNode(parent_node, new_node_id, new_node_text, new_node_data, new_node_state, new_node_icon, collection_name, position) {
    $('#jstree2').jstree('create_node', $(parent_node), {
        "text": new_node_text,
        "id": new_node_id,
        "data": new_node_data,
        "state": new_node_state,
        "icon": new_node_icon,
        "collection_name": collection_name
    }, position, false, false);
    // generateWorkboardCallData();
    toggleFetchingDataButton();
}

function deleteSingleNode(eachNode) {
    $("#jstree2").jstree("delete_node", "#" + eachNode.id);

    /*
     $('#jstree2').jstree({core: {check_callback: true}});
     var treeNodes = $('#jstree2').jstree(true)._model.data;
     $('#jstree2').jstree(true).refresh();
     var updatedTreeNodes = delete treeNodes[eachNode.id];

     for (var propertyName in treeNodes) {
     if (treeNodes[propertyName].id != "#")
     createSingleNode("#jstree2", treeNodes[propertyName].id, treeNodes[propertyName].text,
     treeNodes[propertyName].data, treeNodes[propertyName].state, treeNodes[propertyName].icon,
     treeNodes[propertyName].parent, "last");
     }
     */
    // generateWorkboardCallData();
    toggleFetchingDataButton();
}

function getSelectedAnalysisType() {
    var analysisType = 'table';
    $('#analysis-types li').each(function () {
        if ($(this).hasClass('text-warning')) {
            analysisType = ($(this).data("type"));
            return false;
        }
    });
    return analysisType;
}

function callForWorkboardData(analysisType, variables) {
    var path = window.location.pathname;
    if (analysisType == 'table')
        path += "data_table/";
    else if (analysisType == 'bubble')
        path += "data_bubble/";
    else path += "data_chart/";

    customLoader('#workboard-tab-content');

    $.ajax({
        type: 'POST',
        url: path,
        data: {'variables': JSON.stringify(variables), 'type': analysisType},
        success: function (data) {
            $('#workboard-tab-content').html(data);
            $('#workboard-tab-content').waitMe('hide');
        },
        error: function (data) {
            console.log(data);
        }
    });
}

function generateChartRestriction(analysisType, variables) {
    var collection = Object.keys(variables);

    if (collection.length == 1) {
        var column_types = _.groupBy(variables[collection[0]], function (v) {
            return v.type;
        });

        if (column_types.integer == undefined) {
            column_types['integer'] = [];
        }
        if (column_types.string == undefined) {
            column_types['integer'] = [];
        }

        if (analysisType == 'bar' || analysisType == 'line') {
            if (column_types.integer.length >= 1 && column_types.string.length == 1) {
                return true;
            } else {
                toastrMessages('For Bar/Line Chart you need to select one string and multiple integer', 'info');
                return false;
            }
        }
        else if (analysisType == 'pie') {
            if (column_types.integer.length == 1 && column_types.string.length == 1) {
                return true;
            } else {
                toastrMessages('For Pie Chart you need to select one string and one integer', 'info');
                return false;
            }
        }
        else if (analysisType == 'bubble') {
            if (column_types.integer.length == 2 && column_types.string.length == 1) {
                return true;
            } else {
                toastrMessages('For Bubble Chart you need to select one string and two integer', 'info');
                return false;
            }
        }
        else return true;
    }
    else if (collection.length == 0) {
        toastrMessages('Please select some variables from Features List', 'info');
        return false;
    }
    else {
        toastrMessages('Our system currently not supporting Table Joins', 'info');
        return false;
    }
}

function generateWorkboardCallData() {
    var analysisType = getSelectedAnalysisType();
    var variables = getSummaryListSelectedVariables();

    if (generateChartRestriction(analysisType, variables)) {
        callForWorkboardData(analysisType, variables);
    }

}

function updateWorkboard(variables) {
    var path = window.location.pathname + "update/";
    var analysisType = getSelectedAnalysisType();

    if (generateChartRestriction(analysisType, variables)) {
        $.ajax({
            type: 'POST',
            url: path,
            data: {'variables': JSON.stringify(variables), 'type': analysisType},
            success: function (data) {
                toastrMessages(data, 'success');
            },
            error: function (data) {
                toastrMessages(data, 'error');
            }
        });
    }
}

function getProcessedBarChartData(data, inputType) {
    var fetchedData = JSON.parse(data);
    data = [];
    fetchedData.forEach(function (variable) {
        data.push({
            key: variable.var_name,
            values: variable.sum
        })
    });

    return data;
}

function getProcessedPieChartData(data, inputType) {
    var fetchedData = JSON.parse(data);
    data = [];
    fetchedData.forEach(function (variable) {
        variable.sum.forEach(function (item) {
            data.push(item);
        });
    });

    return data;
}

function populateJSTreeAndChart(variables) {
    variables = JSON.parse(variables);

    if (variables.length > 0) {
        $('#jstree1').on('loaded.jstree', (e, data) => {
            for (var i = 0; i < variables.length; i++) {
                var nodeId = variables[i].fields.variable_id;
                $('#jstree1').jstree(true).select_node(nodeId);
            }
            $("#fetch-data-btn").click();
        });
    }

}

function drawABarChart(data, selector) {
    nv.addGraph(function () {
        var height = 420;
        var chart = nv.models.multiBarChart()
                .x(function (d) {
                    return d.label
                })
                .y(function (d) {
                    return d.value
                })
                .height(height)
                .margin({left: 80, top: 20, bottom: 120, right: 20})
            ;
        chart.xAxis.rotateLabels('-45');

        chart.yAxis.tickFormat(d3.format(',.3f'))
            .rotateLabels('45');

        d3.select(selector)
            .datum(getProcessedBarChartData(data, 'sum'))
            .transition().duration(500)
            .call(chart)
        ;

        nv.utils.windowResize(chart.update);

        return chart;
    });
}

function drawAPieChart(data, selector) {
    nv.addGraph(function () {
        var chart = nv.models.pieChart()
            .x(function (d) {
                return d.label
            })
            .y(function (d) {
                return d.value
            })
            .showLabels(true);

        d3.select(selector)
            .datum(getProcessedPieChartData(data, 'sum'))
            .transition().duration(350)
            .call(chart);

        return chart;
    });
}

function drawALineChart(data, selector) {
    nv.addGraph(function () {
        var value_list = [];
        var categories = [];
        for (var i = 0; i < data.length; i++) {
            data[i].values.forEach(function (item) {
                value_list.push(item.index_col);
                categories.push(item.label);
            })
        }
        var chart = nv.models.lineChart()
                .x(function (d) {
                    return d.index_col
                })
                .y(function (d) {
                    return d.value
                })
                .margin({left: 80, top: 20, bottom: 120, right: 20})
            ;
        chart.xAxis.rotateLabels('-45')
            .showMaxMin(false)
            .tickValues(value_list)
            .tickFormat(function (d) {
                return categories[d];
            });

        chart.yAxis
            .tickFormat(d3.format(',.2f'));

        d3.select(selector)
            .datum(data)
            .transition().duration(500)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}

function drawABubbleChart(data, selector) {
    nv.addGraph(function () {
        var value_list = [];
        var categories = [];
        for (var i = 0; i < data.length; i++) {
            data[i].values.forEach(function (item) {
                value_list.push(item.index_col);
                categories.push(item.x);
            })
        }
        var chart = nv.models.scatterChart()
            .x(function (d) {
                return d.index_col
            })
            .y(function (d) {
                return d.y
            })
            .pointSize(function (d) {
                return d.size
            })
            .color(d3.scale.category10().range())
            .margin({left: 80, top: 20, bottom: 120, right: 20});

        chart.tooltip.contentGenerator(function (key) {
            return '<h3>' + categories[key.point.index_col] + '</h3>' +
                '<p>' + '{{ yaxis.upper }}' + ': ' + key.point.y + '</p>' +
                '<p>' + '{{ zaxis.upper }}' + ': ' + key.point.size + '</p>';
        });

        chart.xAxis.rotateLabels('-45')
            .showMaxMin(false)
            .tickValues(value_list)
            .tickFormat(function (d) {
                return categories[d];
            });

        chart.yAxis
            .tickFormat(d3.format(',.2f'));

        chart.scatter.showLabels(true);

        d3.select(selector)
            .datum(data)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
}