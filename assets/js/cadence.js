(function () {
  'use strict';

  var COLORS = [
    '#58a6ff','#3fb950','#f0883e','#d2a8ff','#ffa657',
    '#79c0ff','#7ee787','#ff7b72','#e3b341','#a371f7',
    '#56d364','#ff9a8b','#63bdff','#cae8ff'
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
      avgLine = '<span class="cs-val" style="color:#3fb950">' + avg + 'd</span> avg to finish&nbsp;&nbsp;';
    } else {
      var ages = projects
        .filter(function (p) { return p.status === 'ongoing'; })
        .map(function (p) { return Math.round((TODAY - parseDate(p.startDate)) / 86400000); });
      if (ages.length > 0) {
        var avgAge = Math.round(ages.reduce(function (a, b) { return a + b; }, 0) / ages.length);
        avgLine = '<span class="cs-val">' + avgAge + 'd</span> avg age&nbsp;&nbsp;';
      }
    }

    container.innerHTML =
      '<span class="cs-dot" style="color:#3fb950">●</span> <span class="cs-val">' + ongoing + '</span> active&nbsp;&nbsp;' +
      '<span class="cs-dot" style="color:#58a6ff">✓</span> <span class="cs-val">' + finished + '</span> done&nbsp;&nbsp;' +
      '<span class="cs-dot" style="color:#ff7b72">✗</span> <span class="cs-val">' + abandoned + '</span> dropped<br>' +
      avgLine;
  }

  function renderCadence(projects) {
    var mapContainer = document.getElementById('cadence-map');
    var statsContainer = document.getElementById('cadence-stats');
    if (!mapContainer) return;

    var TODAY = new Date();
    var STALE_DAYS = 45;

    projects.sort(function (a, b) { return parseDate(a.startDate) - parseDate(b.startDate); });

    if (statsContainer) renderStats(projects, statsContainer);

    // Assign lanes
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
        if (laneEnds[l] <= startDate) { lane = l; laneEnds[l] = endDate; break; }
      }
      if (lane === -1) { lane = laneEnds.length; laneEnds.push(endDate); }
      p._lane = lane;
    });

    var numLanes = laneEnds.length;

    // Layout
    var TRUNK_X   = 10;
    var LANE_W    = 10;
    var LABEL_PAD = 8;
    var LABEL_W   = 46;
    var PAD_T     = 24;
    var PAD_B     = 10;
    var PX_PER_DAY = 0.55;
    var MIN_LABEL_GAP = 12; // px between date labels

    var TEXT_X = TRUNK_X + (numLanes + 1) * LANE_W + LABEL_PAD;

    var allStartDates = projects.map(function (p) { return p._startDate; });
    var minDate = new Date(Math.min.apply(null, allStartDates));
    var totalDays = (TODAY - minDate) / 86400000;
    var svgH = Math.round(PAD_T + totalDays * PX_PER_DAY + PAD_B);
    var svgW = TEXT_X + LABEL_W;

    function dateToY(date) {
      return Math.round(PAD_T + (TODAY - date) / 86400000 * PX_PER_DAY);
    }

    // Track placed label Y positions to prevent overlap
    var placedLabels = [];
    function tryLabel(y, text, color, opacity) {
      for (var i = 0; i < placedLabels.length; i++) {
        if (Math.abs(placedLabels[i] - y) < MIN_LABEL_GAP) return '';
      }
      placedLabels.push(y);
      return '<text x="' + TEXT_X + '" y="' + (y + 3) + '" ' +
        'font-size="8" fill="' + color + '" font-family="\'SF Mono\',\'Fira Code\',monospace" ' +
        'opacity="' + (opacity || 0.9) + '">' + text + '</text>';
    }

    var bg = '#0d1117';
    var trunkColor = 'rgba(255,255,255,0.15)';
    var nowColor = '#ffffff';

    var parts = [];

    // Background rect
    parts.push('<rect width="' + svgW + '" height="' + svgH + '" fill="' + bg + '"/>');

    // Trunk
    parts.push('<line x1="' + TRUNK_X + '" y1="' + PAD_T + '" x2="' + TRUNK_X + '" y2="' + (svgH - PAD_B) + '" stroke="' + trunkColor + '" stroke-width="1.5"/>');

    // "NOW" — dot + label
    parts.push('<circle cx="' + TRUNK_X + '" cy="' + PAD_T + '" r="3" fill="' + nowColor + '"/>');
    parts.push('<text x="' + (TRUNK_X + 7) + '" y="' + (PAD_T + 3) + '" font-size="8" fill="' + nowColor + '" font-family="\'SF Mono\',\'Fira Code\',monospace" font-weight="bold" opacity="0.9">NOW</text>');

    // Draw branches
    projects.forEach(function (p) {
      var startY = dateToY(p._startDate);
      var endY   = p._isEnded ? dateToY(p._endDate) : PAD_T;
      var branchX = TRUNK_X + (p._lane + 1) * LANE_W;
      var c = p.color;

      var isStale = !p._isEnded && (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;
      var dash = p.status === 'abandoned' ? ' stroke-dasharray="3,2"'
               : isStale               ? ' stroke-dasharray="1.5,2"'
               : '';

      // Horizontal connector trunk → branch
      parts.push('<line x1="' + TRUNK_X + '" y1="' + startY + '" x2="' + branchX + '" y2="' + startY + '" stroke="' + c + '" stroke-width="1"/>');

      // Vertical branch
      parts.push('<line x1="' + branchX + '" y1="' + startY + '" x2="' + branchX + '" y2="' + endY + '" stroke="' + c + '" stroke-width="1"' + dash + '/>');

      // Start dot
      parts.push('<circle cx="' + branchX + '" cy="' + startY + '" r="2.5" fill="' + c + '"/>');

      // Start date label (deduplicated)
      parts.push(tryLabel(startY, shortDate(p.startDate), c, 0.85));

      if (p.status === 'finished') {
        parts.push('<line x1="' + branchX + '" y1="' + endY + '" x2="' + TRUNK_X + '" y2="' + endY + '" stroke="' + c + '" stroke-width="1"/>');
        parts.push('<circle cx="' + TRUNK_X + '" cy="' + endY + '" r="2.5" fill="' + c + '"/>');
        parts.push(tryLabel(endY, shortDate(p.lastEdited), c, 0.7));
      } else if (p.status === 'abandoned') {
        parts.push('<line x1="' + (branchX-3) + '" y1="' + (endY-3) + '" x2="' + (branchX+3) + '" y2="' + (endY+3) + '" stroke="' + c + '" stroke-width="1.5"/>');
        parts.push('<line x1="' + (branchX+3) + '" y1="' + (endY-3) + '" x2="' + (branchX-3) + '" y2="' + (endY+3) + '" stroke="' + c + '" stroke-width="1.5"/>');
      } else {
        parts.push('<circle cx="' + branchX + '" cy="' + PAD_T + '" r="2.5" fill="' + c + '"/>');
      }
    });

    var svg = '<svg width="' + svgW + '" height="' + svgH + '" xmlns="http://www.w3.org/2000/svg" style="display:block;border-radius:6px">' + parts.join('') + '</svg>';

    // Legend
    var legendParts = ['<div class="cadence-legend">'];
    projects.slice().reverse().forEach(function (p) {
      var tag = '';
      if (p.status === 'finished') tag = '<span style="color:#58a6ff;font-size:9px"> ✓</span>';
      else if (p.status === 'abandoned') tag = '<span style="color:#ff7b72;font-size:9px"> ✗</span>';
      else {
        var isStale = (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;
        if (isStale) tag = '<span style="color:#6e7681;font-size:9px"> stale</span>';
      }
      legendParts.push(
        '<span style="color:' + p.color + '">■</span> ' +
        '<a href="/' + p.folder + '">' + p.name + '</a>' + tag + '<br>'
      );
    });
    legendParts.push('</div>');

    mapContainer.innerHTML = svg + legendParts.join('');
  }

  var req = new XMLHttpRequest();
  req.open('GET', '/projects.json', true);
  req.onreadystatechange = function () {
    if (req.readyState === 4 && req.status === 200) {
      try { renderCadence(JSON.parse(req.responseText)); }
      catch (e) { console.error('cadence.js:', e); }
    }
  };
  req.send();
})();
