"""CivicsOR guides, second set (November 2026): courts, the constitution, budgets,
boards and commissions, school boards, neighborhoods, local measures, state
agencies, campaign money, running for office, federal offices, agencies and
budget, and volunteering. Each lists the sources its facts come from."""

G = {}

SOS_ELECT = "https://sos.oregon.gov/elections/Pages/default.aspx"
ORESTAR = "https://secure.sos.state.or.us/orestar/GotoSearchByName.do"
RUN = "https://sos.oregon.gov/elections/Pages/runforoffice.aspx"
COURTS = "https://www.courts.oregon.gov/"
BLUE = "https://sos.oregon.gov/blue-book/Pages/default.aspx"
LFO = "https://www.oregonlegislature.gov/lfo/Pages/default.aspx"
BOARDS = "https://www.oregon.gov/gov/Pages/board-list.aspx"
BULLETIN = "https://sos.oregon.gov/archives/Pages/oregon_administrative_rules.aspx"

G["courts"] = dict(
    cat="State", title="Oregon's courts, and where you fit in",
    lede="Oregon's judges are elected, its courtrooms are open to the public, and jury service is one of the most direct ways to take part.",
    body="""
  <h2>How the courts fit together</h2>
  <ul>
    <li><strong>Circuit courts</strong> are where cases start: felonies and misdemeanors, lawsuits, divorce and custody, juvenile cases, small claims, landlord-tenant cases and more. There's a circuit court in every county, organized into 27 judicial districts.</li>
    <li><strong>The Oregon Tax Court</strong> hears cases about state tax laws, including property taxes.</li>
    <li><strong>The Court of Appeals</strong> hears most appeals from circuit courts and many state agency decisions. It has 13 judges.</li>
    <li><strong>The Oregon Supreme Court</strong> is the state's highest court. Its seven justices choose one of their own as Chief Justice, who also runs the state court system.</li>
    <li><strong>City municipal courts and county justice courts</strong> handle many traffic tickets, violations and some misdemeanors. They're run by local governments, not the state.</li>
  </ul>

  <h2>Judges are elected</h2>
  <p>All of Oregon's state judges, from circuit courts to the Supreme Court, are elected to six-year terms in nonpartisan elections. When a seat opens in the middle of a term, the governor appoints someone to fill it until the next general election, so many judges first reach the bench by appointment. Judicial races are on your May and November ballots; read the voters' pamphlet.</p>

  <h2>Ways to take part</h2>
  <ul>
    <li><strong>Serve on a jury.</strong> If you get a summons, respond. Courts can often reschedule your service if the date doesn't work.</li>
    <li><strong>Watch.</strong> Most hearings and trials are open to the public. Oregon Supreme Court and Court of Appeals arguments are also streamed and recorded online.</li>
    <li><strong>Get help with your own case.</strong> Every courthouse has resources for people without a lawyer, and the Oregon Judicial Department's website has forms and guides. If you're charged with a crime and can't afford a lawyer, ask the court to appoint one.</li>
    <li><strong>Weigh in on the system.</strong> Court budgets, the number of judges and public defense funding are set by the Legislature. See <a href="weigh-in-on-a-state-bill.html">how to weigh in on a state bill</a>.</li>
  </ul>
""",
    sources=[(COURTS, "Oregon Judicial Department"),
             ("https://www.courts.oregon.gov/about/Documents/StateCourtsOverview.pdf", "Oregon's state courts overview (Oregon Judicial Department)"),
             ("https://sos.oregon.gov/blue-book/government/Pages/supreme.aspx", "Oregon Supreme Court (Oregon Blue Book)")],
)

