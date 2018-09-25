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