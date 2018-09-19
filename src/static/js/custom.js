$(document).ready(function () {

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
      toastr.error(message);
    else if (type == 'success')
      toastr.success(message);

  }, 500);
}