$(document).ready(function () {
  loadEmptyJSTree();
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
      generateWorkboardCallData();
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

  $("#analysis-types li").click(function () {
    $('#analysis-types li').each(function () {
      $(this).removeClass('text-warning');
    });
    $(this).addClass('text-warning');
    generateWorkboardCallData();
  });

});

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

  }, 500);
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
  generateWorkboardCallData();
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
  generateWorkboardCallData();
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
  else path += "data_chart/";

  $.ajax({
    type: 'POST',
    url: path,
    data: {'variables': JSON.stringify(variables)},
    success: function (data) {
      $('#workboard-tab-content').html(data);
    },
    error: function (data) {
      console.log(data);
    }
  });
}

function generateWorkboardCallData() {
  var analysisType = getSelectedAnalysisType();
  var summaryList = $("#jstree2").jstree().get_selected(true);
  var variables = {};
  summaryList.forEach(function (node) {
    if (variables[node.original.collection_name] == undefined) {
      variables[node.original.collection_name] = [];
      variables[node.original.collection_name].push(node.text);
    }
    else variables[node.original.collection_name].push(node.text);
  });

  callForWorkboardData(analysisType, variables);

}