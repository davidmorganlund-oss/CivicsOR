"""CivicsOR guide bodies (Oregon), first set, November 2026.

Each guide: cat, title, lede, body (HTML), sources [(url, label)].
Facts were checked against the linked sources in November 2026.
"""

G = {}

PML = "https://www.oregonlegislature.gov/bills_laws/ors/ors192.html"
OGEC_PML = "https://www.oregon.gov/ogec/Public-Meetings-Law"
OLIS = "https://olis.oregonlegislature.gov/liz/"
TESTIFY = "https://www.oregonlegislature.gov/citizen_engagement/Pages/Submit-Exhibits.aspx"
TESTIFY_HELP = "https://www.oregonlegislature.gov/OLIS_help/Pages/Testimony.aspx"
FIND_LEG = "https://geo.maps.arcgis.com/apps/instant/lookup/index.html?appid=fd070b56c975456ea2a25f7e3f4289d1"
SOS_IR = "https://sos.oregon.gov/elections/Pages/statelaw.aspx"
VOTE = "https://sos.oregon.gov/voting-elections/Pages/default.aspx"

# ---------------------------------------------------------------- start here

G["contact-your-representatives"] = dict(
    cat="Skills", title="How to contact the people who represent you",
    lede="A short, specific message from someone who lives in the district gets read. Here is how to pick the right office and what to put in the message.",
    body=f"""
  <h2>Start with the right level of government</h2>
  <p>The fastest way to get nowhere is to ask the wrong office. As a rough guide:</p>
  <ul>
    <li><strong>City:</strong> zoning and building permits inside city limits, city streets and sidewalks, city police, parks, water and sewer.</li>
    <li><strong>County:</strong> elections, property assessment and taxes, the sheriff and jail, the district attorney's office, public health, and land use outside city limits.</li>
    <li><strong>Metro:</strong> in the Portland area, the elected regional government handles the urban growth boundary, garbage and recycling, regional parks and supportive housing services.</li>
    <li><strong>Special districts:</strong> fire, water, parks, transit, ports and library districts each have their own elected board.</li>
    <li><strong>State:</strong> school funding, state highways, prisons, the Oregon Health Plan, unemployment insurance, the DMV, and state law in general.</li>
    <li><strong>Federal:</strong> Social Security and Medicare, veterans' benefits, immigration, passports, federal taxes, and the national forests and other federal land that cover much of Oregon.</li>
  </ul>
  <p>Not sure who yours are? Use <a href="../reps.html">Who represents you</a>.</p>

  <h2>What to put in the message</h2>
  <ol>
    <li><strong>Say you're a constituent.</strong> Give your city or town. Offices sort mail by whether you live in the district.</li>
    <li><strong>Make one ask.</strong> "Please vote yes on House Bill 2001" is better than a general opinion. Include the bill or agenda item number if there is one.</li>
    <li><strong>Give your reason in a few sentences.</strong> How it affects you, your family or your work.</li>
    <li><strong>Keep it to a short page.</strong></li>
    <li><strong>Ask for a reply</strong> and include how to reach you.</li>
  </ol>

  <h2>Email, phone or in person</h2>
  <ul>
    <li><strong>Email</strong> is the easiest to send and the easiest to track. Every legislator's address and Capitol phone number is on the Legislature's website.</li>
    <li><strong>A phone call</strong> is quick. Have your one ask ready. If you aren't sure who to call, the Legislature's information line is 1-800-332-2313.</li>
    <li><strong>Between sessions,</strong> legislators are home in their districts. Many hold town halls and coffee hours. That is often the best time to be heard, and the time to bring them an idea for a bill.</li>
    <li><strong>In person</strong> works best at the local level. See <a href="speak-at-a-public-meeting.html">how to speak at a local public meeting</a>.</li>
  </ul>

  <h2>When you need help, not a vote</h2>
  <p>If you're stuck with a government agency, elected officials' offices can often help. Members of Congress have staff who handle problems with federal agencies. State legislators can ask a state agency about your case. Call the office and ask for help with a constituent issue.</p>
""",
    sources=[(FIND_LEG, "Find Your Legislator (Oregon Legislature)"),
             ("https://www.oregonlegislature.gov/", "Oregon State Legislature")],
)

# ---------------------------------------------------------------- local

