/* CivicsOR special-district lookup.
   Takes the map point the Census Bureau returned for an address and asks
   three free public state map services which districts that point falls in:
   - Oregon State Fire Marshal structural fire district boundaries
   - Oregon education boundaries (education service districts and community
     college districts)
   - Oregon Department of Agriculture soil and water conservation district zones
   Only the map coordinates are sent, never the address, and nothing is kept.
   All three answer JSONP, so this works from a static site with no key.
   For addresses in Portland and Multnomah County, two local maps add the
   City Council district (City of Portland open data) and the County
   Commissioner district (Multnomah County's elections map). */
(function (root) {
  'use strict';

  var FIRE = 'https://services.arcgis.com/uUvqNMGPm7axC2dD/arcgis/rest/services/Structural_Fire_Districts_Public/FeatureServer/68/query';
  var EDU = 'https://services.arcgis.com/uUvqNMGPm7axC2dD/ArcGIS/rest/services/EDUCATIONAL_BOUNDARIES/FeatureServer/0/query';
  var SWCD = 'https://maps.oda.oregon.gov/arcgis/rest/services/Framework/ODA_AdminBounds_SoilWaterConservationDistrict_Zones/MapServer/0/query';
  // Portland City Council districts (four since 2025), from Portland Maps open data.
  var PDX_COUNCIL = 'https://www.portlandmaps.com/od/rest/services/COP_OpenData_Boundary/MapServer/1413/query';
  // Multnomah County Commissioner districts, from the county's elections map.
  var MULTCO_COMMISSION = 'https://www3.multco.us/gisagspublic/rest/services/Elections/Congress_State_Jurisdictional_Boundaries/MapServer/4/query';

  // Short forms the Fire Marshal's data uses in agency names.
  var WORDS = {
    RFPD: 'Rural Fire Protection District', RFD: 'Rural Fire District', FPD: 'Fire Protection District',
    FD: 'Fire Department', VFD: 'Volunteer Fire Department', WD: 'Water District', 'F&R': 'Fire & Rescue',
    DIST: 'District', CO: 'County', AMB: 'Ambulance', EMERG: 'Emergency', SRVCS: 'Services', INTL: 'International',
    MT: 'Mount', ST: 'St.', VLY: 'Valley', LK: 'Lake', BCH: 'Beach', N: 'North', SW: 'Southwest',
    SPRGFD: 'Springfield', EMS: 'EMS', DE: 'Department', OF: 'of', AND: 'and'
  };

  // Labels and notes in English, or in Spanish on pages under /es/
  // (<html lang="es">). District names come from the state's data and stay as they are.
  var LANG = (typeof document !== 'undefined' && document.documentElement.lang === 'es') ? 'es' : 'en';
  var S = {
    en: {
      fire: 'Fire', esd: 'Education service district', cc: 'Community college', swcd: 'Soil and water conservation',
      esdNote: 'Gives the school districts in the region special education, technology and other shared services. Run by an elected board.',
      byContract: ' (by contract)',
      ccContract: function (c) { return 'This address isn’t in a community college district. ' + c + ' serves the area under a contract, so you don’t vote for its board.'; },
      ccNote: 'Run by an elected board. Residents here pay in-district tuition.',
      zone: ', Zone ',
      swcdNote: 'Helps landowners with erosion, water quality and habitat. Its directors are elected, some by zone.'
    },
    es: {
      fire: 'Bomberos', esd: 'Distrito de servicios educativos', cc: 'Colegio comunitario', swcd: 'Conservación de suelos y agua',
      esdNote: 'Da a los distritos escolares de la región educación especial, tecnología y otros servicios compartidos. Lo dirige una junta electa.',
      byContract: ' (por contrato)',
      ccContract: function (c) { return 'Esta dirección no está dentro de un distrito de colegio comunitario. ' + c + ' atiende la zona por contrato, así que usted no vota por su junta.'; },
      ccNote: 'Lo dirige una junta electa. Los residentes de aquí pagan la matrícula reducida para residentes del distrito (in-district tuition).',
      zone: ', zona ',
      swcdNote: 'Ayuda a los propietarios de terrenos con la erosión, la calidad del agua y los hábitats. Sus directores se eligen, algunos por zona.'
    }
  }[LANG];

  var FIRE_NOTES = LANG === 'es' ? {
    'Rural Fire Protection District': 'Bomberos y respuesta a emergencias, a cargo de una junta directiva electa.',
    'County Special District': 'Bomberos y respuesta a emergencias, a cargo de un distrito de servicios del condado.',
    'Water District': 'Este distrito de agua también da protección contra incendios. Lo dirige una junta electa.',
    'Fire Department': 'Un departamento de bomberos de la ciudad u otro departamento público cubre esta dirección.',
    'Tribal': 'Un departamento de bomberos tribal cubre esta dirección.',
    'Private': 'Aquí la protección contra incendios viene de un proveedor privado, no de un distrito con impuestos.',
    'Subscription': 'Aquí la protección contra incendios es por suscripción, no de un distrito con impuestos.'
  } : {
    'Rural Fire Protection District': 'Fire and emergency response, run by an elected board of directors.',
    'County Special District': 'Fire and emergency response, run by a county service district.',
    'Water District': 'This water district also provides fire protection. An elected board runs it.',
    'Fire Department': 'A city or other public fire department covers this address.',
    'Tribal': 'A tribal fire department covers this address.',
    'Private': 'Fire protection here comes from a private provider, not a tax district.',
    'Subscription': 'Fire protection here is by subscription, not a tax district.'
  };

  // Community college districts, as the education boundaries name them.
  var COLLEGES = {
    'Portland': 'Portland Community College', 'Clackamas': 'Clackamas Community College',
    'Rogue': 'Rogue Community College', 'Southwest Oregon': 'Southwestern Oregon Community College',
    'Klamath': 'Klamath Community College', 'Blue Mountain': 'Blue Mountain Community College',
    'Columbia Gorge': 'Columbia Gorge Community College', 'Linn-Benton': 'Linn-Benton Community College',
    'Chemeketa': 'Chemeketa Community College', 'Treasure Valley': 'Treasure Valley Community College',
    'Umpqua': 'Umpqua Community College', 'Mount Hood': 'Mt. Hood Community College',
    'Tillamook Bay': 'Tillamook Bay Community College', 'Lincoln': 'Oregon Coast Community College',
    'Central Oregon': 'Central Oregon Community College', 'Lane': 'Lane Community College',
    'Clatsop': 'Clatsop Community College'
  };

  function titleWord(w) {
    return w.toLowerCase().replace(/[a-z]+/g, function (p) { return p.charAt(0).toUpperCase() + p.slice(1); })
      .replace(/^Mc([a-z])/, function (m, c) { return 'Mc' + c.toUpperCase(); });
  }

  // "TUALATIN VALLEY F&R" -> "Tualatin Valley Fire & Rescue",
  // "CLACKAMAS CO FIRE DIST 1" -> "Clackamas County Fire District 1".
  function fireName(raw) {
    var s = String(raw || '').replace(/\s+/g, ' ').trim();
    if (!s) return '';
    s = s.replace(/#\s*(\d+)/g, 'No. $1');
    return s.split(' ').map(function (w) {
      var core = w.replace(/^\(|\)$/g, '');
      var hit = WORDS.hasOwnProperty(core) ? WORDS[core] : null;
      var out = hit || core.split('-').map(function (p) { return WORDS[p] || titleWord(p); }).join('-');
      return w.replace(core, out);
    }).join(' ').replace(/^(\w)/, function (c) { return c.toUpperCase(); });
  }

  function swcdName(raw) {
    var s = String(raw || '').trim();
    return s ? s.replace(/\bSWCD\b/, 'Soil and Water Conservation District') : '';
  }

  function jsonp(url, timeoutMs) {
    return new Promise(function (resolve, reject) {
      var name = '__civicsor_d' + Date.now() + Math.floor(Math.random() * 1e6);
      var script = document.createElement('script');
      var timer = setTimeout(function () { finish(); reject(new Error('timeout')); }, timeoutMs || 15000);
      function finish() { clearTimeout(timer); delete root[name]; script.remove(); }
      root[name] = function (data) { finish(); resolve(data); };
      script.onerror = function () { finish(); reject(new Error('network')); };
      script.src = url + (url.indexOf('?') < 0 ? '?' : '&') + 'callback=' + name;
      document.head.appendChild(script);
    });
  }

  function features(response) {
    if (!response || !response.features) throw new Error('bad response');
    return response.features.map(function (f) { return f.attributes || {}; });
  }

  function fromFire(response) {
    var seen = {};
    return features(response).map(function (a) {
      return { type: 'FIRE', label: S.fire, name: fireName(a.Agency_Name), note: FIRE_NOTES[a.Category] || '' };
    }).filter(function (d) {
      if (!d.name || seen[d.name]) return false;
      seen[d.name] = true;
      return true;
    });
  }

  function fromEducation(response) {
    var out = [];
    features(response).slice(0, 1).forEach(function (a) {
      var esd = String(a.ESD_Name || '').trim();
      if (esd) out.push({ type: 'ESD', label: S.esd, name: esd, note: S.esdNote });
      var cc = String(a.CC_Taxing_District_Name || '').trim();
      var contract = /\(contract out of district\)/i.exec(cc);
      var key = cc.replace(/\s*\(.*\)\s*$/, '').trim();
      key = Object.keys(COLLEGES).filter(function (k) { return k.toLowerCase() === key.toLowerCase(); })[0];
      if (key && contract) {
        out.push({ type: 'CC', label: S.cc, name: COLLEGES[key] + S.byContract, note: S.ccContract(COLLEGES[key]) });
      } else if (key) {
        out.push({ type: 'CC', label: S.cc, name: COLLEGES[key], note: S.ccNote });
      }
    });
    return out;
  }

  function fromSwcd(response) {
    return features(response).slice(0, 1).filter(function (a) { return swcdName(a.SWCD_Name); }).map(function (a) {
      var name = swcdName(a.SWCD_Name);
      var zone = a.Zone != null && String(a.Zone).trim() !== '' ? String(a.Zone).trim() : '';
      return { type: 'SWCD', label: S.swcd, name: name + (zone ? S.zone + zone : ''), note: S.swcdNote };
    });
  }

  // A district number, "1" to "4", from either local map; '' if none.
  function districtNumber(response, field) {
    var a = features(response)[0];
    var m = a ? /(\d+)/.exec(String(a[field] == null ? '' : a[field])) : null;
    return m ? String(Number(m[1])) : '';
  }
  function fromCouncil(response) { return districtNumber(response, 'DISTRICT'); }
  function fromCommission(response) { return districtNumber(response, 'DIST_ID'); }

  function query(base, x, y, fields) {
    return base + '?geometry=' + encodeURIComponent(x + ',' + y) + '&geometryType=esriGeometryPoint&inSR=4326' +
      '&spatialRel=esriSpatialRelIntersects&outFields=' + fields + '&returnGeometry=false&f=json';
  }

  // Each source can fail on its own; a null result means that one didn't answer.
  function lookup(x, y) {
    var safe = function (p) { return p.catch(function () { return null; }); };
    return Promise.all([
      safe(jsonp(query(FIRE, x, y, 'Agency_Name,Category')).then(fromFire)),
      safe(jsonp(query(EDU, x, y, 'ESD_Name,CC_Taxing_District_Name')).then(fromEducation)),
      safe(jsonp(query(SWCD, x, y, 'SWCD_Name,Zone')).then(fromSwcd))
    ]).then(function (r) { return { fire: r[0], education: r[1], swcd: r[2] }; });
  }

  // Portland and Multnomah County only: which council and commissioner
  // district the point is in. Each is null if its map didn't answer, '' if
  // the point is outside it, and undefined (not asked) for other places.
  function localDistricts(x, y, where) {
    var safe = function (p) { return p.catch(function () { return null; }); };
    var skip = Promise.resolve(undefined);
    return Promise.all([
      where.city === 'Portland' ? safe(jsonp(query(PDX_COUNCIL, x, y, 'DISTRICT')).then(fromCouncil)) : skip,
      where.county === 'Multnomah' ? safe(jsonp(query(MULTCO_COMMISSION, x, y, 'DIST_ID')).then(fromCommission)) : skip
    ]).then(function (r) { return { council: r[0], commission: r[1] }; });
  }

  var api = { lookup: lookup, localDistricts: localDistricts, fromFire: fromFire, fromEducation: fromEducation,
    fromSwcd: fromSwcd, fromCouncil: fromCouncil, fromCommission: fromCommission, fireName: fireName };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.CivicsORDistricts = api;
})(typeof window !== 'undefined' ? window : this);
