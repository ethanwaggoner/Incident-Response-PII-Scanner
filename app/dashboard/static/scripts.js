let customSearchData = [];

function validateButton() {
  $('#run').html('Validating...').prop('disabled', true);
  $('#hiddenRun').val('run');

  // Include customSearchData in the form data
  $('<input>').attr({
    type: 'hidden',
    name: 'custom_search_data',
    value: JSON.stringify(customSearchData),
  }).appendTo('#pii-form');

  setTimeout(function () {
    $('#pii-form').submit();
  }, 100);
}


  function validateAndAdd() {
  const nameInput = $('input[name="custom_search_name[]"]');
  const regexInput = $('input[name="custom_search_regex[]"]');
  const nameValue = nameInput.val().trim();
  const regexValue = regexInput.val().trim();

  if (nameValue && regexValue) {
    const newRow = $('<tr></tr>');
    newRow.append(`<td>${nameValue}</td>`);
    newRow.append(`<td>${regexValue}</td>`);
    $('#custom-regex').find('tbody').append(newRow);

    customSearchData.push({name: nameValue, regex: regexValue});

    // Clear the input fields after adding the row
    nameInput.val('');
    regexInput.val('');
  } else {
    alert('Please enter valid Name and Regex values');
  }
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

   $('#regex-btn').on('click', function (event) {
  event.preventDefault();
  validateAndAdd();
});

});