G["local-government"] = dict(
    cat="Local", title="How local government works in Oregon",
    lede="Counties, cities, Metro, and hundreds of special districts each run part of daily life. Here is who does what, and where you can step in.",
    body="""
  <h2>Counties</h2>
  <p>Oregon has 36 counties. Each one runs elections, assesses property and collects property taxes, runs the jail through the sheriff, prosecutes crimes through the district attorney, handles public health, and plans land use outside city limits.</p>
  <ul>
    <li><strong>Most counties are run by a board of commissioners</strong> with three to five members. In a handful of mostly rural counties, a county court does the job: a county judge, who also runs county business, and two commissioners.</li>
    <li><strong>Nine counties have home rule charters,</strong> written and amended by their own voters. Multnomah County's charter, for example, sets up an elected chair and four district commissioners.</li>
  </ul>

  <h2>Cities</h2>
  <p>Oregon has more than 240 cities. A city council (in some cities, a commission) passes local laws, sets the budget, and hires a city manager or administrator in most cities. Cities handle zoning inside city limits, police, streets, parks, water and sewer.</p>
  <p>Portland changed its government in 2025. The city now has 12 councilors, three elected from each of four districts using ranked-choice voting, and a mayor who runs city bureaus but doesn't sit on the council.</p>

  <h2>Metro</h2>
  <p>In the Portland area, Metro is a regional government elected by voters in the urban parts of Multnomah, Washington and Clackamas counties. It manages the urban growth boundary, garbage and recycling, regional parks and natural areas, the Oregon Zoo and the Oregon Convention Center, and the regional supportive housing services tax. Its council meets in public and takes testimony.</p>

  <h2>Special districts</h2>
  <p>Oregon has more than a thousand special districts, each with its own elected board: fire and rescue, water, parks and recreation, ports, transit, libraries, cemeteries, irrigation and more. School districts, education service districts and community colleges work the same way. These boards are covered by the Public Meetings Law, and their seats often go uncontested. They are a good place to get involved and to run for office.</p>

  <h2>Land use: Oregon's system is different</h2>
  <p>Since 1973, every Oregon city and county has had to plan under statewide land use goals, including citizen involvement. Each city sits inside an urban growth boundary that separates land for development from farms and forest. That makes local planning decisions matter.</p>
  <ul>
    <li><strong>Watch for notices.</strong> Neighbors near a proposed development get mailed notice of land use hearings, and notices are posted on the site.</li>
    <li><strong>Raise it, or you may lose it.</strong> If you want to appeal a land use decision to the state Land Use Board of Appeals later, you generally have to raise your issue, in writing or in testimony, before the local hearing record closes. Be specific.</li>
  </ul>

  <section class="near-you" data-show="site,districts" data-title="Your local governments" aria-label="Your local governments"></section>

  <h2>Neighborhood groups</h2>
  <p>Many cities recognize neighborhood associations, and Washington County has Citizen Participation Organizations, or CPOs, that review land use proposals and talk with county staff. They are a low-key way to learn what's coming and to be heard early.</p>
""",
    sources=[("https://sos.oregon.gov/blue-book/government/pages/about-counties.aspx", "About Oregon counties (Oregon Blue Book)"),
             ("https://www.oregonmetro.gov/", "Metro"),
             ("https://www.oregon.gov/lcd/op/pages/goals.aspx", "Oregon's statewide land use planning goals (DLCD)"),
             ("https://www.portland.gov/council/agenda", "Portland City Council agendas")],
)

G["speak-at-a-public-meeting"] = dict(
    cat="Local", title="How to speak at a local public meeting",
    lede="What Oregon's Public Meetings Law gives you, what it doesn't, and how to use your two or three minutes well.",
    body="""
  <h2>What Oregon law gives you</h2>
  <p>Oregon's Public Meetings Law (ORS 192.610 to 192.705) covers the governing bodies of cities, counties, school districts, special districts and state boards, and the committees and advisory groups that make recommendations to them.</p>
  <ul>
    <li><strong>You can attend.</strong> Meetings are open to the public, and a quorum can't meet in private to decide or deliberate, outside the narrow exceptions the law allows.</li>
    <li><strong>You get notice.</strong> Every meeting needs public notice, with the time and place and a list of the main subjects the body expects to take up. A special meeting needs at least 24 hours' notice.</li>
    <li><strong>You can attend from home.</strong> Under a 2021 law, governing bodies must reasonably give the public a way to attend by phone or video. Where they take testimony in person, they must also let people testify remotely or send written testimony by email.</li>
    <li><strong>You can record.</strong> Oregon generally requires everyone's consent to record a conversation, but the law makes an exception for public meetings and hearings of government bodies.</li>
  </ul>

  <h2>What it doesn't give you</h2>
  <p><strong>The Public Meetings Law gives you the right to watch, not always the right to speak.</strong> A board doesn't have to take public comment at an ordinary meeting. Most city councils, county boards and school boards choose to, under their own rules.</p>
  <p><strong>Public hearings are different.</strong> When a law requires a hearing, people get to testify. That includes the yearly budget and most land use decisions. If you want to be sure of being heard, a public hearing is the place.</p>

  <section class="near-you" data-show="meetings" data-title="Meetings near you" aria-label="Meetings near you"></section>

  <h2>Before the meeting</h2>
  <ol>
    <li><strong>Find the meeting.</strong> The <a href="../index.html">calendar</a> lists what's coming up near you.</li>
    <li><strong>Read the agenda.</strong> Find the item you care about. Note whether it is a public hearing, an action item, or a work session, where a board discusses but usually doesn't vote or take testimony.</li>
    <li><strong>Check how to sign up.</strong> Many bodies want you to sign up ahead of time, especially to speak online. Multnomah County, for example, closes sign-up at 4 p.m. the day before its Thursday meetings. The sign-up rules are usually on the agenda.</li>
    <li><strong>Send written comments too.</strong> Written testimony goes into the record even if you can't stay, and it's the safest way to preserve an issue in a land use case.</li>
  </ol>

  <h2>At the meeting</h2>
  <ul>
    <li><strong>Say your name and where you live.</strong></li>
    <li><strong>Make one point, and make it early.</strong> Most bodies give two or three minutes. See <a href="two-minute-pitch.html">build a two-minute pitch</a>.</li>
    <li><strong>Speak to the whole body,</strong> not to staff or the audience. Officials usually won't answer questions during public comment, and that's normal.</li>
    <li><strong>Leave a copy</strong> of your remarks with the clerk or recorder.</li>
  </ul>

  <h2>After</h2>
  <p>Check the minutes or recording to see what happened. Follow up by email with the members. If the decision is still ahead, come back when it's on the agenda for action.</p>
""",
    sources=[(PML, "ORS chapter 192, Public Meetings Law (Oregon Legislature)"),
             (OGEC_PML, "Public Meetings Law (Oregon Government Ethics Commission)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors165.html", "ORS 165.540, recording conversations (Oregon Legislature)"),
             ("https://multco.us/info/about-board-meetings", "About board meetings (Multnomah County)")],
)

