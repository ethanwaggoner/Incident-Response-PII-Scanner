 function validateButton() {
    $('#run').html('Validating...').prop('disabled', true);
    $('#hiddenRun').val('run');

    setTimeout(function () {
      $('#pii-form').submit();
    }, 100);
  }

  $(document).ready(function() {

  function refreshDataTable() {
    $('#pii-table').DataTable().ajax.reload(null, false);
  }

  function updateProgressBar() {
    const numerator = parseInt($('#numerator').text());
    const denominator = parseInt($('#denominator').text());
    let percentage = 0;

    if (denominator > 0) {
      percentage = (numerator / denominator) * 100;
    }

    $('#progress-bar')
      .css('width', percentage + '%')
      .attr('aria-valuenow', percentage)
      .text(percentage.toFixed(2) + '%');
  }

  function animateRunningText() {
  $('#run').prop('disabled', true).html(' Running <span class="spinner"></span>');
}


  function checkCompletion() {
    const numerator = parseInt($('#numerator').text());
    const denominator = parseInt($('#denominator').text());

    if (numerator === denominator && numerator > 0) {
      $('#run').prop('disabled', false).text('Run Scan');
    } else if (numerator < denominator) {
      animateRunningText();
    }
      }

  function fetchDataAndUpdate() {
  const piiCountRequest = $.get('/dashboard/pii-count');
  const totalFilesScannedRequest = $.get('/dashboard/total-files-scanned');
  const totalFilesRequest = $.get('/dashboard/total-files');

  $.when(piiCountRequest, totalFilesScannedRequest, totalFilesRequest).done(function (piiCountData, totalFilesScannedData, totalFilesData) {
    $('#pii-count').text(piiCountData[0]);
    $('#numerator').text(totalFilesScannedData[0]);
    $('#denominator').text(totalFilesData[0]);

    updateProgressBar();
    checkCompletion();
    refreshDataTable();
  });
}


  setInterval(fetchDataAndUpdate, 1000);

  $('#pii-table').DataTable({
    dom: 'Bfrtip',
    buttons: [
      {
        extend: 'csv',
        className: 'btn',
        text: 'Export to CSV',
      },
      {
        extend: 'copy',
        className: 'btn',
        text: 'Copy to Clipboard',
      },
    ],
    lengthChange: false,
    paging: true,
    info: false,
    pagesize: 15,
    scrollY: true,

    ajax: {
      url: '/dashboard/table-results',
      dataSrc: '',
      type: 'GET'
    },
    columns: [
      { data: 'pii_type' },
      { data: 'file_path' },
      { data: 'pii' }
    ]
  });
});