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
    if (links) links.textContent = /portland\.gov\/council\/agenda/.test(place.mayor.source) ? 'Source' : 'Mayor’s page';
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

    out.appendChild(el('p', 'muted', 'Showing results for ' + match.matchedAddress + '.'));
    if (window.CivicsORLocal && county) {
      // Remember only the county and city, so the Engage guides can show local links.
      window.CivicsORLocal.save({ county: county, city: localData && localData.cities[city] ? city : '' });
    }

    out.appendChild(city
      ? localCard('City', 'City of ' + city, LOCAL.places[city], 'Your mayor and council members are listed on the city’s website. We have not added a direct link for this city yet.', localData && localData.cities[city])
      : localCard('City', 'Outside city limits', null, 'This address is in an unincorporated area, so the county is your local government.'));

    if (county) {
      out.appendChild(localCard('County', county + ' County', LOCAL.counties[county], 'Your county commissioners are listed on the county’s website. Most Oregon counties have a board of three to five commissioners; a few smaller ones have a county court, a county judge and two commissioners.', localData && localData.counties[county]));
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
        out.appendChild(el('p', 'empty', 'We could not find that address. Check the spelling, include the city or ZIP code, and leave off apartment numbers.'));
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

  fetch('data/local.json').then(function (r) { return r.json(); }).then(function (d) { localData = d; }).catch(function () {});
  fetch('data/officials.json').then(function (r) { return r.json(); }).then(function (d) { officials = d; }).catch(function () {});
})();