G["public-meetings-law"] = dict(
    cat="Local", title="Oregon's Public Meetings Law, in plain language",
    lede="Notice, executive sessions, minutes, and what to do when a board breaks the rules.",
    body=f"""
  <h2>Who it covers</h2>
  <p>The law (ORS 192.610 to 192.705) covers the governing body of any public body: city councils, county boards and courts, school boards, special district boards, state boards and commissions, and the committees, subcommittees and advisory groups that make decisions or recommendations to them. It applies whenever a quorum meets to decide or deliberate on public business, in person, by phone, online, or through a chain of emails or messages among members.</p>

  <h2>Notice</h2>
  <ul>
    <li><strong>Every meeting needs notice</strong> that is reasonably calculated to reach the public and interested people, with the time, place and a list of the principal subjects the body expects to consider.</li>
    <li><strong>A special meeting</strong> needs at least 24 hours' notice. An emergency meeting can be called on less, but the minutes must say why.</li>
    <li><strong>Meetings must be held in the area</strong> the body serves, in a place accessible to people with disabilities, and not where discrimination is practiced.</li>
  </ul>

  <h2>Executive sessions</h2>
  <p>A governing body can meet in a closed executive session only for reasons the law lists, such as:</p>
  <ul>
    <li>hiring a public officer or employee, or considering complaints about one;</li>
    <li>negotiating to buy or sell real property, and labor negotiations;</li>
    <li>talking with its lawyer about current or likely litigation;</li>
    <li>reviewing records that are exempt from public disclosure.</li>
  </ul>
  <p>The body must announce the legal reason. Members of the news media can usually attend executive sessions, though they may be told not to report on certain things. <strong>No final action or decision can be taken in executive session.</strong> The vote has to happen in public.</p>

  <h2>Minutes and recordings</h2>
  <p>Every meeting must have written minutes or a sound, video or digital recording that shows who was there, the motions and proposals, the results of votes and how each member voted, and the substance of the discussion. They must be available to the public within a reasonable time.</p>

  <h2>When a board breaks the rules</h2>
  <ol>
    <li><strong>File a written grievance with the public body</strong> within 30 days of the alleged violation. Include your name and contact information, the date, and what happened. Many cities and counties post a grievance form.</li>
    <li><strong>The public body has 21 days to respond</strong> in writing, and must send your grievance and its response to the Oregon Government Ethics Commission.</li>
    <li><strong>Then you can file a complaint with the Ethics Commission,</strong> which has enforced the Public Meetings Law since 2024. Members found to have violated the law can face penalties.</li>
    <li><strong>You can also go to court.</strong> A decision made in violation of the law can be voided in some cases.</li>
  </ol>
  <p>Before you file, it often helps to raise the problem directly with the clerk or recorder. Many problems are mistakes that are fixed the next time.</p>
""",
    sources=[(PML, "ORS chapter 192, Public Meetings Law (Oregon Legislature)"),
             (OGEC_PML, "Public Meetings Law complaints (Oregon Government Ethics Commission)"),
             ("https://www.portland.gov/attorney/public-meeting-grievance", "Public meetings grievance (City of Portland)")],
)

