"""Guías de CivicsOR en español (noviembre de 2026), primer grupo.

Mismos datos, plazos y fuentes que las guías en inglés de guides_or.py y
guides_or2.py. Cada página queda en site/es/guides/<slug>.html, con el mismo
slug que la versión en inglés. Si cambia un dato en inglés, cámbielo aquí también.

Cada guía: cat, title, lede, body (HTML), sources [(url, etiqueta)], y
opcionalmente "short" (título más corto para la pestaña) y "desc" (descripción
para buscadores, menos de 160 caracteres).

Enlaces dentro del cuerpo: "../" (el calendario), "../reps.html" y "<slug>.html" llevan
a páginas en español. Las guías que todavía no están en español se enlazan a
la versión en inglés con ../../guides/<slug>.html, hreflang="en" y "(en inglés)".

Glosario (para mantener los términos iguales en todas las guías):
  Public Meetings Law = Ley de Reuniones Públicas; Public Records Law = Ley de
  Registros Públicos; governing body = órgano de gobierno; public hearing =
  audiencia pública; work session = sesión de trabajo; clerk = secretario
  (clerk); records officer = encargado de registros; denial = denegación;
  circuit court = corte de circuito; district attorney = fiscal de distrito;
  Attorney General = Fiscal General; drop box = buzón oficial; voters'
  pamphlet = folleto del votante; felony = delito grave; misdemeanor = delito
  menor; parole = libertad bajo palabra; probation = libertad condicional;
  school board = junta escolar; levy = impuesto local; testify = testificar.
"""

G = {}

PML = "https://www.oregonlegislature.gov/bills_laws/ors/ors192.html"
OGEC_PML = "https://www.oregon.gov/ogec/Public-Meetings-Law"
FIND_LEG = "https://geo.maps.arcgis.com/apps/instant/lookup/index.html?appid=fd070b56c975456ea2a25f7e3f4289d1"
VOTE = "https://sos.oregon.gov/voting-elections/Pages/default.aspx"
REGISTER = "https://sos.oregon.gov/elections/Pages/registration.aspx"
EN = 'hreflang="en"'

# ---------------------------------------------------------------- empiece aquí

