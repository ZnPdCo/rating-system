function name2Str(pid, name, func) {
  status_list = JSON.parse(localStorage.getItem('status'));
  content = $('<a>').text(name).click(func);
  if (!status_list.hasOwnProperty(pid)) return $('<td>').append(content);
  if (status_list[pid] == 0)
    return $('<td>')
      .css({ 'background-color': 'rgb(255, 238, 186)' })
      .append(content);
  if (status_list[pid] == 1)
    return $('<td>')
      .css({ 'background-color': 'rgb(195, 230, 203)' })
      .append(content);
  return $('<td>').append(content);
}

function difficulty2Str(difficulty, cnt) {
  var res = $('<td>')
  if(difficulty == null) {
    res.css('color', 'gray');
  } else if (difficulty >= 2400) {
    res.css('color', 'red');
  } else if (difficulty >= 2100) {
    res.css('color', 'rgb(255,140,0)');
  } else if (difficulty >= 1900) {
    res.css('color', 'rgb(170,0,170)');
  } else if (difficulty >= 1600) {
    res.css('color', 'blue');
  } else if (difficulty >= 1400) {
    res.css('color', 'rgb(3,168,158)');
  } else if (difficulty >= 1200) {
    res.css('color', 'green');
  } else if (difficulty >= 1000) {
    res.css('color', 'rgb(136,204,34)');
  } else {
    res.css('color', 'gray');
  }
  res.css('font-weight', '500')
  res.attr('data-toggle', 'popover')
  if(cnt != null) res.attr('data-tooltip', `Number of votes: ${cnt}`)
  res.append(difficulty2Circle(difficulty));
  res.append(` ${difficulty == null ? 'N/A' : Math.round(difficulty)}`);
  return res;
}

function difficulty2Circle(difficulty) {
  var percentage = 0;
  var col = '';
  var res = $('<span>');
  res.css({'display': 'inline-block', 
              'border-radius': '50%', 
              'border-style':'solid',
              'border-width': '1px',
             'margin-right': '5px',
              'height': '12px',
              'width': '12px'});
  if(difficulty == null) {
    col += 'gray';
    percentage = 0;
  } else if (difficulty >= 2400 && difficulty < 3000) {
    col += 'red';
    percentage = (difficulty - 2400) / 6;
  } else if (difficulty >= 2100) {
    col += 'rgb(255,140,0)';
    percentage = (difficulty - 2100) / 3;
  } else if (difficulty >= 1900) {
    col += 'rgb(170,0,170)';
    percentage = (difficulty - 1900) / 2;
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
    percentage = (difficulty - 800) / 2;
  }
  if(difficulty >= 3400) {
    res.css({'border-color': '#FFD700',
    'background': 'linear-gradient(to right, #FFD700, white, #FFD700)'});
  } else if(difficulty >= 3200) {
    res.css({'border-color': '#808080',
    'background': 'linear-gradient(to right, #808080, white, #808080)'});
} else if(difficulty >= 3000) {
  res.css({'border-color': '#965C2C',
  'background': 'linear-gradient(to right, #965C2C, #FFDABD, #965C2C)'});
}else {
    percentage = Math.round(10 * percentage) / 10;
    res.css({
              'border-color': col,
              'background': `linear-gradient(to top, ${col} 0%, ${col} ${percentage}%, rgba(0, 0, 0, 0) ${percentage}%, rgba(0, 0, 0, 0) 100%)`})
  }
  return res;
}

function quality2Str(quality, cnt) {
  var showQuality = Math.round(quality * 10) / 10;
  var res = $('<td>')
  if (quality == null) {
    res.css('color', 'gray');
    showQuality = 'N/A';
  } else {
    quality = Math.round(quality);
    if(quality == 0) {
      res.css('color', 'rgb(157, 108, 73)');
      showQuality = '💩 ' + showQuality;
    } else if (quality == 1) {
      res.css('color', 'gray');
    } else if (quality == 2) {
      res.css('color', 'rgb(144, 238, 144)');
    } else if (quality == 3) {
      res.css('color', 'rgb(80, 200, 120)');
    } else if (quality == 4) {
      res.css('color', 'rgb(34, 139, 34)');
    } else {
      res.css('color', 'rgb(0, 128, 0)')
    }
  }
  res.css('font-weight', '500')
  res.attr('data-toggle', 'popover')
  if(cnt != null) res.attr('data-tooltip', `Number of votes: ${cnt}`)
  res.text(showQuality);
  return res;
}