G["constitution"] = dict(
    cat="State", title="The Oregon Constitution",
    lede="Oregon's constitution is older than the state itself, and Oregon voters change it more often than most. Here is what it does and how it changes.",
    body="""
  <h2>What it is</h2>
  <p>Oregon's constitution was approved by voters in 1857 and took effect when Oregon became a state on February 14, 1859. It sets up the Legislature, the governor and other statewide offices, and the courts, and it limits what state and local governments can do.</p>

  <h2>Parts worth knowing</h2>
  <ul>
    <li><strong>Article I, the Bill of Rights.</strong> Free expression, freedom of worship, the rights of people accused of crimes, and more. Oregon courts sometimes read these protections more broadly than the U.S. Constitution's.</li>
    <li><strong>Article IV, the Legislature.</strong> Since 1902, it has also reserved to the people the power to propose laws and amendments by initiative and to refer laws to the ballot by referendum.</li>
    <li><strong>Article XI, local government and taxes.</strong> This is where the property tax limits voters added in the 1990s live, including the rule that property tax measures in elections other than May and November need at least half of registered voters to turn out.</li>
  </ul>

  <h2>How it changes</h2>
  <ul>
    <li><strong>The Legislature can refer an amendment</strong> to the ballot. Voters must approve it.</li>
    <li><strong>Voters can propose an amendment by initiative.</strong> It takes signatures equal to 8 percent of the votes cast for governor at the last election, then a majority of voters. See <a href="state-initiatives.html">how initiatives work</a>.</li>
  </ul>
  <p>Because amending is relatively easy, Oregon's constitution has been changed many times, and some of the most important rules about taxes and elections come from voter initiatives.</p>

  <h2>Read it yourself</h2>
  <p>The Legislature publishes the full current text, and the Oregon Blue Book has a short history.</p>
""",
    sources=[("https://www.oregonlegislature.gov/bills_laws/Pages/OrConst.aspx", "Oregon Constitution (Oregon Legislature)"),
             (BLUE, "Oregon Blue Book (Oregon Secretary of State)"),
             ("https://sos.oregon.gov/elections/Pages/statelaw.aspx", "State initiatives, referendums and referrals (Oregon Secretary of State)")],
)

