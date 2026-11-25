/* CivicsOR "Who represents you" lookup.
   The address goes straight from the visitor's browser to the U.S. Census
   Bureau geocoder, which returns the districts it sits in. CivicsOR has no
   server, so it never receives or stores the address. Names come from
   data/officials.json, rebuilt nightly. */
(function () {
  'use strict';

  var GEOCODER = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress';
  var LEG_FINDER = 'https://geo.maps.arcgis.com/apps/instant/lookup/index.html?appid=fd070b56c975456ea2a25f7e3f4289d1';

  // Local governments with a council or commission page we have checked.
  var LOCAL = {
    places: {
      Portland: { label: 'Portland City Council agendas', url: 'https://www.portland.gov/council/agenda', note: 'Meetings, agendas and how to testify. Since 2025, each of Portland’s four districts elects three councilors' },
      Salem: { label: 'Salem City Council agendas', url: 'https://www.cityofsalem.net/government/city-council-mayor/city-council-meetings/city-council-meeting-agendas-and-minutes', note: 'Meetings, agendas and how to comment' }
    },
    counties: {
      Multnomah: { label: 'Multnomah County Board of Commissioners', url: 'https://multco.us/info/about-board-meetings', note: 'Meetings, agendas and how to testify' },
      Clackamas: { label: 'Clackamas County Board of County Commissioners', url: 'https://www.clackamas.us/meetings/bcc/business', note: 'Business meetings and agendas' },
      Washington: { label: 'Washington County Board of Commissioners', url: 'https://www.washingtoncountyor.gov/bcc', note: 'Members, meetings and agendas' }
    }
  };

  // New terms start after each November election. Update these after every
  // election: Congress on January 3; the Oregon Legislature on the second
  // Monday in January. The note shows from a few weeks before the first date
  // until a few weeks after the last, and turns itself off after that.
  var NEW_TERMS = [
    { date: '2027-01-03', who: 'New members of Congress' },
    { date: '2027-01-11', who: 'New members of the Oregon Legislature' }
  ];
  var TERM_NOTE_DAYS_BEFORE = 45;
  var TERM_NOTE_DAYS_AFTER = 30;

  function termNote(now) {
    var DAY = 86400000;
    var dates = NEW_TERMS.map(function (t) { var p = t.date.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); });
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    if (today < dates[0].getTime() - TERM_NOTE_DAYS_BEFORE * DAY ||
        today > dates[dates.length - 1].getTime() + TERM_NOTE_DAYS_AFTER * DAY) return '';
    var anyPast = false;
    var parts = NEW_TERMS.map(function (t, i) {
      var past = today >= dates[i];
      if (past) anyPast = true;
      var when = dates[i].toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
      return t.who + (past ? ' took office ' : ' take office ') + when + '.';
    });
    return parts.join(' ') + (anyPast
      ? ' The lists below can lag by a few weeks after a new term starts.'
      : ' Until then, the lists below show the members serving now.');
  }

  var officials = null;
  var localData = null;
  var $ = function (id) { return document.getElementById(id); };

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }
  function safeUrl(url) { return /^https?:\/\//i.test(url || '') ? url : ''; }
  function link(href, text) {
    var a = el('a', null, text);
    a.href = href;
    a.rel = 'noopener';
    return a;
  }

  function geocode(address) {
    return new Promise(function (resolve, reject) {
      var name = '__civicsor_geo_' + Date.now();
      var script = document.createElement('script');
      var timer = setTimeout(function () { finish(); reject(new Error('timeout')); }, 20000);
      function finish() { clearTimeout(timer); delete window[name]; script.remove(); }
      window[name] = function (data) { finish(); resolve(data); };
      script.onerror = function () { finish(); reject(new Error('network')); };
      script.src = GEOCODER + '?address=' + encodeURIComponent(address) +
        '&benchmark=Public_AR_Current&vintage=Current_Current&layers=all&format=jsonp&callback=' + name;
      document.head.appendChild(script);
    });
  }

  // Layer names carry a year or Congress number ("2026 State Legislative
  // Districts - Upper"), so match on the stable part of the name.
  function layer(geographies, pattern) {
    var key = Object.keys(geographies).filter(function (k) { return pattern.test(k); })[0];
    var rows = key ? geographies[key] : null;
    return rows && rows[0] ? rows[0].BASENAME : '';
  }

  function names(geographies, pattern) {
    var out = [];
    Object.keys(geographies).filter(function (k) { return pattern.test(k); }).forEach(function (k) {
      (geographies[k] || []).forEach(function (row) {
        if (row.NAME && out.indexOf(row.NAME) < 0) out.push(row.NAME);
      });
    });
    return out;
  }

  function districtItem(list, d) {
    var li = el('li', 'district');
    li.appendChild(el('strong', null, d.label + ': '));
    li.appendChild(document.createTextNode(d.name));
    if (d.note) li.appendChild(el('span', 'muted', d.note));
    list.appendChild(li);
  }

  // One card listing every district the address sits in. The districts the
  // Census lookup already named show right away; fire, education and
  // conservation districts come from three state map services, which get
  // only the map point.
  function districtsCard(g, match, parts) {
    var card = section('Your districts', 'Every district you live in');
    var list = el('ul', 'districts');
    card.appendChild(list);
    var add = function (d) { districtItem(list, d); };
    if (parts.cd) add({ label: 'U.S. House', name: 'Congressional District ' + parts.cd });
    if (parts.sd) add({ label: 'State Senate', name: 'Senate District ' + parts.sd });
    if (parts.hd) add({ label: 'State House', name: 'House District ' + parts.hd });
    if (parts.county) add({ label: 'County', name: parts.county + ' County' });
    add({ label: 'City', name: parts.city ? 'City of ' + parts.city : 'Unincorporated (outside city limits)' });
    names(g, /School Districts/).forEach(function (n) {
      add({ label: 'School district', name: n, note: 'An elected school board runs your public schools.' });
    });
    names(g, /American Indian Reservations|Off-Reservation Trust Lands/).forEach(function (n) {
      add({ label: 'Tribal land', name: n, note: 'This address is on tribal land. The tribe’s own government serves its members here.' });
    });

    var status = el('p', 'muted', 'Looking up fire, education and conservation districts…');
    card.appendChild(status);
    var D = window.CivicsORDistricts;
    var c = match.coordinates || {};
    if (!D || typeof c.x !== 'number' || typeof c.y !== 'number') {
      status.textContent = 'We could not look up special districts for this address.';
      return card;
    }
    var local = parts.local || Promise.resolve({});
    Promise.all([D.lookup(c.x, c.y), local]).then(function (both) {
      var r = both[0], here = both[1];
      if (here.council) add({ label: 'City council', name: 'Portland City Council District ' + here.council });
      if (here.commission) add({ label: 'County commission', name: 'Multnomah County Commissioner District ' + here.commission });
      [r.fire, r.education, r.swcd].forEach(function (found) { (found || []).forEach(add); });
      status.textContent = (!r.fire || !r.education || !r.swcd || here.council === null || here.commission === null)
        ? 'Part of the district lookup did not respond, so this list may be missing some districts. Try again in a few minutes.'
        : 'Fire districts come from the Oregon State Fire Marshal’s maps, education districts from the state’s education boundary maps, and conservation districts from the Oregon Department of Agriculture.' +
          (here.council ? ' Portland council districts come from the City of Portland’s district map.' : '') +
          (here.commission ? ' Multnomah County commissioner districts come from the county’s elections map.' : '');
      var missing = [];
      if (!here.commission) missing.push('county commissioner districts');
      if (!here.council) missing.push('city council districts');
      card.appendChild(el('p', 'muted', 'Not listed here: ' + missing.concat(['voting precincts']).join(', ') +
        (missing.length ? ',' : '') + ' and library, park, water, sanitary, transit, port and Metro districts. Your county elections office can tell you which of those you live in.'));
    });
    return card;
  }

  // Portland's council district and Multnomah County's commissioner district,
  // with the members the City's and the County's own pages list for each.
  // roster: { source: url, "1": [people], ..., chair: person } from data/local.json.
  function localDistrict(card, promise, key, opts) {
    var slot = el('div');
    card.appendChild(slot);
    promise.then(function (here) {
      var num = here[key];
      if (num === undefined || num === '') return;  // not asked, or outside the map
      if (num === null) {
        slot.appendChild(el('p', 'muted', 'We could not look up your ' + opts.what + ' right now. Try again in a few minutes.'));
        return;
      }
      var roster = opts.roster || {};
      slot.appendChild(el('h4', null, opts.heading + ' ' + num));
      people(slot, roster[num], 'See the ' + opts.who + ' page for the members of this district.');
      if (roster.chair) {
        slot.appendChild(el('h4', null, opts.chairHeading));
        people(slot, [roster.chair], '');
      }
      if (safeUrl(roster.source)) {
        var p = el('p', 'muted');
        p.appendChild(document.createTextNode((opts.note ? opts.note + ' ' : '') + 'Members as listed by the '));
        p.appendChild(link(roster.source, opts.who));
        p.appendChild(document.createTextNode('.'));
        slot.appendChild(p);
      }
    });
  }

  function person(p) {
    var li = el('li', 'person');
    li.appendChild(el('strong', null, p.name));
    if (p.seat) li.appendChild(el('span', 'muted', ' · Seat ' + p.seat));
    if (p.party) li.appendChild(el('span', 'muted', ' · ' + p.party));
    var contact = el('div', 'contact');
    if (p.phone) contact.appendChild(link('tel:' + p.phone.replace(/[^\d+]/g, ''), p.phone));
    if (p.email) contact.appendChild(link('mailto:' + p.email, p.email));
    if (safeUrl(p.url)) contact.appendChild(link(p.url, 'Website'));
    if (contact.children.length) li.appendChild(contact);
    return li;
  }

  function section(title, subtitle) {
    var card = el('section', 'card');
    card.appendChild(el('span', 'eyebrow', title));
    if (subtitle) card.appendChild(el('h3', null, subtitle));
    return card;
  }

  function people(card, list, emptyText) {
    if (list && list.length) {
      var ul = el('ul', 'people');
      list.forEach(function (p) { ul.appendChild(person(p)); });
      card.appendChild(ul);
    } else {
      card.appendChild(el('p', 'muted', emptyText));
    }
  }

  // Official website and boards page for counties and the larger cities,
  // from data/local.json (the same list the Engage guides' "Near you" boxes use).
  function extraLinks(card, place) {
    if (!place) return;
    var p = el('p');
    if (safeUrl(place.site)) p.appendChild(link(place.site, 'Official website'));
    var second = place.boards ? [place.boards, 'Boards and committees']
      : place.commissioners ? [place.commissioners, 'Commissioners (they appoint board members)']
      : place.meetings ? [place.meetings, 'Meetings and agendas'] : null;
    if (second && safeUrl(second[0])) {
      if (p.childNodes.length) p.appendChild(document.createTextNode(' · '));
      p.appendChild(link(second[0], second[1]));
    }
    if (p.childNodes.length) card.appendChild(p);
  }

  // Mayors confirmed on each city's own website (data/local.json), with a
  // link to the council members page where we found one.
  function addMayor(card, place) {
    if (!place || !place.mayor) return;
    card.appendChild(el('h4', null, 'Mayor'));
    people(card, [{ name: place.mayor.name, url: place.mayor.source }], '');
    var links = card.querySelector('ul.people:last-of-type .contact a');
    // Other people's rows say "Website". Where the page we confirmed the mayor
    // on is the council's agenda page, not the mayor's own, say so.
    if (links && /\/council\/agenda/.test(place.mayor.source)) links.textContent = 'City Council agendas';
    if (place.mayor.note) card.appendChild(el('p', 'muted', place.mayor.note));
    if (safeUrl(place.council)) {
      var p = el('p');
      p.appendChild(link(place.council, 'City council members'));
      card.appendChild(p);
    }
  }

  function localCard(title, name, entry, fallback, place) {
    var card = section(title, name);
    if (title === 'City') addMayor(card, place);
    if (!entry && place) { extraLinks(card, place); return card; }
    if (entry) {
      var p = el('p');
      p.appendChild(link(entry.url, entry.label));
      p.appendChild(document.createTextNode(': ' + entry.note + '.'));
      card.appendChild(p);
    } else {
      card.appendChild(el('p', 'muted', fallback));
    }
    extraLinks(card, place);
    return card;
  }

  function render(match) {
    var g = match.geographies;
    var out = $('results');
    out.textContent = '';

    var state = layer(g, /^States$/);
    if (state && state !== 'Oregon') {
      out.appendChild(el('p', 'empty', 'That address is in ' + state + '. CivicsOR only covers Oregon.'));
      return;
    }

    var city = layer(g, /Incorporated Places/);
    var county = layer(g, /^Counties$/);
    var sd = layer(g, /State Legislative Districts - Upper/);
    var hd = layer(g, /State Legislative Districts - Lower/);
    var cd = layer(g, /Congressional Districts/);

    // Portland and Multnomah County only: council and commissioner districts
    // from the City's and the County's own maps (see districts.js).
    var D = window.CivicsORDistricts;
    var c = match.coordinates || {};
    var local = (D && D.localDistricts && typeof c.x === 'number' && typeof c.y === 'number' &&
      (city === 'Portland' || county === 'Multnomah')) ? D.localDistricts(c.x, c.y, { city: city, county: county }) : null;

    out.appendChild(el('p', 'muted', 'Showing results for ' + match.matchedAddress + '.'));
    out.appendChild(districtsCard(g, match, { city: city, county: county, sd: sd, hd: hd, cd: cd, local: local }));
    if (window.CivicsORLocal && county) {
      // Remember only the county and city, so the Engage guides can show local links.
      window.CivicsORLocal.save({ county: county, city: localData && localData.cities[city] ? city : '' });
    }

    var cityPlace = localData && localData.cities[city];
    var cityCard = city
      ? localCard('City', 'City of ' + city, LOCAL.places[city], 'Your mayor and council members are listed on the city’s website. We have not added a direct link for this city yet.', cityPlace)
      : localCard('City', 'Outside city limits', null, 'This address is in an unincorporated area, so the county is your local government.');
    if (local && city === 'Portland') {
      localDistrict(cityCard, local, 'council', { heading: 'City Council, District', what: 'Portland City Council district',
        who: 'City of Portland', roster: cityPlace && cityPlace.council_districts });
    }
    out.appendChild(cityCard);

    if (county) {
      var countyPlace = localData && localData.counties[county];
      var countyCard = localCard('County', county + ' County', LOCAL.counties[county], 'Your county commissioners are listed on the county’s website. Most Oregon counties have a board of three to five commissioners; a few smaller ones have a county court, a county judge and two commissioners.', countyPlace);
      if (local && county === 'Multnomah') {
        localDistrict(countyCard, local, 'commission', { heading: 'County Commissioner, District', what: 'county commissioner district',
          who: 'Multnomah County Board of Commissioners', roster: countyPlace && countyPlace.commissioner_districts,
          chairHeading: 'County Chair (elected countywide)', note: 'Four commissioners are elected by district and the chair countywide.' });
      }
      out.appendChild(countyCard);
    }

    var leg = officials && officials.legislators;
    var senators = leg && leg.senate ? leg.senate[sd] : null;
    var reps = leg && leg.house ? leg.house[hd] : null;
    var legCard = section('State Legislature', sd || hd ? 'Senate District ' + (sd || '?') + ' · House District ' + (hd || '?') : 'Legislative districts not found');
    if (leg) {
      legCard.appendChild(el('h4', null, 'State Senator'));
      people(legCard, senators, 'No senator listed.');
      legCard.appendChild(el('h4', null, 'State Representative'));
      people(legCard, reps, 'No representative listed.');
    } else {
      legCard.appendChild(el('p', 'muted', 'We could not load the member list.'));
    }
    var confirm = el('p', 'muted');
    confirm.appendChild(document.createTextNode('Each Senate district is two House districts put together, so you have one state senator and one state representative. Members elected in November take office in January, and this list can lag by a few weeks. Confirm current members with the Legislature’s '));
    confirm.appendChild(link(LEG_FINDER, 'Find Your Legislator'));
    confirm.appendChild(document.createTextNode(' page.'));
    legCard.appendChild(confirm);
    out.appendChild(legCard);

    var congress = (officials && officials.congress) || { senators: [], house: {} };
    var fed = section('Congress', cd ? 'Congressional District ' + cd : 'Congressional district not found');
    fed.appendChild(el('h4', null, 'U.S. Representative'));
    people(fed, congress.house[cd] ? [congress.house[cd]] : [], 'No representative listed.');
    fed.appendChild(el('h4', null, 'U.S. Senators'));
    people(fed, congress.senators, 'No senators listed.');
    out.appendChild(fed);
  }

  $('lookup').addEventListener('submit', function (ev) {
    ev.preventDefault();
    var address = $('address').value.trim();
    var out = $('results');
    out.textContent = '';
    if (address.length < 6) {
      out.appendChild(el('p', 'empty', 'Enter a street address with a city or ZIP code, like 900 Court St NE, Salem.'));
      return;
    }
    out.appendChild(el('p', 'empty', 'Looking up your districts…'));
    geocode(/oregon|,\s*or\b|\bor\s+9\d{4}/i.test(address) ? address : address + ', OR').then(function (data) {
      var matches = data && data.result && data.result.addressMatches;
      if (!matches || !matches.length) {
        out.textContent = '';
        out.appendChild(el('p', 'empty', 'We could not find that address. Check the street number, spelling and ZIP code, and leave off apartment numbers. If it still isn’t found, try a nearby street address. Some government buildings aren’t in the Census Bureau’s address list.'));
        return;
      }
      render(matches[0]);
    }).catch(function () {
      out.textContent = '';
      var p = el('p', 'empty');
      p.appendChild(document.createTextNode('The address lookup is not responding right now. You can use the Legislature’s '));
      p.appendChild(link(LEG_FINDER, 'Find Your Legislator'));
      p.appendChild(document.createTextNode(' page instead.'));
      out.appendChild(p);
    });
  });

  var note = $('term-note');
  var noteText = note ? termNote(new Date()) : '';
  if (noteText) { note.textContent = noteText; note.hidden = false; }

  fetch('data/local.json').then(function (r) { return r.json(); }).then(function (d) { localData = d; }).catch(function () {});
  fetch('data/officials.json').then(function (r) { return r.json(); }).then(function (d) { officials = d; }).catch(function () {});
})();
