(function () {
  'use strict';

  var COLORS = [
    '#2563eb','#16a34a','#d97706','#7c3aed','#dc2626',
    '#0891b2','#ea580c','#0d9488','#9333ea','#e11d48',
    '#2980b9','#27ae60','#c0392b','#8e44ad','#16a085',
    '#f59e0b','#6366f1','#10b981','#ef4444','#3b82f6'
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

  function dayDate(str) {
    if (!str) return '';
    var parts = str.split('/');
    if (parts.length !== 3) return '';
    var d = parseInt(parts[0], 10);
    var m = parseInt(parts[1], 10) - 1;
    return d + ' ' + MONTHS[m];
  }

  function renderStats(projects, container, workDates) {
    var TODAY = new Date();

    if (projects.length === 1) {
      var p = projects[0];
      var ended = p.status === 'finished' || p.status === 'abandoned';
      var days = ended
        ? Math.round((parseDate(p.lastEdited) - parseDate(p.startDate)) / 86400000)
        : Math.round((TODAY - parseDate(p.startDate)) / 86400000);
      var statusColor = p.status === 'finished' ? '#2563eb' : p.status === 'abandoned' ? '#dc2626' : '#16a34a';
      var statusLabel = p.status === 'finished' ? '✓ finished' : p.status === 'abandoned' ? '✗ abandoned' : '● active';
      var daysLabel = ended ? 'd to complete' : 'd since start';
      var cadenceLine = '';
      if (workDates && workDates.length >= 2) {
        var sorted = workDates.slice().sort(function(a, b) { return parseDate(a) - parseDate(b); });
        var gaps = [];
        for (var i = 1; i < sorted.length; i++) {
          gaps.push(Math.round((parseDate(sorted[i]) - parseDate(sorted[i-1])) / 86400000));
        }
        var avgGap = Math.round(gaps.reduce(function(a,b){return a+b;},0) / gaps.length);
        cadenceLine = '<br>updated every ~<span class="cs-val">' + avgGap + 'd</span>';
      } else if (workDates && workDates.length === 1) {
        cadenceLine = '<br><span class="cs-val">' + workDates.length + '</span> session logged';
      }
      container.innerHTML =
        '<span style="color:' + statusColor + '">' + statusLabel + '</span>&nbsp; ' +
        'started <span class="cs-val">' + shortDate(p.startDate) + '</span><br>' +
        '<span class="cs-val">' + days + '</span>' + daysLabel + cadenceLine;
      return;
    }

    var ongoing = 0, finished = 0, abandoned = 0, finishedDays = [];
    projects.forEach(function (p) {
      if (p.status === 'finished') {
        finished++;
        var d = Math.round((parseDate(p.lastEdited) - parseDate(p.startDate)) / 86400000);
        if (d > 0) finishedDays.push(d);
      } else if (p.status === 'abandoned') {
        abandoned++;
      } else {
        ongoing++;
      }
    });

    var line2 = '';
    if (finishedDays.length > 0) {
      var avg = Math.round(finishedDays.reduce(function(a,b){return a+b;},0) / finishedDays.length);
      line2 = 'avg <span class="cs-val">' + avg + 'd</span> to finish';
    } else {
      var ages = projects.filter(function(p){return p.status==='ongoing';})
        .map(function(p){return Math.round((TODAY - parseDate(p.startDate))/86400000);});
      if (ages.length) {
        var avgAge = Math.round(ages.reduce(function(a,b){return a+b;},0)/ages.length);
        line2 = 'avg age <span class="cs-val">' + avgAge + 'd</span>';
      }
    }

    container.innerHTML =
      '<span style="color:#16a34a">●</span> <span class="cs-val">' + ongoing + '</span> active&nbsp; ' +
      '<span style="color:#2563eb">✓</span> <span class="cs-val">' + finished + '</span> done&nbsp; ' +
      '<span style="color:#dc2626">✗</span> <span class="cs-val">' + abandoned + '</span> dropped' +
      (line2 ? '<br>' + line2 : '');
  }

  function getPageWorkDates() {
    var dates = [];
    var headings = document.querySelectorAll('section h2');
    for (var i = 0; i < headings.length; i++) {
      var text = headings[i].textContent.trim();
      if (/^\d{2}\/\d{2}\/(\d{2}|\d{4})$/.test(text)) dates.push(text);
    }
    return dates;
  }

  function renderCadence(projects, workDates) {
    var mapEl   = document.getElementById('cadence-map');
    var statsEl = document.getElementById('cadence-stats');
    if (!mapEl) return;

    var TODAY = new Date();
    var STALE_DAYS = 45;

    var isSingle = projects.length === 1;

    projects.sort(function(a,b){ return parseDate(a.startDate) - parseDate(b.startDate); });
    if (statsEl) renderStats(projects, statsEl, workDates);

    // Lane assignment
    var laneEnds = [];
    projects.forEach(function(p, i) {
      p.color = COLORS[i % COLORS.length];
      var s = parseDate(p.startDate);
      var ended = p.status === 'finished' || p.status === 'abandoned';
      var e = ended ? parseDate(p.lastEdited) : TODAY;
      p._s = s; p._e = e; p._ended = ended;
      // For the top-anchor: ended projects use their end date, active use TODAY
      p._top = ended ? e : TODAY;
      var lane = -1;
      for (var l = 0; l < laneEnds.length; l++) {
        if (laneEnds[l] <= s) { lane = l; laneEnds[l] = e; break; }
      }
      if (lane === -1) { lane = laneEnds.length; laneEnds.push(e); }
      p._lane = lane;
    });

    // Layout constants — larger scale on single-project pages
    var TRUNK_X    = 14;
    var LANE_W     = isSingle ? 22  : 14;
    var R          = isSingle ? 7   : 5;
    var DOT_R      = isSingle ? 6   : 4.5;
    var MERGE_R    = isSingle ? 4.5 : 3.5;
    var NOW_R      = isSingle ? 7   : 5.5;
    var LABEL_PAD  = 9;
    var LABEL_W    = 55;
    var PAD_T      = 52;
    var PAD_B      = 14;
    var PX_PER_DAY = isSingle ? 2.2 : 0.52;
    var MIN_GAP    = isSingle ? 16  : 13;

    var numLanes = laneEnds.length;
    var TEXT_X   = TRUNK_X + (numLanes + 1) * LANE_W + LABEL_PAD;

    var allStarts = projects.map(function(p){ return p._s; });
    var minDate   = new Date(Math.min.apply(null, allStarts));
    // Top of graph: latest active project's "now", or latest end date if all ended
    var TOP_DATE  = new Date(Math.max.apply(null, projects.map(function(p){ return p._top; })));
    var totalDays = (TOP_DATE - minDate) / 86400000;
    var svgH = Math.round(PAD_T + totalDays * PX_PER_DAY + PAD_B);
    var svgW = TEXT_X + LABEL_W;

    function toY(date) {
      return Math.round(PAD_T + (TOP_DATE - date) / 86400000 * PX_PER_DAY);
    }

    var parts = [];
    var placedY = [];

    function tryLabel(y, text, color) {
      for (var i = 0; i < placedY.length; i++) {
        if (Math.abs(placedY[i] - y) < MIN_GAP) return '';
      }
      placedY.push(y);
      return '<text x="' + TEXT_X + '" y="' + (y + 4) + '" ' +
        'font-size="10.5" fill="' + color + '" ' +
        'font-family="\'Helvetica Neue\',Helvetica,Arial,sans-serif" ' +
        'opacity="0.85">' + text + '</text>';
    }

    var TRUNK_COL = '#d0d7de';
    var NOW_COL   = '#267CB9';

    // Trunk line
    parts.push('<line x1="' + TRUNK_X + '" y1="' + PAD_T + '" x2="' + TRUNK_X + '" y2="' + (svgH - PAD_B) + '" stroke="' + TRUNK_COL + '" stroke-width="2"/>');

    // "Now" / "Finished" dot + label — sits at top of graph
    var allEnded = projects.every(function(p) { return p._ended; });
    var topLabel = allEnded ? shortDate(projects[projects.length - 1].lastEdited) : 'Now';
    var nowLineW = TRUNK_X + (numLanes + 1) * LANE_W;
    if (!allEnded) {
      parts.push('<line x1="' + TRUNK_X + '" y1="' + PAD_T + '" x2="' + nowLineW + '" y2="' + PAD_T + '" stroke="' + NOW_COL + '" stroke-width="1" stroke-dasharray="3,3" opacity="0.5"/>');
      parts.push('<circle cx="' + TRUNK_X + '" cy="' + PAD_T + '" r="' + NOW_R + '" fill="' + NOW_COL + '"/>');
      parts.push('<text x="' + (nowLineW + 6) + '" y="' + (PAD_T + 4) + '" font-size="11" fill="' + NOW_COL + '" font-family="\'Helvetica Neue\',Helvetica,Arial,sans-serif" font-weight="600">' + topLabel + '</text>');
    }

    projects.forEach(function(p) {
      var sY  = toY(p._s);
      var eY  = p._ended ? toY(p._e) : PAD_T;
      var bX  = TRUNK_X + (p._lane + 1) * LANE_W;
      var c   = p.color;

      var isStale = !p._ended && (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;
      var dash = p.status === 'abandoned' ? ' stroke-dasharray="5,3"'
               : isStale                  ? ' stroke-dasharray="3,3"'
               : '';

      // Build SVG path with rounded corners
      var zeroDuration = p.status === 'finished' && Math.abs(sY - eY) < 2;
      var d;
      if (p.status === 'finished') {
        if (zeroDuration) {
          // Same-day project — just a dot on the trunk, no branch
          parts.push('<circle cx="' + TRUNK_X + '" cy="' + sY + '" r="' + MERGE_R + '" fill="' + c + '" stroke="white" stroke-width="1.5"/>');
          parts.push(tryLabel(sY, shortDate(p.lastEdited), c));
        } else {
          // Branch out, up, then merge back to trunk
          d = 'M ' + TRUNK_X + ',' + sY +
              ' H ' + (bX - R) +
              ' Q ' + bX + ',' + sY + ' ' + bX + ',' + (sY - R) +
              ' V ' + (eY + R) +
              ' Q ' + bX + ',' + eY + ' ' + (bX - R) + ',' + eY +
              ' H ' + TRUNK_X;
          parts.push('<path d="' + d + '" fill="none" stroke="' + c + '" stroke-width="2"/>');
          // Merge dot on trunk
          parts.push('<circle cx="' + TRUNK_X + '" cy="' + eY + '" r="' + MERGE_R + '" fill="' + c + '" stroke="white" stroke-width="1.5"/>');
          // End date label
          parts.push(tryLabel(eY, shortDate(p.lastEdited), c));
        }
      } else {
        // Branch out then up to Now (or just open end)
        d = 'M ' + TRUNK_X + ',' + sY +
            ' H ' + (bX - R) +
            ' Q ' + bX + ',' + sY + ' ' + bX + ',' + (sY - R) +
            ' V ' + eY;
        parts.push('<path d="' + d + '" fill="none" stroke="' + c + '" stroke-width="2"' + dash + '/>');
        if (!p._ended) {
          // Lines just terminate at the Now guide — no dot (avoids the cluster)
        } else {
          // Abandoned: X marker
          parts.push('<line x1="' + (bX-4) + '" y1="' + (eY-4) + '" x2="' + (bX+4) + '" y2="' + (eY+4) + '" stroke="' + c + '" stroke-width="2"/>');
          parts.push('<line x1="' + (bX+4) + '" y1="' + (eY-4) + '" x2="' + (bX-4) + '" y2="' + (eY+4) + '" stroke="' + c + '" stroke-width="2"/>');
        }
      }

      // Work date ticks (project page only)
      if (workDates) {
        workDates.forEach(function(dateStr) {
          var wd = parseDate(dateStr);
          var wY = toY(wd);
          if (wY <= sY && wY >= eY) {
            var tk = 7;
            parts.push('<line x1="' + (bX - tk) + '" y1="' + wY + '" x2="' + (bX + tk) + '" y2="' + wY +
              '" stroke="white" stroke-width="3.5"/>');
            parts.push('<line x1="' + (bX - tk) + '" y1="' + wY + '" x2="' + (bX + tk) + '" y2="' + wY +
              '" stroke="' + c + '" stroke-width="2.5" opacity="0.95"/>');
            parts.push(tryLabel(wY, dayDate(dateStr), c));
          }
        });
      }

      // Branch start dot (skip for same-day projects — trunk dot was already drawn)
      if (!zeroDuration) {
        parts.push('<circle cx="' + bX + '" cy="' + sY + '" r="' + DOT_R + '" fill="' + c + '" stroke="white" stroke-width="2"/>');
        parts.push(tryLabel(sY, shortDate(p.startDate), c));
      }
    });

    var svg = '<svg width="' + svgW + '" height="' + svgH + '" xmlns="http://www.w3.org/2000/svg" style="display:block">' +
              parts.join('') + '</svg>';

    // Legend — newest first, root-relative links
    var leg = ['<div class="cadence-legend">'];
    projects.slice().reverse().forEach(function(p) {
      var tag = '';
      if (p.status === 'finished')  tag = '<span style="color:#aaa;font-size:10px"> ✓</span>';
      else if (p.status === 'abandoned') tag = '<span style="color:#aaa;font-size:10px"> ✗</span>';
      else {
        var isStale = (TODAY - parseDate(p.lastEdited)) > STALE_DAYS * 86400000;
        if (isStale) tag = '<span style="color:#bbb;font-size:10px"> stale</span>';
      }
      leg.push('<span style="color:' + p.color + ';font-size:11px">●</span> ' +
               '<a href="/' + p.folder + '">' + p.name + '</a>' + tag + '<br>');
    });
    leg.push('</div>');

    mapEl.innerHTML = svg + leg.join('');
  }

  var req = new XMLHttpRequest();
  req.open('GET', '/projects.json', true);
  req.onreadystatechange = function() {
    if (req.readyState === 4 && req.status === 200) {
      try {
        var projects = JSON.parse(req.responseText);
        var folder = window.location.pathname.replace(/^\/|\/$/g, '');
        var match = projects.filter(function(p) { return p.folder === folder; });
        var workDates = match.length === 1 ? getPageWorkDates() : null;
        renderCadence(match.length === 1 ? match : projects, workDates);
      }
      catch(e) { console.error('cadence.js:', e); }
    }
  };
  req.send();
})();