G["public-records-requests"] = dict(
    cat="Local", title="How to make a public records request in Oregon",
    lede="How to ask for emails, contracts and reports, what it can cost, the deadlines, and what to do if the answer is no.",
    body="""
  <h2>Your right</h2>
  <p>Under Oregon's Public Records Law (ORS 192.311 to 192.478), anyone can ask to inspect or get a copy of a public record from a state agency, county, city, school district or special district. You don't have to say why you want it. A public record is any writing about the public's business, in any form: email, text messages, spreadsheets, video, maps and more.</p>

  <h2>How to ask</h2>
  <ol>
    <li><strong>Find the right agency</strong> and its records officer. Many agencies have an online request form.</li>
    <li><strong>Put it in writing.</strong> The legal deadlines start when the agency receives a written request.</li>
    <li><strong>Be specific.</strong> Name the records, the people or topics, and a date range. "Emails between the city manager and the parks director about the Riverside Park contract, Jan. 1 to March 31, 2026" gets a faster, cheaper answer than "all emails about the park."</li>
    <li><strong>Ask for electronic copies</strong> if that works for you. They're usually cheaper.</li>
  </ol>

  <h2>Deadlines</h2>
  <ul>
    <li><strong>Within 5 business days,</strong> the agency must acknowledge your written request, or finish its response.</li>
    <li><strong>Within 10 more business days,</strong> it must either finish its response or give you a written estimate of when it will, and of any fee.</li>
    <li><strong>The overall rule</strong> is to respond as soon as practicable and without unreasonable delay. Large requests can take longer; the agency should tell you why.</li>
  </ul>

  <h2>Costs</h2>
  <p>An agency can charge a reasonable fee to cover its actual costs of finding, reviewing and copying records, and it may ask you to pay before it starts. It must give you an estimate first if the fee will be more than $25. <strong>You can ask for a fee waiver or reduction</strong> if releasing the records is in the public interest, for example because they shed light on how government is working. Say why in your request.</p>

  <h2>If they say no</h2>
  <ul>
    <li><strong>Ask which exemption they're relying on.</strong> Oregon law lists the kinds of records that can be withheld, such as some personnel and medical records and records about pending litigation. Often only part of a record can be withheld, and the rest must be released.</li>
    <li><strong>Petition for review.</strong> If a state agency denies your request, you can petition the Attorney General. If a local agency does, you can petition the district attorney of that county. Either can order the records released. You can also go to circuit court.</li>
    <li><strong>Get help.</strong> The Oregon Public Records Advocate helps resolve disputes over requests to state agencies, and to local bodies that agree to take part.</li>
  </ul>
""",
    sources=[("https://www.oregonlegislature.gov/bills_laws/ors/ors192.html", "ORS chapter 192, Public Records Law (Oregon Legislature)"),
             ("https://www.doj.state.or.us/oregon-department-of-justice/public-records/", "Public records (Oregon Department of Justice)"),
             ("https://www.oregon.gov/pra/", "Office of the Public Records Advocate")],
)

# ---------------------------------------------------------------- state

G["legislature"] = dict(
    cat="State", title="How the Oregon Legislature works",
    lede="Who's in it, when it meets, how a bill moves, and where your voice counts.",
    body=f"""
  <h2>Who's in it</h2>
  <ul>
    <li><strong>The Senate</strong> has 30 members, elected to four-year terms.</li>
    <li><strong>The House</strong> has 60 members, elected to two-year terms.</li>
    <li>Each Senate district is made of two House districts, so every Oregonian has one state senator and one state representative. There are no term limits. <a href="../reps.html">Find yours</a>.</li>
  </ul>

  <h2>When it meets</h2>
  <ul>
    <li><strong>Long sessions</strong> start in January of odd-numbered years and can last up to 160 days. This is when the two-year state budget is written.</li>
    <li><strong>Short sessions</strong> start in February of even-numbered years and can last up to 35 days.</li>
    <li><strong>Between sessions,</strong> committees meet during Legislative Days, a few days at a time every couple of months, to study issues and hear reports. These hearings are often where next session's bills take shape. The <a href="../legislature.html">Legislature page</a> lists them.</li>
  </ul>

  <h2>How a bill moves</h2>
  <ol>
    <li><strong>A legislator or committee asks for a draft.</strong> Legislative Counsel writes it, often months before session.</li>
    <li><strong>It's introduced</strong> and sent to a committee.</li>
    <li><strong>Public hearing.</strong> The committee hears testimony. This is the main place for the public to weigh in.</li>
    <li><strong>Work session.</strong> The committee discusses, amends and votes. It doesn't usually take public testimony in a work session. Many bills never get a work session, and that's how most bills die.</li>
    <li><strong>Floor vote,</strong> then the same steps in the other chamber.</li>
    <li><strong>The governor</strong> signs, vetoes, or lets it become law without a signature.</li>
  </ol>
  <p>Session has deadlines: bills that don't get a committee vote by a set date in their first chamber usually can't move that session.</p>

  <h2>A few Oregon rules worth knowing</h2>
  <ul>
    <li><strong>Quorum:</strong> each chamber needs two-thirds of its members present to do business. Since voters passed Measure 113 in 2022, a legislator with 10 unexcused absences in a session can't serve the next term.</li>
    <li><strong>Taxes:</strong> bills that raise revenue need a three-fifths vote in each chamber.</li>
    <li><strong>Emergency clause:</strong> a bill that declares an emergency takes effect right away, and voters can't refer it to the ballot.</li>
  </ul>
  <p>Ready to weigh in? See <a href="weigh-in-on-a-state-bill.html">how to weigh in on a state bill</a>.</p>
""",
    sources=[("https://www.oregonlegislature.gov/", "Oregon State Legislature"),
             (OLIS, "Oregon Legislative Information System (OLIS)")],
)

