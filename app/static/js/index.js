function showTable() {
  let table = $('#problems-table tbody');
  table.empty();
  for (let i = 0; i < window.data.length; i++) {
    let row = $('<tr>');
    (function (data) {
      row.append($('<td>').text(data['pid']));
      row.append($('<td>').text(data['contest']));
      row.append(
        name2Str(data['pid'], data['name'], function () {
          window.details = data;
          Details();
        }).click(function (e) {
          if ($(e.target).prop('tagName') == 'TD' && !window.auto_status)
            changeStatus(data['pid']);
        })
      );
      row.append(difficulty2Str(data['difficulty'], data['cnt1']));
      row.append(quality2Str(data['quality'], data['cnt2']));
      row.append(
        $('<td>')
          .html('<a>Vote</a>')
          .click(function () {
            window.pid = data['pid'];
            Vote();
          })
      );
      row.append(
        $('<td>')
          .html('<a>Show Votes</a>')
          .click(function () {
            window.pid = data['pid'];
            $('#show-votes').modal('show');
            showVotes();
          })
      );
    })(data[i]);
    table.append(row);
  }
}
function changeStatus(pid) {
  status_list = JSON.parse(localStorage.getItem('status'));
  if (!status_list.hasOwnProperty(pid)) status_list[pid] = 0;
  else if (status_list[pid] == 0) status_list[pid] = 1;
  else if (status_list[pid] == 1) delete status_list[pid];
  localStorage.setItem('status', JSON.stringify(status_list));
  showTable();
  $.ajax({
    url: '/backend/update_status/',
    type: 'POST',
    data: {
      status: JSON.stringify(status_list),
    },
  });
}
function Vote() {
  $.ajax({
    url: '/backend/get_vote/',
    type: 'POST',
    data: {
      pid: window.pid,
    },
    success: function (data) {
      $('#difficulty').val(data['difficulty'] == '-1' ? '' : data['difficulty']);
      $('#quality').val(data['quality'] == '-1' ? '' : data['quality']);
      $('#comment').val(data['comment']);
      $('#vote').modal('show');
    },
  });
}
function showVotes() {
  let table = $('#vote-table tbody');
  table.empty();

  $.ajax({
    url: '/backend/get_votes/',
    type: 'POST',
    data: {
      pid: window.pid,
    },
    success: function (data) {
      data.forEach(function (vote) {
        let row = $('<tr>');
        row.append(difficulty2Str(vote['difficulty'], null));
        row.append(quality2Str(vote['quality'], null));
        row.append($('<td>').text(vote['comment']));
        addReportLink(row, vote['id']);
        table.append(row);
      });
    },
  });
}
function Details() {
  $('#details').modal('show');
  $('#details ul').empty();
  $('#details ul').append(
    $('<li>').text(`Contest: ${window.details['contest']}`)
  );
  $('#details ul').append($('<li>').text(`Name: ${window.details['name']}`));
  $('#details ul').append(
    $('<li>').append(
      $('<a>')
        .text(`Links: ${window.details['info']['links']}`)
        .attr('href', window.details['info']['links'])
    )
  );
  Object.entries(window.details['info']).forEach(function ([key, value]) {
    if (key != 'links') {
      $('#details ul').append($('<li>').text(`${key}: ${value}`));
    }
  });
}

function addReportLink(row, id) {
  row.append(
    $('<td>')
      .html('<a>Report</a>')
      .click(function () {
        $.ajax({
          url: '/backend/report/',
          type: 'POST',
          data: {
            id: id,
          },
          success: function () {
            alert('Report!');
          },
        });
      })
  );
}

function sortData(sortBy) {
  try {
    window.data.sort(function (a, b) {
      if (a[sortBy] == null && b[sortBy] == null) {
        return 0;
      }
      if (a[sortBy] == null) {
        return 1;
      }
      if (b[sortBy] == null) {
        return -1;
      }
      return a[sortBy] > b[sortBy] ? -1 : 1;
    });
    showTable();
  } catch (error) {
    console.error('Sorting error: ', error);
  }
}