G["contact-your-representatives"] = dict(
    cat="Habilidades", title="Cómo comunicarse con quienes le representan",
    short="Cómo comunicarse con sus representantes",
    lede="Un mensaje corto y concreto de alguien que vive en el distrito sí se lee. Así se escoge la oficina correcta y esto es lo que debe decir el mensaje.",
    body=f"""
  <h2>Empiece con el nivel de gobierno correcto</h2>
  <p>La manera más rápida de no llegar a ningún lado es preguntarle a la oficina equivocada. Como guía general:</p>
  <ul>
    <li><strong>Ciudad:</strong> zonificación y permisos de construcción dentro de los límites de la ciudad, calles y banquetas de la ciudad, policía municipal, parques, agua y alcantarillado.</li>
    <li><strong>Condado:</strong> elecciones, avalúos e impuestos a la propiedad, el alguacil (sheriff) y la cárcel, la oficina del fiscal de distrito (district attorney), salud pública, y el uso de suelo fuera de los límites de la ciudad.</li>
    <li><strong>Metro:</strong> en el área de Portland, el gobierno regional electo se encarga del límite de crecimiento urbano (urban growth boundary), la basura y el reciclaje, los parques regionales y los servicios de vivienda con apoyo (supportive housing services).</li>
    <li><strong>Distritos especiales:</strong> los distritos de bomberos, agua, parques, transporte público, puertos y bibliotecas tienen cada uno su propia junta electa.</li>
    <li><strong>Estado:</strong> el financiamiento de las escuelas, las carreteras estatales, las prisiones, el Plan de Salud de Oregon (Oregon Health Plan), el seguro de desempleo, el DMV y las leyes estatales en general.</li>
    <li><strong>Federal:</strong> Seguro Social y Medicare, beneficios para veteranos, inmigración, pasaportes, impuestos federales, y los bosques nacionales y otras tierras federales que cubren gran parte de Oregon.</li>
  </ul>
  <p>¿No sabe quiénes le representan? Use <a href="../reps.html">Quién le representa</a>.</p>

  <h2>Qué poner en el mensaje</h2>
  <ol>
    <li><strong>Diga que es residente del distrito (constituent).</strong> Mencione su ciudad o pueblo. Las oficinas clasifican el correo según si usted vive en el distrito.</li>
    <li><strong>Haga una sola petición.</strong> "Por favor vote a favor del proyecto de ley House Bill 2001" funciona mejor que una opinión general. Incluya el número del proyecto de ley o del asunto de la agenda si lo tiene.</li>
    <li><strong>Dé su razón en pocas frases.</strong> Cómo le afecta a usted, a su familia o a su trabajo.</li>
    <li><strong>Que no pase de una página corta.</strong></li>
    <li><strong>Pida una respuesta</strong> e incluya cómo contactarle. Puede escribir en español; si lo necesita, diga que prefiere una respuesta en español.</li>
  </ol>

  <h2>Correo, teléfono o en persona</h2>
  <ul>
    <li><strong>El correo electrónico</strong> es lo más fácil de enviar y de dar seguimiento. La dirección de correo y el teléfono en el Capitolio de cada legislador están en el sitio web de la Legislatura (en inglés).</li>
    <li><strong>Una llamada</strong> es rápida. Tenga lista su única petición. Si no sabe a quién llamar, la línea de información de la Legislatura es el 1-800-332-2313.</li>
    <li><strong>Entre sesiones,</strong> los legisladores están en sus distritos. Muchos hacen reuniones comunitarias (town halls) y encuentros informales con café. A menudo es el mejor momento para que le escuchen, y el momento de llevarles una idea para un proyecto de ley.</li>
    <li><strong>En persona</strong> funciona mejor a nivel local. Vea <a href="speak-at-a-public-meeting.html">cómo hablar en una reunión pública local</a>.</li>
  </ul>

  <h2>Cuando necesita ayuda, no un voto</h2>
  <p>Si tiene un problema con una agencia de gobierno, las oficinas de los funcionarios electos a menudo pueden ayudar. Los miembros del Congreso tienen personal que atiende problemas con agencias federales. Los legisladores estatales pueden preguntarle a una agencia estatal por su caso. Llame a la oficina y pida ayuda con un asunto de residente del distrito ("constituent issue").</p>
""",
    sources=[(FIND_LEG, "Find Your Legislator, Legislatura de Oregon (en inglés)"),
             ("https://www.oregonlegislature.gov/", "Legislatura del Estado de Oregon (en inglés)")],
)

