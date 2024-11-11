function showTable() {
    let table = $('#problems-table tbody');
    table.empty();
    for (let i = 0; i < data.length; i++) {
        let row = $('<tr>');
        row.append($('<td>').text(data[i]['pid']));
        row.append($('<td>').text(data[i]['contest']));
        row.append($('<td>').html(data[i]['name']));
        row.append(difficulty2Str(data[i]['difficulty'], data[i]['cnt1']));
        row.append(quality2Str(data[i]['quality'], data[i]['cnt2']));
        (function (pid) {
            row.append($('<td>').html("<a>Vote</a>").click(function () {
                window.pid = pid;
                Vote();
            }));
            row.append($('<td>').html("<a>Show Votes</a>").click(function () {
                window.pid = pid;
                $('#show-votes').modal('show');
                showVotes();
            }));
        })(data[i]['pid']);
        table.append(row);
    }
}
function Vote() {
    $.ajax({
        url: '/backend/get_vote/',
        type: 'POST',
        data: {
            pid: window.pid
        },
        success: function (data) {
            $('#difficulty').val(data['difficulty']);
            $('#quality').val(data['quality']);
            $('#comment').val(data['comment']);
            $('#vote').modal('show');
        }
    });
}
function showVotes() {
    let table = $('#vote-table tbody');
    table.empty();

    $.ajax({
        url: '/backend/get_votes/',
        type: 'POST',
        data: {
            pid: window.pid
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
        }
    });
}

function addReportLink(row, id) {
    row.append($('<td>').html("<a>Report</a>").click(function () {
        $.ajax({
            url: '/backend/report/',
            type: 'POST',
            data: {
                id: id
            },
            success: function () {
                alert("Report!");
            }
        });
    }));
}

function sortData(sortBy) {
    try {
        data.sort(function (a, b) {
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
        console.error("Sorting error: ", error);
    }
}