G["weigh-in-on-a-state-bill"] = dict(
    cat="State", title="How to weigh in on a state bill",
    lede="Four ways to tell the Oregon Legislature what you think, and the timing that catches people.",
    body=f"""
  <h2>1. Testify at a public hearing, in person or remotely</h2>
  <ol>
    <li>Find the bill on <a href="{OLIS}" rel="noopener">OLIS</a>, the Legislature's website for bills and committees.</li>
    <li>Once the bill is scheduled for a public hearing, choose <strong>Register to Testify</strong>. You can't register before it's scheduled.</li>
    <li>Choose to testify in person at the Capitol in Salem, or remotely by video or phone. You'll get an email with how to join.</li>
    <li>Register early. Registration closes shortly before the meeting starts.</li>
    <li>Keep it short: who you are, where you live, and how the bill would affect you. Chairs often limit each person to two or three minutes.</li>
  </ol>

  <h2>2. Submit written testimony</h2>
  <p>On the bill's page in OLIS, choose <strong>Submit Testimony</strong>. You can submit from the time a bill is scheduled for a public hearing until <strong>48 hours after the scheduled start of the hearing</strong>. Written testimony counts, and it's a good way to add detail you can't fit into two minutes.</p>
  <p><strong>Everything you submit is public</strong> and searchable online, including your name and anything in the document. Leave out your address, phone number and anything else you don't want posted.</p>

  <h2>3. Contact your own legislators</h2>
  <p>Email or call your senator and representative, especially before a committee vote or floor vote. See <a href="contact-your-representatives.html">how to contact the people who represent you</a>.</p>

  <h2>4. Follow the bill</h2>
  <p>Sign up for <strong>Capitol e-Subscribe</strong> to get email when a bill or a committee agenda changes. The <a href="../legislature.html">Legislature page</a> here shows what each committee is hearing.</p>

  <h2>Timing that catches people</h2>
  <ul>
    <li><strong>Hearings are scheduled on short notice.</strong> Committee agendas often post just a few days ahead.</li>
    <li><strong>Public hearing versus work session.</strong> The public hearing is where you testify. By the work session, the committee is voting, so contact members before it.</li>
    <li><strong>The first-chamber deadline.</strong> Most bills that haven't had a committee vote by a set date early in session are done for the year.</li>
  </ul>
  <p>Questions? The Legislature's information line is 1-800-332-2313.</p>
""",
    sources=[(TESTIFY, "Steps to register to testify and submit testimony (Oregon Legislature)"),
             (TESTIFY_HELP, "Testimony help (OLIS)"),
             (OLIS, "Oregon Legislative Information System (OLIS)")],
)