G["voting-in-oregon"] = dict(
    cat="Estado", title="Votar en Oregon, también después de una condena",
    short="Votar en Oregon",
    desc="Oregon vota por correo. Quién puede votar, cómo registrarse, cómo devolver su boleta a tiempo y qué dice la ley sobre votar con antecedentes penales.",
    lede="Oregon vota por correo. Así se registra para votar, así devuelve su boleta a tiempo, y esto es lo que dice la ley sobre votar con antecedentes penales.",
    body=f"""
  <h2>Registrarse para votar</h2>
  <ul>
    <li><strong>Para registrarse y votar, debe ser ciudadano de EE. UU.</strong> También debe vivir en Oregon y tener por lo menos 16 años para registrarse. Recibe su primera boleta para la primera elección que caiga en su cumpleaños número 18 o después. Los residentes permanentes (green card) y otras personas que no son ciudadanas no pueden registrarse ni votar en Oregon.</li>
    <li><strong>Regístrese a más tardar 21 días antes de una elección.</strong> Puede registrarse en línea con una licencia de manejo o identificación (ID) de Oregon, o por correo.</li>
    <li><strong>Muchas personas quedan registradas automáticamente</strong> cuando sacan o renuevan una licencia o ID de Oregon en el DMV, y reciben una tarjeta por correo que les pregunta a qué partido quieren pertenecer, si a alguno.</li>
    <li><strong>Actualice su registro cuando se mude,</strong> para que su boleta le llegue.</li>
  </ul>

  <h2>Su boleta</h2>
  <p>Cada votante registrado recibe una boleta por correo unas dos semanas y media antes de cada elección, junto con un folleto del votante (voters' pamphlet) para las elecciones estatales.</p>
  <ul>
    <li><strong>Devuélvala en un buzón oficial (drop box)</strong> a más tardar a las 8 p. m. del día de la elección. Es la manera más segura.</li>
    <li><strong>O envíela por correo.</strong> El franqueo ya está pagado. Una boleta enviada por correo cuenta si tiene <strong>matasellos (postmark) a más tardar el día de la elección</strong> y llega dentro de los siete días siguientes. Los matasellos se han estado retrasando, así que la Secretaría de Estado recomienda enviar su boleta por correo por lo menos una semana antes del día de la elección, o pedir en el mostrador de la oficina de correos que le pongan el matasellos a mano.</li>
    <li><strong>Firme el sobre.</strong> Su firma se compara con la de su registro. Si hay un problema, su condado se comunicará con usted y le dará tiempo para corregirlo.</li>
    <li><strong>¿Necesita ayuda o una boleta de reemplazo?</strong> Llame a la oficina de elecciones de su condado. Cada condado también tiene opciones de votación accesibles.</li>
  </ul>

  <h2>Votar con antecedentes penales</h2>
  <p>Oregon tiene una de las reglas más sencillas del país:</p>
  <ul>
    <li><strong>Solo pierde el derecho a votar mientras está en prisión por una condena por un delito grave (felony).</strong></li>
    <li><strong>Su derecho a votar vuelve automáticamente cuando sale en libertad,</strong> también si está en libertad bajo palabra (parole) o en supervisión posterior a la prisión (post-prison supervision). Sí tiene que registrarse otra vez.</li>
    <li><strong>Puede votar</strong> si está en libertad condicional (probation), si está en la cárcel en espera de juicio, o si cumple en la cárcel una sentencia por un delito menor (misdemeanor).</li>
    <li>La misma regla se aplica a las condenas federales de los residentes de Oregon.</li>
  </ul>
  <p>Si está ayudando a alguien que sale de prisión, registrarse para votar puede ir en la lista de pasos para la reintegración (reentry), junto con la identificación y los beneficios.</p>
""",
    sources=[(VOTE, "Votación y elecciones, Secretaría de Estado de Oregon (en inglés)"),
             (REGISTER, "Registrarse para votar: quién puede registrarse, Secretaría de Estado de Oregon (en inglés)"),
             ("https://sos.oregon.gov/elections/Pages/faq.aspx", "Preguntas frecuentes sobre elecciones, incluida la regla del matasellos, Secretaría de Estado de Oregon (en inglés)"),
             ("https://multco.us/info/voting-rights-oregon-person-convicted-felony-frequently-asked-questions", "Derecho al voto de las personas condenadas por un delito grave, Elecciones del Condado de Multnomah (en inglés)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors137.html", "ORS 137.281, derechos durante el encarcelamiento, Legislatura de Oregon (en inglés)")],
)

# ---------------------------------------------------------------- local

