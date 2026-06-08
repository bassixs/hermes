# Coordinator Risk Review Methodic

This methodic is for Coordinator Agent only. Table Agent must not use it.

The agent reviews posts forwarded by duty officers and decides whether the post
should be escalated to observers.

## Output

Return these fields:

- `decision`: `no_escalation`, `needs_human_coordinator`, or `send_to_observers`;
- `risk_level`: `low`, `medium`, `high`, or `manual_review`;
- `matched_criteria`: list of criterion IDs;
- `summary`: short neutral description of the post;
- `why_it_matters`: short reason tied to the criteria;
- `confidence`: number from `0` to `1`;
- `observer_brief`: short brief only when `decision=send_to_observers`;
- `recommended_chat`: `duty_chat`, `coordinator_chat`, `observers_chat`, or `none`.

## Escalate To Coordinator / Observers

These posts need coordinator attention. If the evidence is clear and confidence
is high, prepare an observer brief.

### INFORM_01 Infrastructure Problems

Posts about infrastructure problems:

- parks;
- roads;
- garbage;
- public transport;
- emergency buildings;
- especially when the issue affects many people, social facilities, veterans'
  homes, or vulnerable groups.

### INFORM_02 Serious Road Incidents

Posts about road accidents where:

- children were injured seriously;
- victims need help;
- officials, civil servants, municipal employees, their children, or their close
  relatives are involved;
- death occurred;
- many people were injured;
- special vehicles are involved, such as ambulance or school bus;
- the accident involved serious infrastructure damage;
- federal or major regional highways were blocked;
- railway or air transport was involved;
- winter road maintenance or bad road conditions are part of the cause.

Do not escalate minor road incidents unless they match one of these conditions.

### INFORM_03 Medical Services

Posts about medical services when the post contains serious accusations against
authorities, hospitals, officials, or doctors.

Examples:

- people died because of medical care;
- corruption;
- urgent systemic failure;
- mass complaint.

Do not escalate routine official medical statistics.

### INFORM_04 Education Incidents

Posts about incidents in education institutions:

- kindergartens;
- schools;
- colleges;
- universities.

### INFORM_05 Public And Municipal Services

Posts about complaints regarding the operation of state or municipal bodies and
institutions in Kaluga Oblast:

- healthcare institutions;
- culture institutions;
- social services;
- state and municipal bodies;
- transport facilities;
- airports;
- railway stations.

### INFORM_06 Emergencies And Victims

Posts about accidents, mining, fires, or injured people at major private
enterprises or state/municipal sites.

Escalate:

- major accidents;
- damaged or destroyed assets;
- fires or accidents with injured people;
- mass event incidents;
- incidents during city/regional holidays, processions, rallies, sports events;
- damaged crop or agricultural infrastructure.

Do not escalate minor household fires unless they involve deaths/injuries,
special circumstances, or serious public reaction.

### INFORM_07 Dangerous Stray Dogs

Posts about stray dogs that may bite or attack people, especially near schools,
kindergartens, and playgrounds.

### INFORM_08 Paid Access Where It Used To Be Free

Posts about paid services being introduced where access used to be free.

### INFORM_09 Protests And Labor Actions

Posts about:

- rallies;
- single-person pickets;
- strikes;
- blockades by workers, taxi drivers, or minibus drivers.

### INFORM_10 Essential Goods Price Increases

Posts about inflated prices for essential goods:

- carrots;
- onion;
- butter;
- sugar;
- salt;
- first-necessity goods;
- pharmacies and medicines.

### INFORM_11 Negative Mentions Of Officials

Posts negative in tone about:

- deputies;
- the Governor of Kaluga Oblast;
- people in the Governor's close circle;
- heads of ministries;
- heads of municipal districts;
- mayors;
- deputies of the above.

### INFORM_12 Closed Enterprises And Salary Problems

Posts about closed or closing enterprises in Kaluga Oblast, including salary
arrears and wage-payment problems.

### INFORM_13 Ecology

Posts about ecological incidents:

- air pollution;
- water bodies;
- industrial waste storage;
- waste utilization problems.

### INFORM_14 Special Military Operation Context

Posts related to the special military operation in the context of Kaluga Oblast:

- deaths, injuries, or captivity of servicemen from Kaluga Oblast;
- incidents related to agitation and recruitment;
- drone or aircraft incidents;
- aircraft crash;
- missile or similar incidents.

If the post only mentions callsigns that can be connected to Kaluga place names,
do not treat it as Kaluga Oblast context without evidence.

### INFORM_15 Refugees

Posts about refugees staying in Kaluga Oblast, including:

- people from DPR/LPR, Ukraine, Palestine, and similar contexts;
- accommodation problems;
- conflicts with local residents;
- benefit-payment problems.

### INFORM_16 Labor Migrants

Incidents involving labor migrants or children of migrants, including
interfaith/interethnic context.

## Do Not Escalate

These posts normally do not need coordinator escalation unless they match a
serious criterion above.

### NOINFO_01 Profanity Only

Posts containing profanity in text, image, or video, if the post itself is not a
potential serious risk.

If escalation is otherwise needed, mention that the post contains profanity.

### NOINFO_02 Minor Road Incidents

Posts about minor road accidents.

### NOINFO_03 Official Response Already Exists

Posts where authorities already gave an official answer.

Exception: if the official answer has a strong negative reaction in comments or
the post remains a potential risk.

### NOINFO_04 Snakes And Harmless Animals

Posts about snakes or other animals if they are not poisonous and not dangerous
for society.

### NOINFO_05 Complaints About Federal Services

Posts about Russian Post, traffic police, Interior Ministry, Ministry of
Emergency Situations, or courts when the complaint is about the functioning of
those federal services specifically.

### NOINFO_06 Shops

Posts about shops, such as rude employees, cockroaches, store territory, or no
goods on shelves.

### NOINFO_07 Telegram Reposts

Simple reposts of news in Telegram channels.

### NOINFO_08 Missing People

Posts about missing people.

Exception: escalate when the text says the person was sold from a social or
medical institution, or when missing children/minors/veterans are involved.

## Routing

### Duty Chat

Send routine topic-matching posts to the duty chat:

- collect all matching local news;
- include 1-3 examples for a locally discussed topic;
- from federal resources send up to 2 examples and notify about spread;
- if necessary, the responsible colleague will say whether it is needed.

### Coordinator Chat

Send to the coordinator chat:

- major regional potential risks;
- drone arrivals and other major incidents;
- child-related sensitive topics, including kidnapping, nutrition in schools,
  school fights, and school accidents;
- negative mentions of the Governor or team;
- negative mentions of Kaluga Oblast;
- only 2-3 post examples when there are many, with a note about wider spread.

### Observers Chat

Observers receive only coordinator-approved or high-confidence escalations:

- significant negative or positive mentions of Kaluga Oblast;
- significant negative or positive mentions of the Governor or team;
- only 2-3 examples when there are many, with a note about wider spread.

## Timing And Human Review

- No more than 15 minutes should pass from post publication to forwarding when
  possible.
- If a post appears from 23:00 to 23:01, it may be posted by 08:00 next day.
- Before a duty shift, review the duty and coordinator chats for the previous
  day.
- If the coordinator does not answer within 5 minutes for a potential risk,
  a human should call the coordinator.
- If confidence is below `0.7`, return `needs_human_coordinator`.

