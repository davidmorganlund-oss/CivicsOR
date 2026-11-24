/* CivicsOR "Near you" box. Any element with class "near-you" becomes a
   county and city picker that shows that place's own pages. The choice is
   remembered in this browser only (localStorage), and the address lookup
   on reps.html fills it in too. Data: data/local.json. */
(function () {
  'use strict';

  var KEY = 'civicsor.place';
  var STATE_BOARDS = 'https://www.oregon.gov/gov/Pages/board-list.aspx';

  function base() {
    var s = document.querySelector('script[src$="local.js"]');
    return s ? s.getAttribute('src').replace(/local\.js$/, '') : '';
  }
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(place) {
    try { localStorage.setItem(KEY, JSON.stringify(place)); } catch (e) { /* private mode */ }
  }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function item(list, href, text, note) {
    var li = el('li');
    var a = el('a', null, text);
    a.href = href;
    a.rel = 'noopener';
    if (note) a.appendChild(el('span', null, note));
    li.appendChild(a);
    list.appendChild(li);
  }
  function option(select, value, text, selected) {
    var o = el('option', null, text);
    o.value = value;
    if (selected) o.selected = true;
    select.appendChild(o);
  }

  // Other local governments in the county (data/local.json "districts"), by kind.
  var DISTRICT_NOTES = {
    esd: 'Education service district: serves the school districts in this area. Board meetings and agendas.',
    port: 'Port district: elected commissioners. Meetings, agendas and how to comment.',
    library: 'Library: board meetings and agendas.',
    utility: 'People’s utility district: elected board sets rates. Meetings and agendas.',
    transit: 'Transit district: board meetings, agendas and service changes.',
    hospital: 'Health or hospital district: board meetings and agendas.',
    fire: 'Fire district: elected board. Meetings and agendas.',
    parks: 'Park and recreation district: elected board. Meetings and agendas.',
    other: 'Board meetings and agendas are on its website.'
  };

  function links(data, show, place) {
    var ul = el('ul', 'guide-links near-links');
    var county = data.counties[place.county];
    var city = place.city && data.cities[place.city];
    show.forEach(function (kind) {
      if (kind === 'boards') {
        if (city && city.boards) item(ul, city.boards, 'City of ' + place.city + ' boards and commissions', 'Openings, applications and what each board does.');
        else if (city && city.site) item(ul, city.site, 'City of ' + place.city, 'The city does not list its boards on one page we could link. Look under City Clerk, Mayor or Government, or ask the clerk about openings.');
        else if (city && city.bluebook) item(ul, city.bluebook, 'City of ' + place.city, 'This city has no website of its own. Ask city hall about openings; the Oregon Blue Book lists its address and phone.');
        if (county && county.boards) item(ul, county.boards, place.county + ' County boards and committees', 'County advisory boards and how to apply.');
        else if (county && (county.commissioners || county.site)) item(ul, county.commissioners || county.site, place.county + ' County commissioners',
          'This county does not list its boards on one page. The county commissioners make the appointments, so ask their office about openings.');
        item(ul, STATE_BOARDS, 'State boards, commissions and councils', 'The Governor’s list of state boards and commissions, with current openings and how to apply.');
      }
      if (kind === 'site') {
        if (city && city.site) item(ul, city.site, 'City of ' + place.city, 'Official website: mayor and council, departments and service requests.');
        else if (city && city.bluebook) item(ul, city.bluebook, 'City of ' + place.city, 'This city has no website of its own. The Oregon Blue Book lists its city hall address, phone and elected officials.');
        if (county && county.site) item(ul, county.site, place.county + ' County', 'Official website: commissioners, clerk, departments and services.');
      }
      if (kind === 'districts') {
        ((county && county.districts) || []).forEach(function (d) { item(ul, d.site, d.name, DISTRICT_NOTES[d.kind] || DISTRICT_NOTES.other); });
      }
      if (kind === 'schools') {
        var list = (county && county.schools) || [];
        list.forEach(function (s) { item(ul, s.site, s.name, 'District website: school board meetings, agendas and elections.'); });
        if (!list.length) item(ul, 'https://www.oregon.gov/ode/about-us/Pages/School-Directory.aspx', 'Oregon School Directory', 'Every district in Oregon, with contact information.');
      }
      if (kind === 'meetings') {
        if (place.county) item(ul, base() + 'index.html', 'Public meetings in ' + place.county + ' County', 'The CivicsOR calendar, set to your county.');
        if (city && (city.meetings || city.site)) item(ul, city.meetings || city.site, 'City of ' + place.city + ' meetings', 'Council agendas are on the city’s website.');
        else if (city && city.bluebook) item(ul, city.bluebook, 'City of ' + place.city + ' meetings', 'This city has no website. Council meetings are posted at city hall; the Oregon Blue Book lists its address and phone.');
        if (county && (county.meetings || county.site)) item(ul, county.meetings || county.site, place.county + ' County meetings', 'Commissioners’ agendas are on the county’s website.');
      }
    });
    return ul;
  }

  function build(box, data) {
    var show = (box.getAttribute('data-show') || 'boards').split(',');
    var place = load();
    if (!data.counties[place.county]) place = {};

    box.textContent = '';
    box.appendChild(el('h2', null, box.getAttribute('data-title') || 'Near you'));
    var form = el('div', 'near-pick');
    var cl = el('label', null, 'County');
    var cs = el('select');
    cs.id = 'near-county-' + Math.random().toString(36).slice(2, 7);
    cl.htmlFor = cs.id;
    option(cs, '', 'Choose your county', !place.county);
    Object.keys(data.counties).sort().forEach(function (c) { option(cs, c, c + ' County', c === place.county); });
    var tl = el('label', null, 'City or town');
    var ts = el('select');
    ts.id = cs.id.replace('county', 'city');
    tl.htmlFor = ts.id;
    [cl, cs, tl, ts].forEach(function (n) { form.appendChild(n); });
    box.appendChild(form);
    var out = el('div', 'near-out');
    box.appendChild(out);
    var help = el('p', 'muted');
    help.appendChild(document.createTextNode('Not sure which county or city you’re in? '));
    var a = el('a', null, 'Look up your address');
    a.href = base() + 'reps.html';
    help.appendChild(a);
    help.appendChild(document.createTextNode('. We remember your choice on this device only.'));
    box.appendChild(help);

    function fillCities() {
      ts.textContent = '';
      var names = Object.keys(data.cities).filter(function (n) { return data.cities[n].county === cs.value; }).sort();
      option(ts, '', cs.value ? 'Another town, or outside city limits' : 'Choose a county first', !place.city);
      names.forEach(function (n) { option(ts, n, n, n === place.city); });
      ts.disabled = !cs.value;
    }
    function draw() {
      out.textContent = '';
      if (!place.county) return;
      out.appendChild(links(data, show, place));
      if (!place.city && show.indexOf('boards') !== -1) {
        out.appendChild(el('p', 'muted', 'Most cities and towns post their boards on their own website, usually under City Hall or Government. If you live outside city limits, the county is your local government.'));
      }
    }
    cs.addEventListener('change', function () { place = { county: cs.value }; save(place); fillCities(); draw(); });
    ts.addEventListener('change', function () { place = { county: cs.value, city: ts.value }; save(place); draw(); });
    fillCities();
    draw();
  }

  window.CivicsORLocal = { save: save, load: load };
  var boxes = document.querySelectorAll('.near-you');
  if (!boxes.length) return;
  fetch(base() + 'data/local.json').then(function (r) { return r.json(); }).then(function (data) {
    Array.prototype.forEach.call(boxes, function (b) { build(b, data); });
  }).catch(function () {
    Array.prototype.forEach.call(boxes, function (b) { b.hidden = true; });
  });
})();