G["state-initiatives"] = dict(
    cat="State", title="How Oregon's initiatives and referendums work",
    lede="Oregon voters have been writing their own laws since 1902. Here is how a measure gets on the ballot.",
    body=f"""
  <h2>Three ways onto the statewide ballot</h2>
  <ul>
    <li><strong>Initiative:</strong> voters propose a new law or constitutional amendment by petition.</li>
    <li><strong>Referendum:</strong> voters petition to put a law the Legislature just passed on the ballot, so the people can approve or reject it. Laws passed with an emergency clause can't be referred this way.</li>
    <li><strong>Referral:</strong> the Legislature sends a measure to voters itself. Every constitutional amendment the Legislature proposes goes to the voters.</li>
  </ul>

  <h2>How many signatures</h2>
  <p>Signature counts are based on the total votes cast for governor at the last governor's election:</p>
  <ul>
    <li><strong>Initiative to change a law:</strong> 6 percent.</li>
    <li><strong>Initiative to amend the Oregon Constitution:</strong> 8 percent.</li>
    <li><strong>Referendum:</strong> 4 percent.</li>
  </ul>
  <p>The governor's race in November 2026 resets these numbers for the 2028 cycle. The Secretary of State publishes the exact counts.</p>

  <h2>The steps for an initiative</h2>
  <ol>
    <li><strong>File a prospective petition</strong> with the Secretary of State, with the text of the measure.</li>
    <li><strong>Get a ballot title.</strong> The Attorney General writes the short title and summary voters will see. Anyone can comment on the draft, and it can be appealed to the Oregon Supreme Court.</li>
    <li><strong>Gather signatures</strong> from registered Oregon voters, following the state's rules for circulators.</li>
    <li><strong>Turn them in</strong> no later than four months before the November general election, which means early July. County elections officials verify them.</li>
  </ol>

  <h2>What voters get</h2>
  <p>Every household gets a voters' pamphlet with each measure's text, an explanatory statement written by a committee that includes supporters and opponents, an estimate of its cost, and arguments for and against filed by anyone who pays the fee or gathers signatures.</p>
  <p>Oregon also has a <strong>Citizens' Initiative Review</strong>. When it reviews a measure, a panel of randomly chosen voters spends several days hearing from both sides and experts, then writes a statement that goes in the voters' pamphlet. It doesn't review every measure.</p>

  <h2>Local measures</h2>
  <p>Counties, cities and districts have their own initiative and referendum process. For a county, an initiative takes signatures equal to 6 percent of the county's votes for governor, and a referendum 4 percent. Your county elections office can tell you the rules.</p>
""",
    sources=[(SOS_IR, "State initiatives, referendums and referrals (Oregon Secretary of State)"),
             ("https://sos.oregon.gov/elections/Pages/locallaw.aspx", "Local initiatives and referendums (Oregon Secretary of State)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors250.html", "ORS chapter 250, initiative and referendum and the Citizens' Initiative Review")],
)

G["voting-in-oregon"] = dict(
    cat="State", title="Voting in Oregon, including after a conviction",
    lede="Oregon votes by mail. Here is how to register, return your ballot on time, and what the law says about voting with a criminal record.",
    body=f"""
  <h2>Registering</h2>
  <ul>
    <li><strong>Register by 21 days before an election.</strong> You can register online with an Oregon driver's license or ID, or by mail.</li>
    <li><strong>Many people are registered automatically</strong> when they get or renew an Oregon license or ID at the DMV, and get a card in the mail asking which party, if any, they want.</li>
    <li><strong>Update your registration when you move,</strong> so your ballot finds you.</li>
  </ul>

  <h2>Your ballot</h2>
  <p>Every registered voter gets a ballot in the mail about two and a half weeks before each election, along with a voters' pamphlet for state elections.</p>
  <ul>
    <li><strong>Return it at an official drop box</strong> by 8 p.m. on Election Day. This is the surest way.</li>
    <li><strong>Or mail it.</strong> Postage is prepaid. A mailed ballot counts if it's <strong>postmarked by Election Day</strong> and arrives within seven days. Postmarks have been lagging, so the Secretary of State advises mailing your ballot at least a week before Election Day, or asking for a hand postmark at the post office counter.</li>
    <li><strong>Sign the envelope.</strong> Your signature is checked against your registration. If there's a problem, your county will contact you and give you time to fix it.</li>
    <li><strong>Need help or a replacement ballot?</strong> Call your county elections office. Each county also has accessible voting options.</li>
  </ul>

  <h2>Voting with a criminal record</h2>
  <p>Oregon has one of the simpler rules in the country:</p>
  <ul>
    <li><strong>You can't vote only while you're incarcerated for a felony conviction.</strong></li>
    <li><strong>Your right to vote comes back automatically when you're released,</strong> including on parole or post-prison supervision. You do need to register again.</li>
    <li><strong>You can vote</strong> if you're on probation, held in jail before trial, or serving a misdemeanor sentence in jail.</li>
    <li>The same rule applies to federal convictions for Oregon residents.</li>
  </ul>
  <p>If you're helping someone leaving prison, registering to vote can go on the reentry checklist alongside ID and benefits.</p>
""",
    sources=[(VOTE, "Voting and elections (Oregon Secretary of State)"),
             ("https://sos.oregon.gov/elections/Pages/faq.aspx", "Elections FAQ, including the postmark rule (Oregon Secretary of State)"),
             ("https://multco.us/info/voting-rights-oregon-person-convicted-felony-frequently-asked-questions", "Voting rights for people convicted of a felony (Multnomah County Elections)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors137.html", "ORS 137.281, rights during incarceration (Oregon Legislature)")],
)

# ---------------------------------------------------------------- skills

