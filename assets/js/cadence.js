(function () {
  'use strict';

  var COLORS = [
    '#e74c3c','#3498db','#27ae60','#f39c12','#9b59b6',
    '#16a085','#e67e22','#c0392b','#2980b9','#8e44ad',
    '#1abc9c','#d35400','#2c3e50','#c0392b'
  ];

  var MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  function parseDate(str) {
    if (!str || str === 'On going') return new Date();
    var parts = str.split('/');
    if (parts.length !== 3) return new Date();
    var d = parseInt(parts[0], 10);
    var m = parseInt(parts[1], 10) - 1;
    var y = parseInt(parts[2], 10);
    if (y < 100) y += 2000;
    return new Date(y, m, d);
  }

  function shortDate(str) {
    if (!str || str === 'On going') return '';
    var parts = str.split('/');
    if (parts.length !== 3) return '';
    var m = parseInt(parts[1], 10) - 1;
    var y = parseInt(parts[2], 10);
    if (y < 100) y += 2000;
    return MONTHS[m] + " '" + String(y).slice(-2);
  }

  function renderStats(projects, container) {
    var ongoing = 0, finished = 0, abandoned = 0;
    var finishedDays = [];
    var TODAY = new Date();

    projects.forEach(function (p) {
      if (p.status === 'finished') {
        finished++;
        var days = Math.round((parseDate(p.lastEdited) - parseDate(p.startDate)) / 86400000);
        if (days > 0) finishedDays.push(days);
      } else if (p.status === 'abandoned') {
        abandoned++;
      } else {
        ongoing++;
      }
    });

    var avgLine = '';
    if (finishedDays.length > 0) {
      var avg = Math.round(finishedDays.reduce(function (a, b) { return a + b; }, 0) / finishedDays.length);
      avgLine = '<span style="color:#3498db">&#10003;</span> avg ' + avg + ' days to finish<br>';
    } else {
      // Show average age of open projects
      var ages = projects
        .filter(function (p) { return p.status === 'ongoing'; })
        .map(function (p) { return Math.round((TODAY - parseDate(p.startDate)) / 86400000); });
      if (ages.length > 0) {
        var avgAge = Math.round(ages.reduce(function (a, b) { return a + b; }, 0) / ages.length);
        avgLine = '<span style="color:#aaa">&#9202;</span> avg age ' + avgAge + ' days<br>';
      }
    }

    container.innerHTML =
      '<span style="color:#27ae60">&#9679;</span> ' + ongoing + ' ongoing&nbsp;&nbsp;' +
      '<span style="color:#3498db">&#10003;</span> ' + finished + ' done&nbsp;&nbsp;' +
      '<span style="color:#e74c3c">&#10007;</span> ' + abandoned + ' dropped<br>' +
      avgLine;
  }

  function renderCadence(projects) {
    var mapContainer = document.getElementById('cadence-map');
    var statsContainer = document.getElementById('cadence-stats');
    if (!mapContainer) return;

    var TODAY = new Date();
    var STALE_DAYS = 45;

    // Sort oldest first
    projects.sort(function (a, b) {
      return parseDate(a.startDate) - parseDate(b.startDate);
    });

    if (statsContainer) renderStats(projects, statsContainer);

    // Assign lanes with greedy algorithm
    var laneEnds = [];
    projects.forEach(function (p, i) {
      p.color = COLORS[i % COLORS.length];
      var startDate = parseDate(p.startDate);
      var isEnded = (p.status === 'finished' || p.status === 'abandoned');
      var endDate = isEnded ? parseDate(p.lastEdited) : TODAY;
      p._startDate = startDate;
      p._endDate = endDate;
      p._isEnded = isEnded;

      var lane = -1;
      for (var l = 0; l < laneEnds.length; l++) {
        if (laneEnds[l] <= startDate) {
          lane = l;
          laneEnds[l] = endDate;
          break;
        }
      }
      if (lane === -1) {
        lane = laneEnds.length;
        laneEnds.push(endDate);
      }
      p._lane = lane;
    });

    var numLanes = laneEnds.length;

    // Layout constants
    var TRUNK_X = 12;
    var LANE_W = 10;
    var LABEL_PAD = 6;
    var LABEL_W = 44;   // width reserved for date text
    var PAD_T = 22;
    var PAD_B = 14;
    var PX_PER_DAY = 0.55;

    var TEXT_X = TRUNK_X + (numLanes + 1) * LANE_W + LABEL_PAD;

    // Date range
    var allStartDates = projects.map(function (p) { return p._startDate; });
    var minDate = new Date(Math.min.apply(null, allStartDates));
    var totalMs = TODAY - minDate;
    var totalDays = totalMs / 86400000;
    var svgH = Math.round(PAD_T + totalDays * PX_PER_DAY + PAD_B);
    var svgW = TEXT_X + LABEL_W;

    function dateToY(date) {
      var days = (TODAY - date) / 86400000;
      return Math.round(PAD_T + days * PX_PER_DAY);
    }

    var parts = [];

    // Main trunk
    parts.push('<line x1="' + TRUNK_X + '" y1="' + PAD_T + '" x2="' + TRUNK_X + '" y2="' + (svgH - PAD_B) + '" stroke="#bbb" stroke-width="2"/>');

    // "Now" dot + label
    parts.push('<circle cx="' + TRUNK_X + '" cy="' + PAD_T + '" r="4" fill="#555"/>');
    parts.push('<text x="' + (TRUNK_X + 8) + '" y="' + (PAD_T + 4) + '" font-size="9" fill="#555" font-family="sans-serif">Now</text>');

    // Draw each project branch
    projects.forEach(function (p) {
      var startY = dateToY(p._startDate);
      var endY = p._isEnded ? dateToY(p._endDate) : PAD_T;
      var branchX = TRUNK_X + (p._lane + 1) * LANE_W;
      var c = p.color;

      var isStale = !p._isEnded &&
        (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;

      var dashAttr = '';
      if (p.status === 'abandoned') dashAttr = ' stroke-dasharray="4,3"';
      else if (isStale) dashAttr = ' stroke-dasharray="2,2"';

      // Horizontal connector: trunk → branch
      parts.push('<line x1="' + TRUNK_X + '" y1="' + startY + '" x2="' + branchX + '" y2="' + startY + '" stroke="' + c + '" stroke-width="2"/>');

      // Vertical branch line
      parts.push('<line x1="' + branchX + '" y1="' + startY + '" x2="' + branchX + '" y2="' + endY + '" stroke="' + c + '" stroke-width="2"' + dashAttr + '/>');

      // Start dot
      parts.push('<circle cx="' + branchX + '" cy="' + startY + '" r="3" fill="' + c + '"/>');

      // Start date label
      var startLabel = shortDate(p.startDate);
      if (startLabel) {
        parts.push('<text x="' + TEXT_X + '" y="' + (startY + 3) + '" font-size="8" fill="' + c + '" font-family="sans-serif" opacity="0.85">' + startLabel + '</text>');
      }

      if (p.status === 'finished') {
        // Merge horizontal back to trunk
        parts.push('<line x1="' + branchX + '" y1="' + endY + '" x2="' + TRUNK_X + '" y2="' + endY + '" stroke="' + c + '" stroke-width="2"/>');
        parts.push('<circle cx="' + TRUNK_X + '" cy="' + endY + '" r="3" fill="' + c + '"/>');
        // End date label
        var endLabel = shortDate(p.lastEdited);
        if (endLabel) {
          parts.push('<text x="' + TEXT_X + '" y="' + (endY + 3) + '" font-size="8" fill="' + c + '" font-family="sans-serif" opacity="0.7">' + endLabel + '</text>');
        }
      } else if (p.status === 'abandoned') {
        var x = branchX, y = endY;
        parts.push('<line x1="' + (x-4) + '" y1="' + (y-4) + '" x2="' + (x+4) + '" y2="' + (y+4) + '" stroke="' + c + '" stroke-width="2"/>');
        parts.push('<line x1="' + (x+4) + '" y1="' + (y-4) + '" x2="' + (x-4) + '" y2="' + (y+4) + '" stroke="' + c + '" stroke-width="2"/>');
      } else {
        // Ongoing: dot connecting up to "Now"
        parts.push('<circle cx="' + branchX + '" cy="' + PAD_T + '" r="3" fill="' + c + '"/>');
      }
    });

    var svg = '<svg width="' + svgW + '" height="' + svgH + '" xmlns="http://www.w3.org/2000/svg" style="display:block">' + parts.join('') + '</svg>';

    // Legend (newest first, root-relative links)
    var legendParts = ['<div class="cadence-legend">'];
    projects.slice().reverse().forEach(function (p) {
      var statusLabel = '';
      if (p.status === 'finished') statusLabel = ' <em style="color:#aaa">(done)</em>';
      else if (p.status === 'abandoned') statusLabel = ' <em style="color:#aaa">(dropped)</em>';
      else {
        var isStale = (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;
        if (isStale) statusLabel = ' <em style="color:#aaa">(stale)</em>';
      }
      legendParts.push(
        '<span style="color:' + p.color + '">&#9632;</span> ' +
        '<a href="/' + p.folder + '" style="color:#555;text-decoration:none;font-size:10px">' + p.name + '</a>' +
        statusLabel + '<br>'
      );
    });
    legendParts.push('</div>');

    mapContainer.innerHTML = svg + legendParts.join('');
  }

  // Fetch projects.json from root
  var req = new XMLHttpRequest();
  req.open('GET', '/projects.json', true);
  req.onreadystatechange = function () {
    if (req.readyState === 4) {
      if (req.status === 200) {
        try {
          renderCadence(JSON.parse(req.responseText));
        } catch (e) {
          console.error('cadence.js: failed to parse projects.json', e);
        }
      } else {
        console.warn('cadence.js: projects.json not found (status ' + req.status + ')');
      }
    }
  };
  req.send();
})();
