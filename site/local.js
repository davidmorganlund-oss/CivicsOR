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

  // English and Spanish wording. Pages under /es/ set <html lang="es">. Place
  // names come from the data and stay as they are; the linked sites are in English.
  var LANG = document.documentElement.lang === 'es' ? 'es' : 'en';
  var S = {
    en: {
      cityOf: function (c) { return 'City of ' + c; }, countyOf: function (c) { return c + ' County'; },
      cityBoards: function (c) { return 'City of ' + c + ' boards and commissions'; }, cityBoardsNote: 'Openings, applications and what each board does.',
      noBoardsPage: 'The city does not list its boards on one page we could link. Look under City Clerk, Mayor or Government, or ask the clerk about openings.',
      noSiteBoards: 'This city has no website of its own. Ask city hall about openings; the Oregon Blue Book lists its address and phone.',
      countyBoards: function (c) { return c + ' County boards and committees'; }, countyBoardsNote: 'County advisory boards and how to apply.',
      countyCommissioners: function (c) { return c + ' County commissioners'; },
      noCountyBoards: 'This county does not list its boards on one page. The county commissioners make the appointments, so ask their office about openings.',
      stateBoards: 'State boards, commissions and councils', stateBoardsNote: 'The Governor’s list of state boards and commissions, with current openings and how to apply.',
      citySite: 'Official website: mayor and council, departments and service requests.',
      noSiteCity: 'This city has no website of its own. The Oregon Blue Book lists its city hall address, phone and elected officials.',
      countySite: 'Official website: commissioners, clerk, departments and services.',
      schoolNote: 'District website: school board meetings, agendas and elections.',
      schoolDir: 'Oregon School Directory', schoolDirNote: 'Every district in Oregon, with contact information.',
      meetingsIn: function (c) { return 'Public meetings in ' + c + ' County'; }, calNote: 'The CivicsOR calendar, set to your county.',
      cityMeetings: function (c) { return 'City of ' + c + ' meetings'; }, cityMeetingsNote: 'Council agendas are on the city’s website.',
      noSiteMeetings: 'This city has no website. Council meetings are posted at city hall; the Oregon Blue Book lists its address and phone.',
      countyMeetings: function (c) { return c + ' County meetings'; }, countyMeetingsNote: 'Commissioners’ agendas are on the county’s website.',
      nearYou: 'Near you', county: 'County', chooseCounty: 'Choose your county', cityTown: 'City or town',
      notSure: 'Not sure which county or city you’re in? ', lookUp: 'Look up your address', remember: '. We remember your choice on this device only.',
      another: 'Another town, or outside city limits', countyFirst: 'Choose a county first',
      mostCities: 'Most cities and towns post their boards on their own website, usually under City Hall or Government. If you live outside city limits, the county is your local government.',
      calPage: './', repsPage: 'reps.html',
      districtNotes: {
        esd: 'Education service district: serves the school districts in this area. Board meetings and agendas.',
        port: 'Port district: elected commissioners. Meetings, agendas and how to comment.',
        library: 'Library: board meetings and agendas.',
        utility: 'People’s utility district: elected board sets rates. Meetings and agendas.',
        transit: 'Transit district: board meetings, agendas and service changes.',
        hospital: 'Health or hospital district: board meetings and agendas.',
        fire: 'Fire district: elected board. Meetings and agendas.',
        parks: 'Park and recreation district: elected board. Meetings and agendas.',
        other: 'Board meetings and agendas are on its website.'
      }
    },
    es: {
      cityOf: function (c) { return 'Ciudad de ' + c; }, countyOf: function (c) { return 'Condado de ' + c; },
      cityBoards: function (c) { return 'Juntas y comisiones de la Ciudad de ' + c + ' (en inglés)'; }, cityBoardsNote: 'Puestos vacantes, solicitudes y qué hace cada junta.',
      noBoardsPage: 'La ciudad no tiene sus juntas en una sola página que podamos enlazar. Busque en City Clerk, Mayor o Government, o pregunte al secretario municipal (city clerk) por los puestos vacantes.',
      noSiteBoards: 'Esta ciudad no tiene sitio web propio. Pregunte en la alcaldía (city hall) por los puestos vacantes; el Oregon Blue Book tiene su dirección y teléfono.',
      countyBoards: function (c) { return 'Juntas y comités del condado de ' + c + ' (en inglés)'; }, countyBoardsNote: 'Juntas asesoras del condado y cómo presentar una solicitud.',
      countyCommissioners: function (c) { return 'Comisionados del condado de ' + c + ' (en inglés)'; },
      noCountyBoards: 'Este condado no tiene sus juntas en una sola página. Los comisionados del condado hacen los nombramientos, así que pregunte en su oficina por los puestos vacantes.',
      stateBoards: 'Juntas, comisiones y consejos del estado (en inglés)', stateBoardsNote: 'La lista de la Gobernación con las juntas y comisiones estatales, los puestos vacantes y cómo presentar una solicitud.',
      citySite: 'Sitio web oficial (en inglés): alcaldía y concejo, departamentos y solicitudes de servicio.',
      noSiteCity: 'Esta ciudad no tiene sitio web propio. El Oregon Blue Book tiene la dirección, el teléfono y los funcionarios electos de su alcaldía.',
      countySite: 'Sitio web oficial (en inglés): comisionados, secretaría del condado, departamentos y servicios.',
      schoolNote: 'Sitio web del distrito (en inglés): reuniones, agendas y elecciones de la junta escolar.',
      schoolDir: 'Directorio de escuelas de Oregon (en inglés)', schoolDirNote: 'Todos los distritos de Oregon, con sus datos de contacto.',
      meetingsIn: function (c) { return 'Reuniones públicas en el condado de ' + c; }, calNote: 'El calendario de CivicsOR, con su condado ya elegido.',
      cityMeetings: function (c) { return 'Reuniones de la Ciudad de ' + c + ' (en inglés)'; }, cityMeetingsNote: 'Las agendas del concejo están en el sitio web de la ciudad.',
      noSiteMeetings: 'Esta ciudad no tiene sitio web. Las reuniones del concejo se anuncian en la alcaldía (city hall); el Oregon Blue Book tiene su dirección y teléfono.',
      countyMeetings: function (c) { return 'Reuniones del condado de ' + c + ' (en inglés)'; }, countyMeetingsNote: 'Las agendas de los comisionados están en el sitio web del condado.',
      nearYou: 'Cerca de usted', county: 'Condado', chooseCounty: 'Elija su condado', cityTown: 'Ciudad o pueblo',
      notSure: '¿No sabe en qué condado o ciudad está? ', lookUp: 'Busque su dirección', remember: '. Recordamos su elección solo en este dispositivo.',
      another: 'Otro pueblo, o fuera de los límites de la ciudad', countyFirst: 'Primero elija un condado',
      mostCities: 'La mayoría de las ciudades y pueblos publican sus juntas en su propio sitio web, casi siempre en City Hall o Government. Si vive fuera de los límites de la ciudad, el condado es su gobierno local.',
      calPage: 'es/', repsPage: 'es/reps.html',
      districtNotes: {
        esd: 'Distrito de servicios educativos: atiende a los distritos escolares de esta zona. Reuniones y agendas de la junta.',
        port: 'Distrito portuario: comisionados electos. Reuniones, agendas y cómo enviar comentarios.',
        library: 'Biblioteca: reuniones y agendas de la junta.',
        utility: 'Distrito de servicios públicos (people’s utility district): una junta electa fija las tarifas. Reuniones y agendas.',
        transit: 'Distrito de transporte público: reuniones de la junta, agendas y cambios en el servicio.',
        hospital: 'Distrito de salud u hospital: reuniones y agendas de la junta.',
        fire: 'Distrito de bomberos: junta electa. Reuniones y agendas.',
        parks: 'Distrito de parques y recreación: junta electa. Reuniones y agendas.',
        other: 'Las reuniones y agendas de la junta están en su sitio web (en inglés).'
      }
    }
  }[LANG];

  // Other local governments in the county (data/local.json "districts"), by kind.
  var DISTRICT_NOTES = S.districtNotes;

  function links(data, show, place) {
    var ul = el('ul', 'guide-links near-links');
    var county = data.counties[place.county];
    var city = place.city && data.cities[place.city];
    show.forEach(function (kind) {
      if (kind === 'boards') {
        if (city && city.boards) item(ul, city.boards, S.cityBoards(place.city), S.cityBoardsNote);
        else if (city && city.site) item(ul, city.site, S.cityOf(place.city), S.noBoardsPage);
        else if (city && city.bluebook) item(ul, city.bluebook, S.cityOf(place.city), S.noSiteBoards);
        if (county && county.boards) item(ul, county.boards, S.countyBoards(place.county), S.countyBoardsNote);
        else if (county && (county.commissioners || county.site)) item(ul, county.commissioners || county.site, S.countyCommissioners(place.county), S.noCountyBoards);
        item(ul, STATE_BOARDS, S.stateBoards, S.stateBoardsNote);
      }
      if (kind === 'site') {
        if (city && city.site) item(ul, city.site, S.cityOf(place.city), S.citySite);
        else if (city && city.bluebook) item(ul, city.bluebook, S.cityOf(place.city), S.noSiteCity);
        if (county && county.site) item(ul, county.site, S.countyOf(place.county), S.countySite);
      }
      if (kind === 'districts') {
        ((county && county.districts) || []).forEach(function (d) { item(ul, d.site, d.name, DISTRICT_NOTES[d.kind] || DISTRICT_NOTES.other); });
      }
      if (kind === 'schools') {
        var list = (county && county.schools) || [];
        list.forEach(function (s) { item(ul, s.site, s.name, S.schoolNote); });
        if (!list.length) item(ul, 'https://www.oregon.gov/ode/about-us/Pages/School-Directory.aspx', S.schoolDir, S.schoolDirNote);
      }
      if (kind === 'meetings') {
        if (place.county) item(ul, base() + S.calPage, S.meetingsIn(place.county), S.calNote);
        if (city && (city.meetings || city.site)) item(ul, city.meetings || city.site, S.cityMeetings(place.city), S.cityMeetingsNote);
        else if (city && city.bluebook) item(ul, city.bluebook, S.cityMeetings(place.city), S.noSiteMeetings);
        if (county && (county.meetings || county.site)) item(ul, county.meetings || county.site, S.countyMeetings(place.county), S.countyMeetingsNote);
      }
    });
    return ul;
  }

  function build(box, data) {
    var show = (box.getAttribute('data-show') || 'boards').split(',');
    var place = load();
    if (!data.counties[place.county]) place = {};

    box.textContent = '';
    box.appendChild(el('h2', null, box.getAttribute('data-title') || S.nearYou));
    var form = el('div', 'near-pick');
    var cl = el('label', null, S.county);
    var cs = el('select');
    cs.id = 'near-county-' + Math.random().toString(36).slice(2, 7);
    cl.htmlFor = cs.id;
    option(cs, '', S.chooseCounty, !place.county);
    Object.keys(data.counties).sort().forEach(function (c) { option(cs, c, S.countyOf(c), c === place.county); });
    var tl = el('label', null, S.cityTown);
    var ts = el('select');
    ts.id = cs.id.replace('county', 'city');
    tl.htmlFor = ts.id;
    [cl, cs, tl, ts].forEach(function (n) { form.appendChild(n); });
    box.appendChild(form);
    var out = el('div', 'near-out');
    box.appendChild(out);
    var help = el('p', 'muted');
    help.appendChild(document.createTextNode(S.notSure));
    var a = el('a', null, S.lookUp);
    a.href = base() + S.repsPage;
    help.appendChild(a);
    help.appendChild(document.createTextNode(S.remember));
    box.appendChild(help);

    function fillCities() {
      ts.textContent = '';
      var names = Object.keys(data.cities).filter(function (n) { return data.cities[n].county === cs.value; }).sort();
      option(ts, '', cs.value ? S.another : S.countyFirst, !place.city);
      names.forEach(function (n) { option(ts, n, n, n === place.city); });
      ts.disabled = !cs.value;
    }
    function draw() {
      out.textContent = '';
      if (!place.county) return;
      out.appendChild(links(data, show, place));
      if (!place.city && show.indexOf('boards') !== -1) {
        out.appendChild(el('p', 'muted', S.mostCities));
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
