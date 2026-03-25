(function () {
  'use strict';

  var COLORS = [
    '#e74c3c','#3498db','#27ae60','#f39c12','#9b59b6',
    '#16a085','#e67e22','#c0392b','#2980b9','#8e44ad',
    '#1abc9c','#d35400','#2c3e50','#27ae60'
  ];

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

  function renderCadence(projects) {
    var container = document.getElementById('cadence-map');
    if (!container) return;

    var TODAY = new Date();
    var STALE_DAYS = 45;

    // Sort oldest first
    projects.sort(function (a, b) {
      return parseDate(a.startDate) - parseDate(b.startDate);
    });

    // Assign lanes using greedy algorithm
    var laneEnds = []; // tracks when each lane becomes free
    projects.forEach(function (p, i) {
      p.color = COLORS[i % COLORS.length];
      var startDate = parseDate(p.startDate);
      var isEnded = (p.status === 'finished' || p.status === 'abandoned');
      var endDate = isEnded ? parseDate(p.lastEdited) : TODAY;
      p._startDate = startDate;
      p._endDate = endDate;
      p._isEnded = isEnded;

      // Find a free lane
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
    var LANE_W = 12;
    var PAD_T = 22;
    var PAD_B = 14;
    var PX_PER_DAY = 0.55;

    // Date range
    var allStartDates = projects.map(function (p) { return p._startDate; });
    var minDate = new Date(Math.min.apply(null, allStartDates));
    var totalMs = TODAY - minDate;
    var totalDays = totalMs / 86400000;
    var svgH = Math.round(PAD_T + totalDays * PX_PER_DAY + PAD_B);
    var svgW = TRUNK_X + (numLanes + 1) * LANE_W + 6;

    function dateToY(date) {
      var days = (TODAY - date) / 86400000;
      return Math.round(PAD_T + days * PX_PER_DAY);
    }

    var parts = [];

    // Main trunk
    parts.push('<line x1="' + TRUNK_X + '" y1="' + PAD_T + '" x2="' + TRUNK_X + '" y2="' + (svgH - PAD_B) + '" stroke="#bbb" stroke-width="2"/>');

    // "Now" label at top
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

      // Horizontal connector: trunk → branch column
      parts.push('<line x1="' + TRUNK_X + '" y1="' + startY + '" x2="' + branchX + '" y2="' + startY + '" stroke="' + c + '" stroke-width="2"/>');

      // Vertical branch line
      parts.push('<line x1="' + branchX + '" y1="' + startY + '" x2="' + branchX + '" y2="' + endY + '" stroke="' + c + '" stroke-width="2"' + dashAttr + '/>');

      // Start dot
      parts.push('<circle cx="' + branchX + '" cy="' + startY + '" r="3" fill="' + c + '"/>');

      if (p.status === 'finished') {
        // Merge back to trunk
        parts.push('<line x1="' + branchX + '" y1="' + endY + '" x2="' + TRUNK_X + '" y2="' + endY + '" stroke="' + c + '" stroke-width="2"/>');
        parts.push('<circle cx="' + TRUNK_X + '" cy="' + endY + '" r="3" fill="' + c + '"/>');
      } else if (p.status === 'abandoned') {
        // X marker
        var x = branchX, y = endY;
        parts.push('<line x1="' + (x-4) + '" y1="' + (y-4) + '" x2="' + (x+4) + '" y2="' + (y+4) + '" stroke="' + c + '" stroke-width="2"/>');
        parts.push('<line x1="' + (x+4) + '" y1="' + (y-4) + '" x2="' + (x-4) + '" y2="' + (y+4) + '" stroke="' + c + '" stroke-width="2"/>');
      } else {
        // Ongoing: dot at top connecting to "Now"
        parts.push('<circle cx="' + branchX + '" cy="' + PAD_T + '" r="3" fill="' + c + '"/>');
      }
    });

    var svg = '<svg width="' + svgW + '" height="' + svgH + '" xmlns="http://www.w3.org/2000/svg" style="display:block">' + parts.join('') + '</svg>';

    // Legend
    var legendParts = ['<div class="cadence-legend">'];
    // Show newest first in legend
    var legendProjects = projects.slice().reverse();
    legendProjects.forEach(function (p) {
      var statusLabel = '';
      if (p.status === 'finished') statusLabel = ' <em style="color:#aaa">(done)</em>';
      else if (p.status === 'abandoned') statusLabel = ' <em style="color:#aaa">(dropped)</em>';
      var isStale = !p._isEnded &&
        (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;
      if (isStale) statusLabel = ' <em style="color:#aaa">(stale)</em>';
      legendParts.push(
        '<span style="color:' + p.color + '">&#9632;</span> ' +
        '<a href="./' + p.folder + '" style="color:#555;text-decoration:none;font-size:10px">' + p.name + '</a>' +
        statusLabel + '<br>'
      );
    });
    legendParts.push('</div>');

    container.innerHTML = svg + legendParts.join('');
  }

  // Load projects.json and render
  var req = new XMLHttpRequest();
  req.open('GET', '/projects.json', true);
  req.onreadystatechange = function () {
    if (req.readyState === 4) {
      if (req.status === 200) {
        try {
          var projects = JSON.parse(req.responseText);
          renderCadence(projects);
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