G["speak-at-a-public-meeting"] = dict(
    cat="Local", title="Cómo hablar en una reunión pública local",
    short="Cómo hablar en una reunión pública",
    desc="Lo que la Ley de Reuniones Públicas de Oregon le garantiza, lo que no, y cómo aprovechar sus dos o tres minutos.",
    lede="Lo que la Ley de Reuniones Públicas de Oregon le garantiza, lo que no, y cómo aprovechar bien sus dos o tres minutos.",
    body=f"""
  <h2>Lo que la ley de Oregon le garantiza</h2>
  <p>La Ley de Reuniones Públicas de Oregon (Public Meetings Law, ORS 192.610 a 192.705) se aplica a los órganos de gobierno de ciudades, condados, distritos escolares, distritos especiales y juntas estatales, y a los comités y grupos asesores que les hacen recomendaciones.</p>
  <ul>
    <li><strong>Puede asistir.</strong> Las reuniones están abiertas al público, y un quórum no puede reunirse en privado para decidir o deliberar, fuera de las pocas excepciones que permite la ley.</li>
    <li><strong>Recibe aviso.</strong> Cada reunión necesita un aviso público, con la hora y el lugar y una lista de los temas principales que el órgano espera tratar. Una reunión especial necesita por lo menos 24 horas de aviso.</li>
    <li><strong>Puede asistir desde su casa.</strong> Según una ley de 2021, los órganos de gobierno deben ofrecer, dentro de lo razonable, una manera de asistir por teléfono o video. Cuando reciben testimonio en persona, también deben dejar que la gente testifique a distancia o envíe su testimonio por escrito por correo electrónico.</li>
    <li><strong>Puede grabar.</strong> En general, en Oregon se necesita el consentimiento de todos para grabar una conversación, pero la ley hace una excepción para las reuniones y audiencias públicas de los órganos de gobierno.</li>
  </ul>

  <h2>Lo que no le garantiza</h2>
  <p><strong>La Ley de Reuniones Públicas le da el derecho a observar, no siempre el derecho a hablar.</strong> Un órgano no está obligado a recibir comentarios del público en una reunión ordinaria. La mayoría de los concejos municipales, juntas de condado y juntas escolares lo hacen por decisión propia, según sus propias reglas.</p>
  <p><strong>Las audiencias públicas son diferentes.</strong> Cuando una ley exige una audiencia, la gente tiene derecho a testificar. Eso incluye el presupuesto anual y la mayoría de las decisiones de uso de suelo. Si quiere asegurarse de que le escuchen, una audiencia pública es el lugar.</p>

  <section class="near-you" data-show="meetings" data-title="Reuniones cerca de usted" aria-label="Reuniones cerca de usted"></section>

  <h2>Antes de la reunión</h2>
  <ol>
    <li><strong>Encuentre la reunión.</strong> El <a href="../">calendario</a> muestra lo que viene cerca de usted.</li>
    <li><strong>Lea la agenda.</strong> Busque el asunto que le interesa. Fíjese si es una audiencia pública, un punto de acción (action item) o una sesión de trabajo (work session), en la que el órgano habla del tema pero por lo general no vota ni recibe testimonio. Casi todas las agendas están en inglés; puede pedirle ayuda al secretario (clerk).</li>
    <li><strong>Averigüe cómo inscribirse.</strong> Muchos órganos piden que se inscriba con anticipación, sobre todo para hablar en línea. El Condado de Multnomah, por ejemplo, cierra la inscripción a las 4 p. m. del miércoles anterior a sus reuniones de los jueves. Las reglas de inscripción suelen estar en la agenda.</li>
    <li><strong>Envíe también comentarios por escrito.</strong> El testimonio por escrito queda en el registro aunque usted no pueda quedarse, y es la manera más segura de dejar constancia de un asunto en un caso de uso de suelo.</li>
  </ol>

  <h2>En la reunión</h2>
  <ul>
    <li><strong>Diga su nombre y dónde vive.</strong></li>
    <li><strong>Haga un solo punto, y hágalo al principio.</strong> La mayoría de los órganos dan dos o tres minutos. Vea <a href="../../guides/two-minute-pitch.html" {EN}>cómo preparar un mensaje de dos minutos (en inglés)</a>.</li>
    <li><strong>Hable al órgano completo,</strong> no al personal ni al público. Por lo general, los funcionarios no contestan preguntas durante los comentarios del público, y eso es normal.</li>
    <li><strong>Deje una copia</strong> de lo que dijo con el secretario (clerk) o la persona que toma el acta.</li>
  </ul>

  <h2>Después</h2>
  <p>Revise el acta o la grabación para ver qué pasó. Dé seguimiento por correo electrónico a los miembros. Si la decisión todavía no se ha tomado, vuelva cuando esté en la agenda para votación.</p>
""",
    sources=[(PML, "ORS capítulo 192, Ley de Reuniones Públicas, Legislatura de Oregon (en inglés)"),
             (OGEC_PML, "Ley de Reuniones Públicas, Comisión de Ética del Gobierno de Oregon (en inglés)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors165.html", "ORS 165.540, grabación de conversaciones, Legislatura de Oregon (en inglés)"),
             ("https://multco.us/info/about-board-meetings", "Sobre las reuniones de la junta, Condado de Multnomah (en inglés)"),
             ("https://multco.us/info/public-testimony-webform", "Inscripción para dar testimonio público, Condado de Multnomah (en inglés)")],
)

