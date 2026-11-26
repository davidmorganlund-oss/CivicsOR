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
      Portland: { label: 'Portland City Council agendas', url: 'https://www.portland.gov/council/agenda', note: 'Meetings, agendas and how to testify. Since 2025, each of Portland’s four districts elects three councilors',
                  label_es: 'Agendas del Concejo Municipal de Portland (en inglés)', note_es: 'Reuniones, agendas y cómo testificar. Desde 2025, cada uno de los cuatro distritos de Portland elige a tres concejales' },
      Salem: { label: 'Salem City Council agendas', url: 'https://www.cityofsalem.net/government/city-council-mayor/city-council-meetings/city-council-meeting-agendas-and-minutes', note: 'Meetings, agendas and how to comment',
               label_es: 'Agendas del Concejo Municipal de Salem (en inglés)', note_es: 'Reuniones, agendas y cómo enviar comentarios' }
    },
    counties: {
      Multnomah: { label: 'Multnomah County Board of Commissioners', url: 'https://multco.us/info/about-board-meetings', note: 'Meetings, agendas and how to testify',
                   label_es: 'Junta de Comisionados del Condado de Multnomah (en inglés)', note_es: 'Reuniones, agendas y cómo testificar' },
      Clackamas: { label: 'Clackamas County Board of County Commissioners', url: 'https://www.clackamas.us/meetings/bcc/business', note: 'Business meetings and agendas',
                   label_es: 'Junta de Comisionados del Condado de Clackamas (en inglés)', note_es: 'Reuniones de trabajo (business meetings) y agendas' },
      Washington: { label: 'Washington County Board of Commissioners', url: 'https://www.washingtoncountyor.gov/bcc', note: 'Members, meetings and agendas',
                    label_es: 'Junta de Comisionados del Condado de Washington (en inglés)', note_es: 'Miembros, reuniones y agendas' }
    }
  };

  // English and Spanish wording. The page under /es/ sets <html lang="es">.
  // Names, phone numbers and district numbers come from the data and stay as they are.
  var LANG = document.documentElement.lang === 'es' ? 'es' : 'en';
  var BASE = LANG === 'es' ? '../' : '';
  var S = {
    en: {
      locale: 'en-US',
      termWho: ['New members of Congress', 'New members of the Oregon Legislature'],
      tookOffice: ' took office ', takeOffice: ' take office ',
      termLag: ' The lists below can lag by a few weeks after a new term starts.',
      termUntil: ' Until then, the lists below show the members serving now.',
      dEyebrow: 'Your districts', dTitle: 'Every district you live in',
      usHouse: 'U.S. House', cd: function (n) { return 'Congressional District ' + n; },
      stSenate: 'State Senate', sdName: function (n) { return 'Senate District ' + n; },
      stHouse: 'State House', hdName: function (n) { return 'House District ' + n; },
      county: 'County', countyOf: function (c) { return c + ' County'; },
      city: 'City', cityOf: function (c) { return 'City of ' + c; }, unincorporated: 'Unincorporated (outside city limits)',
      school: 'School district', schoolNote: 'An elected school board runs your public schools.',
      tribal: 'Tribal land', tribalNote: 'This address is on tribal land. The tribe’s own government serves its members here.',
      dLooking: 'Looking up fire, education and conservation districts…',
      dNone: 'We could not look up special districts for this address.',
      council: 'City council', councilName: function (n) { return 'Portland City Council District ' + n; },
      commission: 'County commission', commissionName: function (n) { return 'Multnomah County Commissioner District ' + n; },
      dPartial: 'Part of the district lookup did not respond, so this list may be missing some districts. Try again in a few minutes.',
      dSource: 'Fire districts come from the Oregon State Fire Marshal’s maps, education districts from the state’s education boundary maps, and conservation districts from the Oregon Department of Agriculture.',
      dSourcePdx: ' Portland council districts come from the City of Portland’s district map.',
      dSourceMult: ' Multnomah County commissioner districts come from the county’s elections map.',
      missCommission: 'county commissioner districts', missCouncil: 'city council districts', missPrecincts: 'voting precincts',
      notListed: 'Not listed here: ',
      notListedEnd: ' and library, park, water, sanitary, transit, port and Metro districts. Your county elections office can tell you which of those you live in.',
      lookupFail: function (what) { return 'We could not look up your ' + what + ' right now. Try again in a few minutes.'; },
      seeMembers: function (who) { return 'See the ' + who + ' page for the members of this district.'; },
      membersAsListed: 'Members as listed by the ',
      seat: ' · Seat ', website: 'Website', official: 'Official website',
      boards: 'Boards and committees', commissionersLink: 'Commissioners (they appoint board members)', meetings: 'Meetings and agendas',
      mayor: 'Mayor', councilAgendas: 'City Council agendas', councilMembers: 'City council members',
      elsewhere: function (st) { return 'That address is in ' + st + '. CivicsOR only covers Oregon.'; },
      showing: function (a) { return 'Showing results for ' + a + '.'; },
      outside: 'Outside city limits',
      cityFallback: 'Your mayor and council members are listed on the city’s website. We have not added a direct link for this city yet.',
      uninc: 'This address is in an unincorporated area, so the county is your local government.',
      pdxCouncil: { heading: 'City Council, District', what: 'Portland City Council district', who: 'City of Portland' },
      multCommission: { heading: 'County Commissioner, District', what: 'county commissioner district', who: 'Multnomah County Board of Commissioners',
        chairHeading: 'County Chair (elected countywide)', note: 'Four commissioners are elected by district and the chair countywide.' },
      board: { 'Board of Commissioners': 'Board of County Commissioners', 'County Court': 'County Court' },
      courtWhat: 'A county court is a county judge and two commissioners. The judge chairs it.',
      title: { Judge: 'County Judge', Chair: 'Chair', 'Vice Chair': 'Vice Chair', 'Vice-Chair': 'Vice Chair', President: 'President', 'Pres.': 'President' },
      termEnds: function (y) { return 'Term ends January ' + y; },
      bbCounty: 'county page', bbCity: 'city page', bbSource: 'Source: Oregon Blue Book, ',
      seatsOnBallot: 'Seats with a term ending in 2027 were on the November 2026 ballot. Whoever won takes office in January 2027, and the Blue Book can take a few weeks to catch up.',
      mayorNewTerm: 'Mayors elected in November usually take office at the first council meeting in January. Check the city’s website if this looks out of date.',
      countyFallback: 'Your county commissioners are listed on the county’s website. Most Oregon counties have a board of three to five commissioners; a few smaller ones have a county court, a county judge and two commissioners.',
      legislature: 'State Legislature', legNotFound: 'Legislative districts not found',
      legTitle: function (sd, hd) { return 'Senate District ' + sd + ' · House District ' + hd; },
      senator: 'State Senator', noSenator: 'No senator listed.', rep: 'State Representative', noRep: 'No representative listed.',
      noRoster: 'We could not load the member list.',
      confirm: 'Each Senate district is two House districts put together, so you have one state senator and one state representative. Members elected in November take office in January, and this list can lag by a few weeks. Confirm current members with the Legislature’s ',
      finder: 'Find Your Legislator', pageEnd: ' page.',
      congress: 'Congress', cdNotFound: 'Congressional district not found',
      usRep: 'U.S. Representative', noUsRep: 'No representative listed.', usSens: 'U.S. Senators', noUsSens: 'No senators listed.',
      tooShort: 'Enter a street address with a city or ZIP code, like 900 Court St NE, Salem.',
      looking: 'Looking up your districts…',
      notFound: 'We could not find that address. Check the street number, spelling and ZIP code, and leave off apartment numbers. If it still isn’t found, try a nearby street address. Some government buildings aren’t in the Census Bureau’s address list.',
      down: 'The address lookup is not responding right now. You can use the Legislature’s ', downEnd: ' page instead.',
      party: {}
    },
    es: {
      locale: 'es-US',
      termWho: ['Los nuevos miembros del Congreso', 'Los nuevos miembros de la Legislatura de Oregon'],
      tookOffice: ' asumieron el cargo el ', takeOffice: ' asumen el cargo el ',
      termLag: ' Las listas de abajo pueden tardar unas semanas en actualizarse después de que empieza un nuevo periodo.',
      termUntil: ' Hasta entonces, las listas de abajo muestran a quienes ocupan los cargos ahora.',
      dEyebrow: 'Sus distritos', dTitle: 'Todos los distritos donde vive',
      usHouse: 'Cámara de Representantes federal', cd: function (n) { return 'Distrito congresional ' + n; },
      stSenate: 'Senado estatal', sdName: function (n) { return 'Distrito del Senado ' + n; },
      stHouse: 'Cámara estatal', hdName: function (n) { return 'Distrito de la Cámara ' + n; },
      county: 'Condado', countyOf: function (c) { return 'Condado de ' + c; },
      city: 'Ciudad', cityOf: function (c) { return 'Ciudad de ' + c; }, unincorporated: 'Área no incorporada (fuera de los límites de la ciudad)',
      school: 'Distrito escolar', schoolNote: 'Una junta escolar electa dirige sus escuelas públicas.',
      tribal: 'Tierra tribal', tribalNote: 'Esta dirección está en tierra tribal. El gobierno de la tribu atiende a sus miembros aquí.',
      dLooking: 'Buscando distritos de bomberos, de educación y de conservación…',
      dNone: 'No pudimos buscar los distritos especiales de esta dirección.',
      council: 'Concejo municipal', councilName: function (n) { return 'Distrito ' + n + ' del Concejo Municipal de Portland'; },
      commission: 'Comisión del condado', commissionName: function (n) { return 'Distrito ' + n + ' de Comisionados del Condado de Multnomah'; },
      dPartial: 'Una parte de la búsqueda de distritos no respondió, así que puede que falten algunos distritos en esta lista. Intente de nuevo en unos minutos.',
      dSource: 'Los distritos de bomberos vienen de los mapas de la Oficina del Jefe de Bomberos del Estado de Oregon, los distritos de educación de los mapas de límites educativos del estado, y los distritos de conservación del Departamento de Agricultura de Oregon.',
      dSourcePdx: ' Los distritos del concejo de Portland vienen del mapa de distritos de la Ciudad de Portland.',
      dSourceMult: ' Los distritos de comisionados del condado de Multnomah vienen del mapa electoral del condado.',
      missCommission: 'distritos de comisionados del condado', missCouncil: 'distritos del concejo municipal', missPrecincts: 'precintos electorales',
      notListed: 'No aparecen aquí: ',
      notListedEnd: ' ni los distritos de bibliotecas, parques, agua, saneamiento, transporte público, puertos y Metro. La oficina de elecciones de su condado puede decirle en cuáles vive.',
      lookupFail: function (what) { return 'No pudimos buscar su ' + what + ' en este momento. Intente de nuevo en unos minutos.'; },
      seeMembers: function (who) { return 'Vea la página de ' + who + ' (en inglés) para los miembros de este distrito.'; },
      membersAsListed: 'Miembros según la página de ',
      seat: ' · Puesto ', website: 'Sitio web', official: 'Sitio web oficial (en inglés)',
      boards: 'Juntas y comités (en inglés)', commissionersLink: 'Comisionados (nombran a los miembros de las juntas) (en inglés)', meetings: 'Reuniones y agendas (en inglés)',
      mayor: 'Alcalde o alcaldesa', councilAgendas: 'Agendas del Concejo Municipal (en inglés)', councilMembers: 'Miembros del concejo municipal (en inglés)',
      elsewhere: function (st) { return 'Esa dirección está en ' + st + '. CivicsOR solo cubre Oregon.'; },
      showing: function (a) { return 'Resultados para ' + a + '.'; },
      outside: 'Fuera de los límites de la ciudad',
      cityFallback: 'Su alcalde o alcaldesa y los miembros del concejo aparecen en el sitio web de la ciudad. Todavía no hemos agregado un enlace directo para esta ciudad.',
      uninc: 'Esta dirección está en un área no incorporada, así que el condado es su gobierno local.',
      pdxCouncil: { heading: 'Concejo Municipal, distrito', what: 'distrito del Concejo Municipal de Portland', who: 'la Ciudad de Portland' },
      multCommission: { heading: 'Comisionados del condado, distrito', what: 'distrito de comisionados del condado', who: 'la Junta de Comisionados del Condado de Multnomah',
        chairHeading: 'Presidencia del condado (County Chair, elegida en todo el condado)', note: 'Cuatro comisionados se eligen por distrito y la presidencia en todo el condado.' },
      board: { 'Board of Commissioners': 'Junta de Comisionados del Condado', 'County Court': 'Corte del condado (county court)' },
      courtWhat: 'Una corte del condado está formada por un juez del condado y dos comisionados. El juez la preside.',
      title: { Judge: 'Juez del condado', Chair: 'Presidencia', 'Vice Chair': 'Vicepresidencia', 'Vice-Chair': 'Vicepresidencia', President: 'Presidencia', 'Pres.': 'Presidencia' },
      termEnds: function (y) { return 'Su período termina en enero de ' + y; },
      bbCounty: 'página del condado', bbCity: 'página de la ciudad', bbSource: 'Fuente: Oregon Blue Book (en inglés), ',
      seatsOnBallot: 'Los cargos cuyo período termina en 2027 estuvieron en la boleta de noviembre de 2026. Quien ganó asume el cargo en enero de 2027, y el Blue Book puede tardar unas semanas en actualizarse.',
      mayorNewTerm: 'Los alcaldes elegidos en noviembre suelen asumir el cargo en la primera reunión del concejo en enero. Consulte el sitio web de la ciudad si esto parece desactualizado.',
      countyFallback: 'Sus comisionados del condado aparecen en el sitio web del condado. La mayoría de los condados de Oregon tienen una junta de tres a cinco comisionados; algunos condados más pequeños tienen una corte del condado (county court), con un juez del condado y dos comisionados.',
      legislature: 'Legislatura estatal', legNotFound: 'No se encontraron los distritos legislativos',
      legTitle: function (sd, hd) { return 'Distrito del Senado ' + sd + ' · Distrito de la Cámara ' + hd; },
      senator: 'Senador o senadora estatal', noSenator: 'No hay senador en la lista.', rep: 'Representante estatal', noRep: 'No hay representante en la lista.',
      noRoster: 'No pudimos cargar la lista de miembros.',
      confirm: 'Cada distrito del Senado está formado por dos distritos de la Cámara, así que usted tiene un senador o senadora estatal y un o una representante estatal. Los miembros elegidos en noviembre asumen el cargo en enero, y esta lista puede tardar unas semanas en actualizarse. Confirme los miembros actuales en la página de la Legislatura ',
      finder: 'Find Your Legislator (en inglés)', pageEnd: '.',
      congress: 'Congreso', cdNotFound: 'No se encontró el distrito congresional',
      usRep: 'Representante federal', noUsRep: 'No hay representante en la lista.', usSens: 'Senadores federales', noUsSens: 'No hay senadores en la lista.',
      tooShort: 'Escriba una dirección con la ciudad o el código postal, como 900 Court St NE, Salem.',
      looking: 'Buscando sus distritos…',
      notFound: 'No pudimos encontrar esa dirección. Revise el número, cómo está escrita la calle y el código postal, y no incluya el número de apartamento. Si aún no aparece, pruebe con una dirección cercana. Algunos edificios de gobierno no están en la lista de direcciones de la Oficina del Censo.',
      down: 'La búsqueda de direcciones no responde en este momento. Puede usar la página de la Legislatura ', downEnd: '.',
      party: { Republican: 'Partido Republicano', Democrat: 'Partido Demócrata', 'Democratic/Working Families': 'Partido Demócrata y Working Families', Independent: 'Independiente' }
    }
  }[LANG];

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
      var when = dates[i].toLocaleDateString(S.locale, { month: 'long', day: 'numeric', year: 'numeric' });
      return (S.termWho[i] || t.who) + (past ? S.tookOffice : S.takeOffice) + when + '.';
    });
    return parts.join(' ') + (anyPast ? S.termLag : S.termUntil);
  }

  var officials = null;
  var localData = null;
  var mayors = null;
  var countyOfficials = null;

  // Census names some cities "Mount Angel" or "Saint ..."; local.json and the
  // Blue Book write "Mt. Angel" and "St. Helens".
  function byCity(map, city) {
    if (!map || !city) return null;
    return map[city] || map[city.replace(/^Mount /, 'Mt. ')] || map[city.replace(/^Saint /, 'St. ')] || null;
  }

  // Notes about November 2026 winners taking office show until this date.
  var NEW_LOCAL_TERMS_UNTIL = new Date(2027, 2, 1);
  function sourceLine(card, url, label) {
    if (!safeUrl(url)) return;
    var p = el('p', 'muted');
    p.appendChild(document.createTextNode(S.bbSource));
    p.appendChild(link(url, label));
    p.appendChild(document.createTextNode('.'));
    card.appendChild(p);
  }
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
    var card = section(S.dEyebrow, S.dTitle);
    var list = el('ul', 'districts');
    card.appendChild(list);
    var add = function (d) { districtItem(list, d); };
    if (parts.cd) add({ label: S.usHouse, name: S.cd(parts.cd) });
    if (parts.sd) add({ label: S.stSenate, name: S.sdName(parts.sd) });
    if (parts.hd) add({ label: S.stHouse, name: S.hdName(parts.hd) });
    if (parts.county) add({ label: S.county, name: S.countyOf(parts.county) });
    add({ label: S.city, name: parts.city ? S.cityOf(parts.city) : S.unincorporated });
    names(g, /School Districts/).forEach(function (n) {
      add({ label: S.school, name: n, note: S.schoolNote });
    });
    names(g, /American Indian Reservations|Off-Reservation Trust Lands/).forEach(function (n) {
      add({ label: S.tribal, name: n, note: S.tribalNote });
    });

    var status = el('p', 'muted', S.dLooking);
    card.appendChild(status);
    var D = window.CivicsORDistricts;
    var c = match.coordinates || {};
    if (!D || typeof c.x !== 'number' || typeof c.y !== 'number') {
      status.textContent = S.dNone;
      return card;
    }
    var local = parts.local || Promise.resolve({});
    Promise.all([D.lookup(c.x, c.y), local]).then(function (both) {
      var r = both[0], here = both[1];
      if (here.council) add({ label: S.council, name: S.councilName(here.council) });
      if (here.commission) add({ label: S.commission, name: S.commissionName(here.commission) });
      [r.fire, r.education, r.swcd].forEach(function (found) { (found || []).forEach(add); });
      status.textContent = (!r.fire || !r.education || !r.swcd || here.council === null || here.commission === null)
        ? S.dPartial
        : S.dSource + (here.council ? S.dSourcePdx : '') + (here.commission ? S.dSourceMult : '');
      var missing = [];
      if (!here.commission) missing.push(S.missCommission);
      if (!here.council) missing.push(S.missCouncil);
      card.appendChild(el('p', 'muted', S.notListed + missing.concat([S.missPrecincts]).join(', ') +
        (missing.length && LANG === 'en' ? ',' : '') + S.notListedEnd));
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
        slot.appendChild(el('p', 'muted', S.lookupFail(opts.what)));
        return;
      }
      var roster = opts.roster || {};
      slot.appendChild(el('h4', null, opts.heading + ' ' + num));
      people(slot, roster[num], S.seeMembers(opts.who));
      if (roster.chair) {
        slot.appendChild(el('h4', null, opts.chairHeading));
        people(slot, [roster.chair], '');
      }
      if (safeUrl(roster.source)) {
        var p = el('p', 'muted');
        p.appendChild(document.createTextNode((opts.note ? opts.note + ' ' : '') + S.membersAsListed));
        p.appendChild(link(roster.source, opts.who));
        p.appendChild(document.createTextNode('.'));
        slot.appendChild(p);
      }
    });
  }

  function person(p) {
    var li = el('li', 'person');
    li.appendChild(el('strong', null, p.name));
    if (p.seat) li.appendChild(el('span', 'muted', S.seat + p.seat));
    if (p.party) li.appendChild(el('span', 'muted', ' · ' + (S.party[p.party] || p.party)));
    if (p.note) li.appendChild(el('span', 'muted', ' · ' + p.note));
    var contact = el('div', 'contact');
    if (p.phone) contact.appendChild(link('tel:' + p.phone.replace(/[^\d+]/g, ''), p.phone));
    if (p.email) contact.appendChild(link('mailto:' + p.email, p.email));
    if (safeUrl(p.url)) contact.appendChild(link(p.url, S.website));
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
    if (safeUrl(place.site)) p.appendChild(link(place.site, S.official));
    var second = place.boards ? [place.boards, S.boards]
      : place.commissioners ? [place.commissioners, S.commissionersLink]
      : place.meetings ? [place.meetings, S.meetings] : null;
    if (second && safeUrl(second[0])) {
      if (p.childNodes.length) p.appendChild(document.createTextNode(' · '));
      p.appendChild(link(second[0], second[1]));
    }
    if (p.childNodes.length) card.appendChild(p);
  }

  // Mayors confirmed on each city's own website (data/local.json), with a
  // link to the council members page where we found one.
  function addMayor(card, place, city) {
    if (!place || !place.mayor) {
      // Otherwise, the mayor as the Oregon Blue Book lists them (data/mayors.json).
      var m = byCity(mayors && mayors.mayors, city);
      if (!m || !m.name) return;
      card.appendChild(el('h4', null, S.mayor));
      people(card, [{ name: m.name }], '');
      sourceLine(card, m.source, S.bbCity);
      if (new Date() < NEW_LOCAL_TERMS_UNTIL) card.appendChild(el('p', 'muted', S.mayorNewTerm));
      if (place && safeUrl(place.council)) {
        var c = el('p');
        c.appendChild(link(place.council, S.councilMembers));
        card.appendChild(c);
      }
      return true;
    }
    card.appendChild(el('h4', null, S.mayor));
    people(card, [{ name: place.mayor.name, url: place.mayor.source }], '');
    var links = card.querySelector('ul.people:last-of-type .contact a');
    // Other people's rows say "Website". Where the page we confirmed the mayor
    // on is the council's agenda page, not the mayor's own, say so.
    if (links && /\/council\/agenda/.test(place.mayor.source)) links.textContent = S.councilAgendas;
    if (place.mayor.note) card.appendChild(el('p', 'muted', place.mayor.note));
    if (safeUrl(place.council)) {
      var p = el('p');
      p.appendChild(link(place.council, S.councilMembers));
      card.appendChild(p);
    }
  }

  // County commissioners or county court, from the Oregon Blue Book
  // (data/county_officials.json). Returns true if it added the list.
  function addCountyBoard(card, county) {
    var c = countyOfficials && countyOfficials.counties && countyOfficials.counties[county];
    if (!c || !c.members || !c.members.length) return false;
    card.appendChild(el('h4', null, S.board[c.body] || c.body));
    var onBallot = false;
    people(card, c.members.map(function (m) {
      if (m.term_ends && +m.term_ends <= 2027) onBallot = true;
      var bits = [];
      if (m.title && S.title[m.title]) bits.push(S.title[m.title]);
      if (m.term_ends) bits.push(S.termEnds(m.term_ends));
      return { name: m.name, seat: m.district || '', note: bits.join(' · ') };
    }), '');
    if (c.body === 'County Court') card.appendChild(el('p', 'muted', S.courtWhat));
    if (onBallot && new Date() < NEW_LOCAL_TERMS_UNTIL) card.appendChild(el('p', 'muted', S.seatsOnBallot));
    sourceLine(card, c.source_url, S.bbCounty);
    return true;
  }

  function localCard(title, name, entry, fallback, place, key) {
    var card = section(title, name);
    var listed = title === S.city ? addMayor(card, place, key)
      : title === S.county && key ? addCountyBoard(card, key) : false;
    if (!entry && place) { extraLinks(card, place); return card; }
    if (entry) {
      var p = el('p');
      p.appendChild(link(entry.url, LANG === 'es' ? entry.label_es : entry.label));
      p.appendChild(document.createTextNode(': ' + (LANG === 'es' ? entry.note_es : entry.note) + '.'));
      card.appendChild(p);
    } else if (!listed) {
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
      out.appendChild(el('p', 'empty', S.elsewhere(state)));
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

    out.appendChild(el('p', 'muted', S.showing(match.matchedAddress)));
    out.appendChild(districtsCard(g, match, { city: city, county: county, sd: sd, hd: hd, cd: cd, local: local }));
    if (window.CivicsORLocal && county) {
      // Remember only the county and city, so the Engage guides can show local links.
      window.CivicsORLocal.save({ county: county, city: localData && localData.cities[city] ? city : '' });
    }

    var cityPlace = localData && byCity(localData.cities, city);
    var cityCard = city
      ? localCard(S.city, S.cityOf(city), LOCAL.places[city], S.cityFallback, cityPlace, city)
      : localCard(S.city, S.outside, null, S.uninc);
    if (local && city === 'Portland') {
      localDistrict(cityCard, local, 'council', { heading: S.pdxCouncil.heading, what: S.pdxCouncil.what,
        who: S.pdxCouncil.who, roster: cityPlace && cityPlace.council_districts });
    }
    out.appendChild(cityCard);

    if (county) {
      var countyPlace = localData && localData.counties[county];
      var countyCard = localCard(S.county, S.countyOf(county), LOCAL.counties[county], S.countyFallback, countyPlace, county);
      if (local && county === 'Multnomah') {
        var mc = S.multCommission;
        localDistrict(countyCard, local, 'commission', { heading: mc.heading, what: mc.what,
          who: mc.who, roster: countyPlace && countyPlace.commissioner_districts,
          chairHeading: mc.chairHeading, note: mc.note });
      }
      out.appendChild(countyCard);
    }

    var leg = officials && officials.legislators;
    var senators = leg && leg.senate ? leg.senate[sd] : null;
    var reps = leg && leg.house ? leg.house[hd] : null;
    var legCard = section(S.legislature, sd || hd ? S.legTitle(sd || '?', hd || '?') : S.legNotFound);
    if (leg) {
      legCard.appendChild(el('h4', null, S.senator));
      people(legCard, senators, S.noSenator);
      legCard.appendChild(el('h4', null, S.rep));
      people(legCard, reps, S.noRep);
    } else {
      legCard.appendChild(el('p', 'muted', S.noRoster));
    }
    var confirm = el('p', 'muted');
    confirm.appendChild(document.createTextNode(S.confirm));
    confirm.appendChild(link(LEG_FINDER, S.finder));
    confirm.appendChild(document.createTextNode(S.pageEnd));
    legCard.appendChild(confirm);
    out.appendChild(legCard);

    var congress = (officials && officials.congress) || { senators: [], house: {} };
    var fed = section(S.congress, cd ? S.cd(cd) : S.cdNotFound);
    fed.appendChild(el('h4', null, S.usRep));
    people(fed, congress.house[cd] ? [congress.house[cd]] : [], S.noUsRep);
    fed.appendChild(el('h4', null, S.usSens));
    people(fed, congress.senators, S.noUsSens);
    out.appendChild(fed);
  }

  $('lookup').addEventListener('submit', function (ev) {
    ev.preventDefault();
    var address = $('address').value.trim();
    var out = $('results');
    out.textContent = '';
    if (address.length < 6) {
      out.appendChild(el('p', 'empty', S.tooShort));
      return;
    }
    out.appendChild(el('p', 'empty', S.looking));
    geocode(/oregon|,\s*or\b|\bor\s+9\d{4}/i.test(address) ? address : address + ', OR').then(function (data) {
      var matches = data && data.result && data.result.addressMatches;
      if (!matches || !matches.length) {
        out.textContent = '';
        out.appendChild(el('p', 'empty', S.notFound));
        return;
      }
      render(matches[0]);
    }).catch(function () {
      out.textContent = '';
      var p = el('p', 'empty');
      p.appendChild(document.createTextNode(S.down));
      p.appendChild(link(LEG_FINDER, S.finder));
      p.appendChild(document.createTextNode(S.downEnd));
      out.appendChild(p);
    });
  });

  var note = $('term-note');
  var noteText = note ? termNote(new Date()) : '';
  if (noteText) { note.textContent = noteText; note.hidden = false; }

  fetch(BASE + 'data/local.json').then(function (r) { return r.json(); }).then(function (d) { localData = d; }).catch(function () {});
  fetch(BASE + 'data/officials.json').then(function (r) { return r.json(); }).then(function (d) { officials = d; }).catch(function () {});
  fetch(BASE + 'data/mayors.json').then(function (r) { return r.json(); }).then(function (d) { mayors = d; }).catch(function () {});
  fetch(BASE + 'data/county_officials.json').then(function (r) { return r.json(); }).then(function (d) { countyOfficials = d; }).catch(function () {});
})();
