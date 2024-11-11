function difficulty2Str(difficulty, cnt) {
  var res = '<td style="';
  if (difficulty >= 2400) {
    res += 'color: red;';
  } else if (difficulty >= 2100) {
    res += 'color: rgb(255,140,0);';
  } else if (difficulty >= 0) {
    res += 'color: rgb(170,0,170);';
  } else if (difficulty >= 1600) {
    res += 'color: blue;';
  } else if (difficulty >= 1400) {
    res += 'color: rgb(3,168,158);';
  } else if (difficulty >= 1200) {
    res += 'color: green;';
  } else if (difficulty >= 1000) {
    res += 'color: rgb(136,204,34);';
  } else {
    res += 'color: gray;';
  }
  res +=
    `font-weight: 500;" data-toggle="popover" ` +
    (cnt == null ? '' : `data-tooltip="Number of votes: ${cnt}"`) +
    ` data-original-title="" title=""> ${difficulty2Circle(difficulty)}${difficulty == null ? 'N/A' : Math.round(difficulty)}</td>`;
  return res;
}

function difficulty2Circle(difficulty) {
  var percentage = 0;
  var col = '';
  if (difficulty >= 2400) {
    col += 'red';
    percentage = (difficulty - 2400) / 9;
  } else if (difficulty >= 2100) {
    col += 'rgb(255,140,0)';
    percentage = (difficulty - 2100) / 3;
  } else if (difficulty >= 0) {
    col += 'rgb(170,0,170)';
    percentage = (difficulty - 0) / 2;
  } else if (difficulty >= 1600) {
    col += 'blue';
    percentage = (difficulty - 1600) / 3;
  } else if (difficulty >= 1400) {
    col += 'rgb(3,168,158)';
    percentage = (difficulty - 1400) / 2;
  } else if (difficulty >= 1200) {
    col += 'green';
    percentage = (difficulty - 1200) / 2;
  } else if (difficulty >= 1000) {
    col += 'rgb(136,204,34)';
    percentage = (difficulty - 1000) / 2;
  } else {
    col += 'gray';
    percentage = difficulty / 10;
  }
  percentage = Math.round(10 * percentage) / 10;
  var res = `<span style="display: inline-block; 
                            border-radius: 50%; 
                            border-style: solid;
                            border-width: 1px;
                            margin-right: 5px;
                            height: 12px;
                            width: 12px;
                            border-color: ${col};
                            background: linear-gradient(to top, ${col} 0%, ${col} ${percentage}%, rgba(0, 0, 0, 0) ${percentage}%, rgba(0, 0, 0, 0) 100%);"></span>`;
  return res;
}

function quality2Str(quality, cnt) {
  var showQuality = Math.round(quality * 10) / 10;
  var res = '<td style="';
  if (quality == null) {
    res += 'color: gray;';
    showQuality = 'N/A';
  } else {
    quality = Math.round(quality);
    if (quality == 1) {
      res += 'color: gray;';
    } else if (quality == 2) {
      res += 'color: rgb(144, 238, 144);';
    } else if (quality == 3) {
      res += 'color: rgb(80, 200, 120);';
    } else if (quality == 4) {
      res += 'color: rgb(34, 139, 34);';
    } else {
      res += 'color: rgb(0, 128, 0);';
    }
  }
  res +=
    `font-weight: 500;" data-toggle="popover" ` +
    (cnt == null ? '' : `data-tooltip="Number of votes: ${cnt}"`) +
    ` data-original-title="" title="">${showQuality}</td>`;
  return res;
}