G["public-records-requests"] = dict(
    cat="Local", title="Cómo pedir registros públicos en Oregon",
    lede="Cómo pedir correos electrónicos, contratos e informes, cuánto puede costar, los plazos y qué hacer si le dicen que no.",
    body="""
  <h2>Su derecho</h2>
  <p>Según la Ley de Registros Públicos de Oregon (Public Records Law, ORS 192.311 a 192.478), cualquier persona puede pedir revisar u obtener una copia de un registro público de una agencia estatal, un condado, una ciudad, un distrito escolar o un distrito especial. No tiene que decir para qué lo quiere. Un registro público es cualquier escrito sobre los asuntos públicos, en cualquier forma: correos electrónicos, mensajes de texto, hojas de cálculo, videos, mapas y más.</p>

  <h2>Cómo hacer la solicitud</h2>
  <ol>
    <li><strong>Busque la agencia correcta</strong> y a su encargado de registros (records officer). Muchas agencias tienen un formulario de solicitud en línea.</li>
    <li><strong>Hágalo por escrito.</strong> Los plazos legales empiezan cuando la agencia recibe una solicitud por escrito. Puede escribir en español, pero la respuesta y los documentos probablemente estarán en inglés.</li>
    <li><strong>Dé detalles concretos.</strong> Nombre los documentos, las personas o los temas, y un rango de fechas. "Los correos entre el administrador de la ciudad y el director de parques sobre el contrato del parque Riverside, del 1 de enero al 31 de marzo de 2026" recibe una respuesta más rápida y más barata que "todos los correos sobre el parque".</li>
    <li><strong>Pida copias electrónicas</strong> si le sirven. Por lo general cuestan menos.</li>
  </ol>

  <h2>Plazos</h2>
  <ul>
    <li><strong>Dentro de 5 días hábiles,</strong> la agencia debe confirmar que recibió su solicitud por escrito, o terminar su respuesta.</li>
    <li><strong>Dentro de los 10 días hábiles siguientes,</strong> debe terminar su respuesta o darle por escrito un cálculo de cuándo la terminará y de cualquier cobro.</li>
    <li><strong>La regla general</strong> es responder tan pronto como sea posible y sin demoras injustificadas. Las solicitudes grandes pueden tardar más; la agencia debe explicarle por qué.</li>
  </ul>

  <h2>Costos</h2>
  <p>Una agencia puede cobrar una tarifa razonable para cubrir lo que realmente le cuesta buscar, revisar y copiar los documentos, y puede pedirle que pague antes de empezar. Debe darle primero un cálculo del costo si el cobro será de más de $25. <strong>Puede pedir que le eximan del pago o se lo reduzcan</strong> si entregar los documentos es de interés público, por ejemplo porque muestran cómo está funcionando el gobierno. Explique por qué en su solicitud.</p>

  <h2>Si le dicen que no</h2>
  <ul>
    <li><strong>Pregunte en qué excepción se basan.</strong> La ley de Oregon enumera los tipos de documentos que se pueden retener, como algunos expedientes de personal y médicos y documentos sobre litigios pendientes. Muchas veces solo se puede retener una parte de un documento, y el resto se debe entregar.</li>
    <li><strong>Pida una revisión.</strong> Si una agencia estatal deniega su solicitud, puede presentar una petición de revisión ante el Fiscal General (Attorney General). Si lo hace una agencia local, puede presentarla ante el fiscal de distrito (district attorney) de ese condado. Cualquiera de los dos puede ordenar que se entreguen los documentos. También puede ir a la corte de circuito (circuit court).</li>
    <li><strong>Pida ayuda.</strong> El Defensor de Registros Públicos de Oregon (Public Records Advocate) ayuda a resolver desacuerdos sobre solicitudes a agencias estatales, y a órganos locales que acepten participar.</li>
  </ul>
""",
    sources=[("https://www.oregonlegislature.gov/bills_laws/ors/ors192.html", "ORS capítulo 192, Ley de Registros Públicos, Legislatura de Oregon (en inglés)"),
             ("https://www.doj.state.or.us/oregon-department-of-justice/public-records/", "Registros públicos, Departamento de Justicia de Oregon (en inglés)"),
             ("https://www.oregon.gov/pra/", "Oficina del Defensor de Registros Públicos (en inglés)")],
)

