let customSearchData = [];

function validateButton(event) {
  $('#run').html('Validating. This may take a few minutes.').prop('disabled', true);
  $('#hiddenRun').val('run');

  // Include customSearchData in the form data
  $('<input>').attr({
    type: 'hidden',
    name: 'custom_search_data',
    value: JSON.stringify(customSearchData),
  }).appendTo('#pii-form');

  setTimeout(function (event) {
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

    // Create a new table cell with a button for removing the row
    const removeButton = $('<button type="button" class="remove-btn">Delete</button>');
    removeButton.on('click', function () {
      removeRow(newRow);
    });
    const removeButtonCell = $('<td></td>');
    removeButtonCell.append(removeButton);
    newRow.append(removeButtonCell);

    $('#custom-regex').find('tbody').append(newRow);

    customSearchData.push({name: nameValue, regex: regexValue});

    // Clear the input fields after adding the row
    nameInput.val('');
    regexInput.val('');
  } else {
    alert('Please enter valid Name and Regex values');
  }
}

// Function to remove the row and update the customSearchData array
function removeRow(row) {
  const rowIndex = row.index();
  customSearchData.splice(rowIndex, 1);
  row.remove();
}

  $(document).ready(function() {

  function refreshDataTable() {
    $('#pii-table').DataTable().ajax.reload(null, false);
  }

  function updateProgressBar() {
    const scan_status = $.get('/dashboard/scan-status');

    const numerator = parseInt($('#numerator').text());
    const denominator = parseInt($('#denominator').text());
    let percentage = 0;

    if (denominator > 0) {
      if (scan_status === 'Completed') {
        percentage = 100;
        $('#numerator').html(denominator)
      } else {
        percentage = (numerator / denominator) * 100;
      }
    }

    $('#progress-bar')
      .css('width', percentage + '%')
      .attr('aria-valuenow', percentage)
      .text(percentage.toFixed(2) + '%');
  }

  function animateRunningText() {
  $('#run').prop('disabled', true).html(' Running <span class="spinner"></span>');
}


  function fetchDataAndUpdate() {
  $.get('/dashboard/pii-count', function(piiCountData) {
    $('#pii-count').text(piiCountData);
  });

  $.get('/dashboard/total-files-scanned', function(totalFilesScannedData) {
    $('#numerator').text(totalFilesScannedData);
  });

  $.get('/dashboard/total-files', function(totalFilesData) {
    $('#denominator').text(totalFilesData);
  });

  $.get('/dashboard/scan-status', function(scan_status) {
    if (scan_status === 'Completed') {
      $('#run').prop('disabled', true).text('Completed');
      $('#get_directory').prop('disabled', true);
      $('#progress-bar')
      .css('width', 100 + '%')
      .attr('aria-valuenow', 100);


    } else {
      const numerator = parseInt($('#numerator').text());
      const denominator = parseInt($('#denominator').text());



      if (numerator < denominator) {
        animateRunningText();
      }
      updateProgressBar();
    }
  });

  refreshDataTable();
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