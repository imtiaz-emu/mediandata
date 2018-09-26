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