G["your-school-board"] = dict(
    cat="Local", title="Su junta escolar",
    desc="Las juntas escolares de Oregon se eligen en mayo y deciden el presupuesto, el plan de estudios y quién dirige el distrito.",
    lede="Las juntas escolares de Oregon se eligen en mayo, en elecciones con poca participación, y deciden el presupuesto, la política sobre el plan de estudios y quién dirige el distrito.",
    body=f"""
  <h2>Qué hace una junta escolar</h2>
  <ul>
    <li>Contrata y evalúa al superintendente.</li>
    <li>Aprueba el presupuesto, con un comité de presupuesto que incluye un número igual de residentes nombrados por la junta.</li>
    <li>Fija las políticas del distrito, aprueba los materiales del plan de estudios y los contratos laborales, y decide si pedirles a los votantes bonos o impuestos locales opcionales (local option levies).</li>
  </ul>
  <p>Las decisiones del día a día en una escuela le tocan al director o la directora y al personal del distrito, así que empiece allí si tiene un problema con un salón o un estudiante.</p>

  <h2>Elecciones</h2>
  <ul>
    <li>Los miembros de la junta tienen periodos de cuatro años y se eligen en una boleta no partidista en mayo de los años impares. Más o menos la mitad de los puestos se eligen cada vez.</li>
    <li>La próxima elección de juntas escolares es el <strong>18 de mayo de 2027</strong>. Los candidatos se inscriben en la oficina de elecciones del condado. La inscripción abre el 6 de febrero de 2027. Los miembros de la junta que fueron elegidos y se postulan otra vez deben inscribirse a más tardar el <strong>11 de marzo de 2027</strong>. Todos los demás, incluidos los miembros de la junta que fueron nombrados, tienen hasta el <strong>18 de marzo de 2027</strong>.</li>
    <li>Solo los ciudadanos de EE. UU. registrados para votar pueden votar en estas elecciones o postularse a la junta. Los residentes permanentes (green card) y otras personas que no son ciudadanas no pueden.</li>
    <li>La participación en estas elecciones suele ser baja, así que cada voto pesa más.</li>
  </ul>

  <section class="near-you" data-show="schools" data-title="Distritos escolares de su condado" aria-label="Distritos escolares de su condado"></section>

  <h2>Cómo participar</h2>
  <ul>
    <li><strong>Encuentre las reuniones.</strong> Las juntas suelen reunirse una o dos veces al mes. Las agendas se publican unos días antes, muchas veces en BoardDocs o en el sitio web del distrito, y casi siempre en inglés. Muchos distritos están en el <a href="../">calendario comunitario</a>.</li>
    <li><strong>Hable durante los comentarios del público.</strong> La mayoría de las juntas reservan un tiempo y le piden que se inscriba antes. Vea <a href="speak-at-a-public-meeting.html">cómo hablar en una reunión pública</a>.</li>
    <li><strong>Únase al comité de presupuesto</strong> o a un comité asesor del distrito.</li>
    <li><strong>Postúlese.</strong> Debe ser un votante registrado que vive en el distrito, y algunas zonas tienen sus propias reglas de residencia. Vea <a href="../../guides/running-for-office.html" {EN}>cómo postularse a un cargo (en inglés)</a>.</li>
  </ul>
""",
    sources=[("https://ballotpedia.org/Rules_governing_school_board_election_dates_and_timing_in_Oregon", "Fechas de elecciones de juntas escolares en Oregon, Ballotpedia (en inglés)"),
             ("https://sos.oregon.gov/elections/Documents/Candidate-SEL190-Highlighted.pdf", "Fechas de inscripción para las elecciones de distrito de 2027, formulario SEL 190, Secretaría de Estado de Oregon (en inglés)"),
             ("https://apps.oregon.gov/oregon-newsroom/OR/SOS/Posts/Post/candidate-filing-window-opens-today-new-deadlines", "Plazo de inscripción más temprano para quienes ya ocupan el cargo por elección, Secretaría de Estado de Oregon (en inglés)"),
             (REGISTER, "Registrarse para votar: quién puede registrarse, Secretaría de Estado de Oregon (en inglés)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors332.html", "ORS capítulo 332, administración local de la educación, Legislatura de Oregon (en inglés)"),
             ("https://www.osba.org/", "Asociación de Juntas Escolares de Oregon (en inglés)")],
)