G["two-minute-pitch"] = dict(
    cat="Skills", title="Build a two-minute pitch for your cause",
    lede="Public comment, a hallway conversation with a legislator, a meeting with a commissioner: most chances to make your case last about two minutes. Here is how to use them.",
    body="""
  <h2>The shape of a good pitch</h2>
  <ol>
    <li><strong>Who you are (10 seconds).</strong> Your name, where you live, and why you have a stake: "I'm a parent in Gresham," "I run a small business in Bend."</li>
    <li><strong>The problem (30 seconds).</strong> One clear sentence about what's wrong, then a short, specific example. A real story beats a statistic, and a story with one number beats both.</li>
    <li><strong>The fix (30 seconds).</strong> What you want done, as concretely as you can: a bill number, a budget line, an agenda item, a change to a policy.</li>
    <li><strong>Why it's worth it (30 seconds).</strong> Who benefits, what it costs or saves, and who else supports it.</li>
    <li><strong>The ask (10 seconds).</strong> Say exactly what you want this person to do: vote yes, co-sponsor, meet with you, add it to an agenda.</li>
  </ol>

  <h2>Make it land</h2>
  <ul>
    <li><strong>Know your audience.</strong> What does this person care about? What have they said or voted on before? Connect your issue to that.</li>
    <li><strong>One ask, not five.</strong> Pick the one thing that matters most right now.</li>
    <li><strong>Practice out loud and time it.</strong> Two minutes is about 250 spoken words. Committee chairs often hold testimony to two or three minutes and will cut you off.</li>
    <li><strong>Leave something behind.</strong> A one-page summary with your contact information, or written testimony in the record.</li>
    <li><strong>Follow up.</strong> Send a thank-you within a day, and repeat your ask.</li>
  </ul>

  <h2>Telling your own story</h2>
  <p>If you're speaking from personal experience, share only what you're comfortable having on the public record. Meetings are usually recorded and posted online, the Legislature's hearings stream live, and written testimony to the Legislature is posted where search engines can find it.</p>
""",
    sources=[(TESTIFY, "Steps to register to testify and submit testimony (Oregon Legislature)")],
)

G["read-a-bill-or-agenda"] = dict(
    cat="Skills", title="How to read a bill or a meeting agenda",
    lede="Bill numbers, bold type and brackets, amendments, and the parts of an agenda that tell you when to show up.",
    body="""
  <h2>Oregon bill numbers</h2>
  <ul>
    <li><strong>HB and SB:</strong> House and Senate bills, which become law if passed and signed.</li>
    <li><strong>HJR and SJR:</strong> joint resolutions, used to send constitutional amendments to voters.</li>
    <li><strong>HJM and SJM:</strong> joint memorials, messages to Congress or the federal government.</li>
    <li><strong>HCR and SCR:</strong> concurrent resolutions, often to honor someone or set legislative rules.</li>
    <li><strong>LC:</strong> a legislative concept, the draft of a bill before it's introduced. Interim committees often discuss LCs months before session.</li>
  </ul>

  <h2>Reading the text</h2>
  <ul>
    <li><strong>Bold type is new.</strong> When a bill changes an existing law, words in <strong>boldface</strong> are being added.</li>
    <li><strong>[Italic words in brackets] are being removed.</strong></li>
    <li><strong>Start with the summary</strong> at the top. It's a plain description written by Legislative Counsel, and it's updated as the bill changes.</li>
    <li><strong>Check the version.</strong> "A-Engrossed" means the bill was amended once in committee, "B-Engrossed" twice, and so on. "Enrolled" is the final version that passed both chambers.</li>
    <li><strong>Read the measure analysis.</strong> On OLIS, each bill has a staff measure summary, and fiscal and revenue impact statements that estimate what it costs.</li>
    <li><strong>Amendments</strong> are numbered, like -1 and -2. A committee may adopt one, several or none.</li>
  </ul>

  <h2>Reading a local agenda</h2>
  <ul>
    <li><strong>Consent agenda:</strong> routine items approved together in one vote, with no discussion unless a member pulls an item. Watch it; important things sometimes land here.</li>
    <li><strong>Public hearing:</strong> the item where the public gets to testify. Many hearings are required by law, such as budgets and land use decisions.</li>
    <li><strong>Action item:</strong> the body expects to vote.</li>
    <li><strong>Work session or study session:</strong> discussion with staff, usually without votes or public testimony. It shows where an issue is headed.</li>
    <li><strong>Executive session:</strong> closed to the public for a reason the law allows. No final decisions can be made there.</li>
    <li><strong>The packet:</strong> the staff reports and documents behind each item, usually posted with the agenda. The staff report's recommendation is often what passes.</li>
  </ul>
""",
    sources=[(OLIS, "Oregon Legislative Information System (OLIS)"),
             (PML, "ORS chapter 192, Public Meetings Law (Oregon Legislature)")],
)