G["state-budgets"] = dict(
    cat="State", title="How Oregon's budgets are made, and where you can weigh in",
    short="Oregon's budgets and where you can weigh in",
    lede="The state writes a two-year budget, and every city, county, school district and special district writes its own, with members of the public at the table.",
    body="""
  <h2>The state budget</h2>
  <ul>
    <li><strong>Two years at a time.</strong> Oregon budgets for a biennium that runs from July 1 of an odd-numbered year. The Legislature adopts it during the long session.</li>
    <li><strong>How big.</strong> The 2025-27 budget the Legislature adopted in June 2025 totals about $139 billion, of which about $37 billion is General Fund, mostly from the personal income tax. The rest is lottery money, federal funds and fees.</li>
    <li><strong>Where it goes.</strong> Education is the largest use of General Fund and lottery money, followed by human services, public safety and health.</li>
    <li><strong>Who writes it.</strong> The governor proposes a budget in December before the long session. The Joint Committee on Ways and Means and its subcommittees hold hearings on each agency's budget, and the Legislature can adjust it in the short session.</li>
    <li><strong>The kicker.</strong> When personal income tax revenue comes in more than 2 percent above the forecast, the surplus goes back to taxpayers as a credit.</li>
  </ul>

  <h2>Weighing in on the state budget</h2>
  <ul>
    <li>Ways and Means holds public hearings around the state, usually in the spring of the long session. They're on the <a href="../legislature.html">Legislature page</a> when scheduled.</li>
    <li>Testify or send written testimony on an agency's budget bill, just like any other bill.</li>
    <li>Tell your own legislators what matters to you before the budget is final. See <a href="contact-your-representatives.html">how to contact them</a>.</li>
  </ul>

  <h2>Local budgets: a seat for the public</h2>
  <p>Oregon's Local Budget Law gives residents an unusually direct role. Every city, county, school district and special district has a <strong>budget committee</strong> made up of its elected board plus an equal number of residents appointed by that board. All members have an equal vote. The committee reviews the proposed budget in public meetings, takes public comment, and approves a budget before the governing body adopts it, usually in May and June.</p>
  <ul>
    <li><strong>Apply to serve.</strong> Openings for citizen members are posted by each local government, often in winter.</li>
    <li><strong>Comment.</strong> Budget committee meetings are open, and there's a public hearing before the budget is adopted.</li>
  </ul>
""",
    sources=[("https://www.oregonlegislature.gov/lfo/Documents/2025-2%20LAB%20Summary%202025-27.pdf", "2025-27 Legislatively Adopted Budget summary (Legislative Fiscal Office)"),
             (LFO, "Legislative Fiscal Office"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors294.html", "ORS chapter 294, Local Budget Law (Oregon Legislature)")],
)

G["boards-and-commissions"] = dict(
    cat="State", title="Serve on a board or commission",
    lede="Hundreds of public boards in Oregon are made up of residents. You don't need to be an expert to apply, and many seats sit empty for lack of applicants.",
    body=f"""
  <h2>State boards and commissions</h2>
  <p>The governor appoints members to more than 250 state boards and commissions, from licensing boards to the commissions that oversee major agencies. Many seats are set aside for members of the public, or for people from a particular region or background.</p>
  <ul>
    <li><strong>Apply online</strong> through the Governor's Boards and Commissions page. You create an account, search for the board, and apply. Include a résumé and a short statement of interest.</li>
    <li><strong>Some appointments need Senate confirmation.</strong> The Senate Committee on Rules reviews them during Legislative Days and the session, and the public can submit testimony.</li>
    <li><strong>Watch for openings.</strong> The governor's office posts lists of upcoming term expirations.</li>
  </ul>

  <h2>City, county and district boards</h2>
  <p>Cities and counties have their own advisory committees: planning commissions, budget committees, parks boards, library boards, equity and public safety committees, and more. Special districts and school districts have budget committees with resident members too. Look for "boards and commissions" or "volunteer opportunities" on your city or county website.</p>

  <h2>What to expect</h2>
  <ul>
    <li>Most boards meet monthly or less, and their meetings follow Oregon's Public Meetings Law. See <a href="public-meetings-law.html">public meetings</a>.</li>
    <li>Members may need to file an annual statement of economic interest with the Oregon Government Ethics Commission and avoid conflicts of interest.</li>
    <li>Many boards don't pay, but some reimburse expenses or pay a per diem.</li>
  </ul>
""",
    sources=[(BOARDS, "Boards and Commissions (Office of the Governor)"),
             ("https://www.oregon.gov/ogec/Pages/default.aspx", "Oregon Government Ethics Commission"),
             ("https://www.oregonlegislature.gov/OLIS_help/Pages/ExecAppt.aspx", "Executive appointments on OLIS (Oregon Legislature)")],
)

G["your-school-board"] = dict(
    cat="Local", title="Your school board",
    lede="Oregon's school boards are elected in low-turnout May elections, and they decide budgets, curriculum policy and who leads the district.",
    body="""
  <h2>What a school board does</h2>
  <ul>
    <li>Hires and evaluates the superintendent.</li>
    <li>Adopts the budget, with a budget committee that includes an equal number of residents appointed by the board.</li>
    <li>Sets district policy, approves curriculum adoptions and labor contracts, and decides whether to ask voters for bonds or local option levies.</li>
  </ul>
  <p>Day-to-day decisions about a school belong to the principal and district staff, so start there with a problem about one classroom or student.</p>

  <h2>Elections</h2>
  <ul>
    <li>Board members serve four-year terms, elected on a nonpartisan ballot in May of odd-numbered years. About half the seats are up each time.</li>
    <li>The next school board election is <strong>May 18, 2027</strong>. Candidates file with the county elections office. Filing opens February 6, 2027. Board members who were elected and are running again must file by <strong>March 11, 2027</strong>. Everyone else, including board members who were appointed, has until <strong>March 18, 2027</strong>.</li>
    <li>Turnout in these elections is often low, so each vote counts for more.</li>
  </ul>

  <section class="near-you" data-show="schools" data-title="School districts in your county" aria-label="School districts in your county"></section>

  <h2>Taking part</h2>
  <ul>
    <li><strong>Find the meetings.</strong> Boards usually meet once or twice a month. Agendas post a few days ahead, often on BoardDocs or the district's website. Many districts are on the <a href="../index.html">Community Calendar</a>.</li>
    <li><strong>Speak during public comment.</strong> Most boards set aside time and ask you to sign up first. See <a href="speak-at-a-public-meeting.html">how to speak at a public meeting</a>.</li>
    <li><strong>Join the budget committee</strong> or a district advisory committee.</li>
    <li><strong>Run.</strong> You need to be a registered voter living in the district, and some zones have their own residency rules. See <a href="running-for-office.html">running for office</a>.</li>
  </ul>
""",
    sources=[("https://ballotpedia.org/Rules_governing_school_board_election_dates_and_timing_in_Oregon", "School board election dates in Oregon (Ballotpedia)"),
             ("https://sos.oregon.gov/elections/Documents/Candidate-SEL190-Highlighted.pdf", "2027 district election filing dates, form SEL 190 (Oregon Secretary of State)"),
             ("https://apps.oregon.gov/oregon-newsroom/OR/SOS/Posts/Post/candidate-filing-window-opens-today-new-deadlines", "Earlier filing deadline for elected incumbents (Oregon Secretary of State)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors332.html", "ORS chapter 332, local administration of education (Oregon Legislature)"),
             ("https://www.osba.org/", "Oregon School Boards Association")],
)

G["your-neighborhood"] = dict(
    cat="Local", title="Get involved in your neighborhood",
    lede="Oregon's land use system requires every city and county to involve the public. Neighborhood groups are often where that starts.",
    body="""
  <h2>Why Oregon has neighborhood groups</h2>
  <p>The first of Oregon's 19 statewide land use planning goals, Goal 1, requires each city and county to run a citizen involvement program, so residents can take part in every phase of planning. Cities meet it in different ways, and many rely on neighborhood associations or similar groups.</p>

  <h2>What it looks like where you live</h2>
  <ul>
    <li><strong>Portland</strong> has 94 neighborhood associations, grouped into districts with district coalition offices, supported by the Office of Community & Civic Life.</li>
    <li><strong>Washington County</strong> replaced its former Community Participation Organizations (CPOs) in 2026. On January 27, 2026, the county board approved a new program it calls SPARC, Strengthening Participation and Reaching Communities. The county describes it as a district-aligned community engagement program, organized in four areas, one for each county commissioner district.</li>
    <li><strong>Many other cities</strong>, from Eugene and Salem to Beaverton and Bend, recognize neighborhood associations and notify them about land use applications nearby.</li>
  </ul>
  <p>Search your city's website for "neighborhood associations." In rural areas, your county's planning department or a community planning organization is the place to start.</p>

  <h2>What neighborhood groups do</h2>
  <ul>
    <li>Get notice of land use applications and can comment, appear at hearings or appeal decisions.</li>
    <li>Bring up traffic safety, parks, emergency preparedness and other local concerns with the city.</li>
    <li>Run cleanups, events and small grants.</li>
  </ul>

  <section class="near-you" data-show="site" data-title="Your city and county websites" aria-label="Your city and county websites"></section>

  <h2>Getting started</h2>
  <ul>
    <li>Go to a meeting. Anyone who lives, owns property or works in the area can usually take part.</li>
    <li>Watch for land use notices: the signs posted on a property and mailed notices to neighbors. They list the deadline to comment.</li>
    <li>Know your city councilor. See <a href="../reps.html">who represents you</a>.</li>
  </ul>
""",
    sources=[("https://www.oregon.gov/lcd/op/pages/goal-1.aspx", "Goal 1: Citizen Involvement (Department of Land Conservation and Development)"),
             ("https://www.portland.gov/civic/myneighborhood/about-neighborhood-system", "About neighborhood associations and district offices (City of Portland)"),
             ("https://washingtoncountyor.gov/CAO/CPO", "SPARC, which replaced the former CPOs (Washington County)")],
)

G["local-ballot-measures"] = dict(
    cat="Local", title="Local ballot measures: bonds, levies and local laws",
    short="Local ballot measures: bonds, levies and laws",
    lede="Most of what's on an Oregon ballot in May is local: school bonds, fire district levies, library districts. Here is how to read them.",
    body="""
  <h2>The kinds you'll see</h2>
  <ul>
    <li><strong>General obligation bonds</strong> borrow money for buildings and equipment, such as new schools or fire stations. They're repaid by a property tax for a set number of years.</li>
    <li><strong>Local option levies</strong> add a property tax for operations, such as teachers, firefighters or library hours, for up to five years (up to ten for capital projects). Many are renewals of an existing levy.</li>
    <li><strong>New districts</strong> with a permanent tax rate, such as a library or fire district.</li>
    <li><strong>Local laws and charter amendments</strong> referred by a council or commission, or put on the ballot by voters through a local initiative or referendum.</li>
  </ul>

  <h2>Rules that shape them</h2>
  <ul>
    <li><strong>Property tax limits.</strong> Measures 5 and 50 from the 1990s cap property taxes, so many local governments rely on levies and bonds that voters approve.</li>
    <li><strong>Double majority.</strong> A property tax measure on a May or November ballot needs a simple majority. At any other election, at least half of registered voters must also cast a ballot, so most tax measures go on May or November ballots.</li>
  </ul>

  <h2>Reading a measure</h2>
  <ul>
    <li>Your county voters' pamphlet has each measure's ballot title, an explanatory statement, and arguments for and against.</li>
    <li>For a tax measure, look for the estimated rate per $1,000 of assessed value and how long it lasts.</li>
    <li>Ask the district for its plans and past audits, and see how it voted to put the measure on the ballot. The <a href="../index.html">Community Calendar</a> lists the meetings where these decisions are made.</li>
  </ul>

  <h2>Putting a measure on the ballot yourself</h2>
  <p>Counties, cities and districts have their own initiative and referendum process. See <a href="state-initiatives.html">initiatives and referendums</a> and ask your county elections office.</p>
""",
    sources=[("https://www.oregon.gov/DOR/forms/FormsPubs/tax-election-ballot-measures_504-421.pdf", "Tax election ballot measures (Oregon Department of Revenue)"),
             ("https://sos.oregon.gov/elections/Pages/locallaw.aspx", "Local initiatives and referendums (Oregon Secretary of State)"),
             ("https://ballotpedia.org/Oregon_Ballot_Measure_56_(2008)", "Measure 56 (2008), the double majority (Ballotpedia)")],
)

G["state-agencies"] = dict(
    cat="State", title="Working with state agencies and commenting on rules",
    short="State agencies and commenting on rules",
    lede="State agencies write the rules that carry out Oregon's laws, and they have to take public comment first.",
    body=f"""
  <h2>How rules get made</h2>
  <p>When the Legislature passes a law, the agency in charge often writes administrative rules to carry it out. Oregon's Administrative Procedures Act (ORS chapter 183) sets the steps:</p>
  <ul>
    <li><strong>Notice.</strong> The agency publishes a notice of proposed rulemaking in the <strong>Oregon Bulletin</strong>, which comes out on the first business day of each month, at least 21 days before the rule takes effect. The notice explains the need for the rule, its cost and the deadline for comments.</li>
    <li><strong>Comments.</strong> Anyone can send written comments by the deadline.</li>
    <li><strong>Hearings.</strong> An agency holds a public hearing if it chooses to, or if ten or more people, or a group representing ten or more, ask for one in time.</li>
    <li><strong>Advisory committees.</strong> Many agencies form rulemaking advisory committees with members of the public before they propose a rule.</li>
  </ul>

  <h2>Getting notice</h2>
  <ul>
    <li>Each agency must keep a mailing list of people who ask to be told about its rulemaking. Ask its rules coordinator to add you.</li>
    <li>Browse proposed rules in the Oregon Bulletin on the Secretary of State's website.</li>
  </ul>

  <h2>Writing a comment that counts</h2>
  <ul>
    <li>Name the rule and the section you're commenting on.</li>
    <li>Explain how it would affect you, your work or your community, with specifics.</li>
    <li>Suggest a change. Agencies have to respond to the substance of comments, not count them.</li>
  </ul>

  <h2>When you're stuck with an agency</h2>
  <ul>
    <li>Ask the agency's ombudsman or customer service office, if it has one.</li>
    <li>Contact your state senator or representative. Their offices help constituents with state agencies. See <a href="../reps.html">who represents you</a>.</li>
    <li>Ask for records under the Public Records Law. See <a href="public-records-requests.html">public records requests</a>.</li>
  </ul>
""",
    sources=[(BULLETIN, "Oregon Administrative Rules and the Oregon Bulletin (Oregon Secretary of State)"),
             ("https://www.oregonlegislature.gov/bills_laws/ors/ors183.html", "ORS chapter 183, Administrative Procedures Act (Oregon Legislature)"),
             ("https://sos.oregon.gov/archives/administrative-rules/Documents/permanent-rulemaking-overview.pdf", "Permanent rulemaking overview (Oregon Secretary of State)")],
)

G["campaign-finance"] = dict(
    cat="State", title="Follow the money in Oregon campaigns",
    desc="Every Oregon campaign reports its money to the Secretary of State, and anyone can look it up. Oregon limits contributions for the first time in 2027.",
    lede="Every Oregon candidate and campaign reports its money to the Secretary of State, and anyone can look it up. Starting in 2027, Oregon also limits contributions for the first time.",
    body=f"""
  <h2>Look it up in ORESTAR</h2>
  <p>ORESTAR is the Secretary of State's campaign finance system. Candidates and political committees file their contributions and expenditures there, for state and local races alike, wherever the candidate filed to run.</p>
  <ul>
    <li>Search by candidate or committee name to see who gave, how much and when, and how the money was spent.</li>
    <li>Search by contributor to see where a person or business has given.</li>
    <li>Oregon uses continuous reporting, so transactions show up throughout the campaign, not just at a few deadlines.</li>
  </ul>

  <h2>Contribution limits start in 2027</h2>
  <p>For most of its history Oregon had no limits on campaign contributions. House Bill 4024 (2024) sets limits on contributions to candidates and committees, with enforcement starting <strong>January 1, 2027</strong>, and adds new disclosure requirements in later years. House Bill 4018 (2026) changed parts of HB 4024. Starting at the end of 2028, the Secretary of State adjusts the limits for the cost of living every two years. HB 4018 also moved the deadline for the state's web-based campaign finance dashboard to January 1, 2032. Local governments can set lower limits for their own elections, and some, like Portland and Multnomah County, already have them. The Secretary of State's Campaign Finance Manual has the current amounts.</p>

  <h2>Other places to look</h2>
  <ul>
    <li><strong>Federal races</strong> (Congress and President) report to the Federal Election Commission at fec.gov, not ORESTAR.</li>
    <li><strong>Lobbying</strong> at the Legislature is registered and reported to the Oregon Government Ethics Commission.</li>
    <li><strong>Officials' finances.</strong> Many public officials file annual statements of economic interest with the Ethics Commission.</li>
  </ul>

  <h2>If you see a problem</h2>
  <p>You can file a complaint about a possible campaign finance violation with the Secretary of State's Elections Division.</p>
""",
    sources=[(ORESTAR, "ORESTAR campaign finance search (Oregon Secretary of State)"),
             ("https://sos.oregon.gov/elections/Pages/campaign-finance-legislation.aspx", "Campaign finance legislation, HB 4024 (Oregon Secretary of State)"),
             ("https://olis.oregonlegislature.gov/liz/2026R1/Measures/Overview/HB4018", "HB 4018 (2026), changes to the campaign finance law (Oregon Legislature)"),
             ("https://www.oregon.gov/ogec/Pages/default.aspx", "Oregon Government Ethics Commission"),
             ("https://www.fec.gov/", "Federal Election Commission")],
)

G["running-for-office"] = dict(
    cat="State", title="Running for office in Oregon",
    lede="Thousands of Oregon offices are on the ballot every two years, many with no one running. Here is how to file.",
    body=f"""
  <h2>Which office, and when</h2>
  <ul>
    <li><strong>State, county and city offices</strong> and Congress: the primary is in May of even-numbered years and the general election is in November. Partisan offices have party primaries; nonpartisan offices, such as judges and most county and city offices, may be decided in May if a candidate wins a majority.</li>
    <li><strong>School boards and special districts</strong> (fire, water, parks, ports, community colleges and more): elected in May of odd-numbered years. The next one is May 18, 2027.</li>
  </ul>

  <h2>How to file</h2>
  <ul>
    <li><strong>Check the qualifications</strong> in the Secretary of State's candidate manuals: usually being a registered voter who lives in the district, sometimes for a set time. A partisan candidate must have been registered with the party 180 days before the filing deadline.</li>
    <li><strong>File with the right office.</strong> State and federal candidates file with the Secretary of State, online through ORESTAR. County, city and district candidates file with the county elections office or city recorder.</li>
    <li><strong>Pay the filing fee or gather signatures</strong> instead. Many local offices have no fee.</li>
    <li><strong>Watch the deadline.</strong> For the May 2026 primary, filing opened in September 2025 and closed in March 2026. Since 2026, elected incumbents running again must file a week earlier than everyone else; appointed incumbents use the regular deadline.</li>
  </ul>

  <h2>Money</h2>
  <ul>
    <li>Most candidates must set up a candidate committee and report contributions and spending in ORESTAR. See <a href="campaign-finance.html">follow the money</a>.</li>
    <li>New contribution limits start January 1, 2027.</li>
  </ul>

  <h2>Getting on the voters' pamphlet</h2>
  <p>Candidates can file a statement and photo for the voters' pamphlet by paying a fee or gathering signatures, by a deadline after the filing deadline.</p>
""",
    sources=[(RUN, "Run for office (Oregon Secretary of State)"),
             ("https://sos.oregon.gov/elections/Documents/statecandidates.pdf", "State Candidate Manual (Oregon Secretary of State)"),
             ("https://apps.oregon.gov/oregon-newsroom/OR/SOS/Posts/Post/candidate-filing-window-opens-today-new-deadlines", "New filing deadlines for incumbents (Oregon Secretary of State)")],
)

G["federal-offices"] = dict(
    cat="Federal", title="Federal elections and who can run",
    lede="Oregon sends eight people to Congress and helps elect a President. Here is who can run for each office and how often.",
    body="""
  <h2>The offices</h2>
  <ul>
    <li><strong>U.S. House of Representatives.</strong> Oregon has six House members, each elected from a congressional district for a two-year term. Every seat is on the ballot in every even-numbered year.</li>
    <li><strong>U.S. Senate.</strong> Oregon has two senators, elected statewide for six-year terms. Their terms are staggered, so the seats come up in different years.</li>
    <li><strong>President and Vice President.</strong> Elected every four years. Oregon's electoral votes go to the ticket that wins the state's popular vote.</li>
  </ul>

  <h2>Who can run (set by the U.S. Constitution)</h2>
  <ul>
    <li><strong>House:</strong> at least 25 years old, a U.S. citizen for at least seven years, and a resident of the state. Members don't have to live in the district they represent.</li>
    <li><strong>Senate:</strong> at least 30 years old, a U.S. citizen for at least nine years, and a resident of the state.</li>
    <li><strong>President:</strong> at least 35 years old, a natural-born citizen, and a U.S. resident for at least 14 years. No one can be elected President more than twice.</li>
  </ul>

  <h2>How Oregon runs these elections</h2>
  <ul>
    <li>House and Senate nominees are chosen in Oregon's May primary. Major parties' primaries are closed: only voters registered with the party get its ballot. Nonaffiliated voters can still vote on nonpartisan races and measures.</li>
    <li>Oregon's presidential primary is held at the same time, in May of presidential election years.</li>
    <li>Candidates for Congress file with the Secretary of State and report campaign money to the Federal Election Commission.</li>
  </ul>

  <h2>How to follow your members</h2>
  <ul>
    <li>Find them with <a href="../reps.html">Who represents you</a>.</li>
    <li>Track their votes and bills on Congress.gov.</li>
    <li>See who funds their campaigns at fec.gov.</li>
  </ul>
""",
    sources=[("https://constitution.congress.gov/constitution/", "The Constitution of the United States (Congress.gov)"),
             ("https://www.congress.gov/", "Congress.gov"),
             ("https://www.fec.gov/", "Federal Election Commission"),
             ("https://sos.oregon.gov/voting-elections/Pages/default.aspx", "Voting and elections (Oregon Secretary of State)")],
)

G["federal-agencies"] = dict(
    cat="Federal", title="Working with federal agencies",
    desc="Federal agencies manage more than half of Oregon's land and run programs many Oregonians rely on. Here is how to get through when one affects you.",
    lede="Federal agencies manage more than half the land in Oregon and run programs millions of Oregonians rely on. When one is stuck, slow or about to change a rule that affects you, there are ways through.",
    body="""
  <h2>When you're stuck with an agency</h2>
  <p>Ask your member of Congress for help. Every House and Senate office has caseworkers who help constituents with federal agencies, including Social Security, Medicare, veterans' benefits, the IRS, passports and immigration cases.</p>
  <ul>
    <li>Call or fill out the office's online form. Find your members with <a href="../reps.html">Who represents you</a>.</li>
    <li>Expect to sign a privacy release, which lets the agency share your case with the office.</li>
    <li>Bring case numbers and copies of letters.</li>
  </ul>

  <h2>Public lands</h2>
  <p>The U.S. Forest Service and the Bureau of Land Management manage much of Oregon's forests and rangeland. Before big decisions, such as forest plans, timber sales, grazing permits and travel management, they usually take public comment under the National Environmental Policy Act. Sign up for the project lists of your local national forest or BLM district to hear about them.</p>

  <h2>Comment on a proposed rule</h2>
  <ul>
    <li>Find proposed rules in the Federal Register.</li>
    <li>Comment on Regulations.gov before the deadline.</li>
    <li>Be specific. Agencies have to consider the substance of comments, not count them. Explain how the rule would affect you, and suggest a change.</li>
  </ul>

  <h2>Request records</h2>
  <p>The Freedom of Information Act lets anyone request records from federal agencies. FOIA.gov explains how and links to each agency's request page.</p>

  <h2>Report a problem</h2>
  <p>Most agencies have an Inspector General who investigates fraud, waste and abuse and takes tips from the public, and many have an ombudsman who helps resolve complaints.</p>
""",
    sources=[("https://www.regulations.gov/", "Regulations.gov"),
             ("https://www.federalregister.gov/", "Federal Register"),
             ("https://www.foia.gov/", "FOIA.gov"),
             ("https://www.fs.usda.gov/r06", "Pacific Northwest Region (U.S. Forest Service)")],
)

G["federal-budget"] = dict(
    cat="Federal", title="The federal budget and where you can weigh in",
    desc="Federal money pays for much of Oregon's state budget, from health coverage to highways. How the federal budget gets made and where public input fits.",
    lede="Federal money pays for much of what Oregon's state budget does, from health coverage to highways. Here is how the federal budget gets made and where public input fits.",
    body="""
  <h2>Two kinds of spending</h2>
  <ul>
    <li><strong>Mandatory spending</strong> is set by existing law and doesn't need a vote each year. It includes Social Security, Medicare and most of Medicaid. It is the larger share.</li>
    <li><strong>Discretionary spending</strong> is decided each year by Congress through appropriations bills. It covers defense and most federal agencies, grants and programs.</li>
  </ul>

  <h2>The yearly cycle</h2>
  <ul>
    <li>The federal fiscal year runs from October 1 to September 30.</li>
    <li>Early in the year, the President sends Congress a budget request. It is a proposal, not law.</li>
    <li>In spring and summer, House and Senate appropriations subcommittees write the annual spending bills, usually 12 of them.</li>
    <li>By October 1, Congress is supposed to pass them. When it doesn't, it usually passes a continuing resolution. If neither passes, parts of the government shut down.</li>
  </ul>

  <h2>Where you can weigh in</h2>
  <ul>
    <li><strong>Contact your members of Congress</strong> about programs you care about, especially in the spring while appropriations bills are written.</li>
    <li><strong>Community projects.</strong> Members of Congress can request funding for specific projects in their district or state. Local governments, nonprofits and tribes ask their members, usually in late winter or early spring.</li>
    <li><strong>The state budget matters too.</strong> Federal funds make up close to a third of Oregon's state budget. See <a href="state-budgets.html">Oregon's budgets</a>.</li>
  </ul>

  <h2>Following the money</h2>
  <p>The Congressional Budget Office publishes plain-language overviews of the budget, and USAspending.gov shows where federal money goes, down to the county.</p>
""",
    sources=[("https://www.cbo.gov/topics/budget", "The federal budget (Congressional Budget Office)"),
             ("https://www.usaspending.gov/", "USAspending.gov"),
             ("https://www.congress.gov/", "Congress.gov"),
             ("https://www.oregonlegislature.gov/lfo/Documents/2025-2%20LAB%20Summary%202025-27.pdf", "2025-27 Legislatively Adopted Budget summary (Legislative Fiscal Office)")],
)

G["volunteer-and-public-service"] = dict(
    cat="Everyday", title="Volunteering and public service jobs",
    lede="Some of the most direct ways to take part don't involve a vote at all. Here is how to find volunteer roles and public jobs in Oregon.",
    body="""
  <h2>Volunteer</h2>
  <ul>
    <li><strong>OregonServes</strong>, the state's service commission, supports AmeriCorps programs across Oregon and promotes volunteering and civic engagement.</li>
    <li><strong>Local governments</strong> use volunteers in parks, libraries, senior centers and emergency preparedness programs, including Community Emergency Response Teams. Check your city or county website.</li>
    <li><strong>Elections.</strong> County elections offices hire temporary workers and welcome observers around each election.</li>
    <li><strong>Boards and committees</strong> are volunteer service too. See <a href="boards-and-commissions.html">serve on a board or commission</a>.</li>
  </ul>

  <h2>Give wisely</h2>
  <ul>
    <li>Check a charity before you give. The Oregon Department of Justice's Charitable Activities Section keeps a searchable registry of charities with their financial reports.</li>
    <li>Small community groups often do the most with the least.</li>
  </ul>

  <h2>Public service jobs</h2>
  <ul>
    <li><strong>State jobs</strong> are posted on the State of Oregon's jobs site.</li>
    <li><strong>Federal jobs</strong> are posted on USAJOBS.</li>
    <li><strong>City, county, school district and special district jobs</strong> are posted on each government's own website.</li>
    <li><strong>Internships</strong> are offered by the Legislature, state agencies and many local governments.</li>
  </ul>
  <p>Public jobs range from engineers and nurses to planners, mechanics, analysts and clerks, and many qualify for the federal Public Service Loan Forgiveness program.</p>
""",
    sources=[("https://www.oregon.gov/oregonserves/Pages/default.aspx", "OregonServes"),
             ("https://www.oregon.gov/jobs/Pages/default.aspx", "State of Oregon jobs"),
             ("https://www.usajobs.gov/", "USAJOBS"),
             ("https://www.doj.state.or.us/charities/", "Charitable Activities (Oregon Department of Justice)")],
)