G["problem-to-policy"] = dict(
    cat="Problem solving", title="Turning a personal problem into a policy ask",
    lede="Plenty of laws started with one person's bad experience. Here is how to tell whether your problem has a government fix, and how to ask for it.",
    body="""
  <h2>Is it a personal problem or a government one?</h2>
  <p>Ask yourself three questions:</p>
  <ul>
    <li><strong>Is it happening to other people too?</strong> If neighbors, coworkers or people online describe the same thing, it may be a pattern, not bad luck.</li>
    <li><strong>Does a rule cause it, or fail to prevent it?</strong> A fee, a deadline, a missing service, a law that doesn't fit how people live.</li>
    <li><strong>Is a government body responsible for that rule?</strong> If yes, you have someone to ask.</li>
  </ul>

  <h2>Find the right level</h2>
  <ul>
    <li><strong>Start with the agency that runs the program.</strong> Many problems are about how a rule is carried out, not the rule itself, and the agency can fix them.</li>
    <li><strong>If the rule itself is the problem,</strong> find who wrote it: a city council, county board, a district board, Metro, the Legislature, a state agency's rules, or Congress. See <a href="contact-your-representatives.html">how to contact the people who represent you</a>.</li>
    <li><strong>State agency rules have their own comment periods.</strong> Proposed rules are published each month in the Secretary of State's Oregon Bulletin, with a deadline for public comment and often a hearing.</li>
  </ul>

  <h2>Shape the ask</h2>
  <ol>
    <li><strong>Describe the problem in one sentence.</strong></li>
    <li><strong>Show it isn't just you.</strong> Collect a few other stories, and any numbers you can find.</li>
    <li><strong>Propose a specific change.</strong> "Let people renew online," "extend the deadline to 30 days," "add a waiver for people who can't pay." You don't need perfect legal language.</li>
    <li><strong>Find allies.</strong> Nonprofits, unions, business groups, faith communities or neighborhood associations may already be working on it.</li>
    <li><strong>Find a champion.</strong> One elected official who will carry the idea is worth more than ten who agree in passing. In the Legislature, a bill needs a sponsor and a committee chair willing to give it a hearing.</li>
  </ol>

  <h2>Mind the calendar</h2>
  <p>Legislators ask Legislative Counsel to draft their bills in the months before session, and many file them early. The time to bring a legislator an idea is spring through fall of the year before a session, when they're home and planning. Once session starts, deadlines move fast, especially in the 35-day short sessions in even-numbered years.</p>

  <h2>Be ready for a long road</h2>
  <p>Most changes take more than one try. Bills often take several sessions to pass, and local changes may wait for the next budget. Keep a record of each conversation, keep your allies informed, and come back.</p>
  <p>When you're ready to make your case in person, use <a href="two-minute-pitch.html">build a two-minute pitch</a>.</p>
""",
    sources=[("https://sos.oregon.gov/archives/administrative-rules/Pages/publications-reports.aspx", "Oregon Bulletin, proposed state agency rules (Oregon Secretary of State)"),
             (TESTIFY, "Steps to register to testify and submit testimony (Oregon Legislature)")],
)

G["media-literacy"] = dict(
    cat="Skills", title="Media literacy: sorting good information from bad",
    lede="Before you share, argue or show up at a meeting, it's worth knowing whether what you read is true. These habits take a minute and catch most problems.",
    body="""
  <h2>Before you believe it</h2>
  <ul>
    <li><strong>Check the source.</strong> Who published this? Do they have a track record, and do they correct mistakes? An unfamiliar site that looks like a news outlet might not be one.</li>
    <li><strong>Read past the headline.</strong> Headlines are written to get clicks and often overstate what the story says.</li>
    <li><strong>Look for the original.</strong> If a post cites a study, a law or a quote, find the original. Bills, agendas, budgets and court records are usually public.</li>
    <li><strong>Check the date.</strong> Old stories get reshared as if they were new.</li>
    <li><strong>See who else is reporting it.</strong> If a big claim appears in only one place, wait.</li>
  </ul>

  <h2>Watch for these</h2>
  <ul>
    <li><strong>Strong emotion.</strong> Content built to make you angry or afraid spreads fastest. That's a cue to slow down.</li>
    <li><strong>Edited or fake images and video,</strong> including AI-generated ones. Look for odd details, and search for the image to see where it first appeared.</li>
    <li><strong>Missing context.</strong> A real clip or number can mislead when it's cut short.</li>
    <li><strong>Summaries from advocates.</strong> Groups on every side summarize bills and ballot measures. Read the measure's own text and the voters' pamphlet before you trust anyone's description of it.</li>
  </ul>

  <h2>Local news matters</h2>
  <p>Local reporters cover city councils, school boards and county decisions that national outlets never will. Many Oregon communities have lost their local paper or seen it shrink. Supporting the local news you still have, and reading it, is one of the easiest ways to stay informed about decisions close to home.</p>

  <h2>Go to the source on government</h2>
  <p>For local and state decisions, the primary sources are usually online: meeting agendas and recordings, the Legislature's bill pages and live video on OLIS, and agency reports. The <a href="../index.html">calendar</a> links to each meeting's official page. For elections, your county elections office and the Secretary of State are the official word on dates, drop boxes and results.</p>
""",
    sources=[("https://www.newslit.org/", "News Literacy Project"),
             (VOTE, "Voting and elections (Oregon Secretary of State)"),
             (OLIS, "Oregon Legislative Information System (OLIS)")],
)
