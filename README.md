# ModernGov Local Council Data API
All local councils seem to use some software from [moderngov](https://moderngov.com/) to store ward, committee, councillor,
and meeting information. This does have an public API but it doesn't accessible or well documented.

I had a need to lookup some local council data digitally and found it quite difficult.

I wished there was a more easily accessible library available when I needed to query it - so I made one!

I did this for Eastleigh & the whole of Hampshire, but it should work for any council making use of the moderngov software to manage their operation, which seems to be most borough and county councils.

# Install

```shell
pip install moderngov
```

# Example Usage

First find the moderngov website your council uses, its usually called demoracy.(council domain), or meetings.(council domain).  Follow a meetings link
and you will see it. 

Maybe some kind person will compile a list of them and add to this repo. :)


You can use this package in two ways:
## Use the moderngov module
```shell
# Connect
moderngov = api.Website('https://meetings.eastleigh.gov.uk')

# get a committee list
moderngov.committee.list()

# get a ward list
moderngov.wards.list()

# get a councillor list
moderngov.members.list()

# get a councillor by member id
moderngov.members.by_id()
```

## Use the CLI command
The CLI tool doesn't yet support all the options the backend module provides, but still it can be useful for quick lookup.

```shell
# List the registered wards
% moderngov meetings.eastleigh.gov.uk -w
Bishopstoke
Botley
Bursledon and Hound North
Chandler's Ford
Eastleigh Central
Eastleigh North
Eastleigh South
Fair Oak & Horton Heath
Hamble and Netley
Hedge End North
Hedge End South
Hiltingbury
West End North
West End South

# List the council members
% moderngov meetings.eastleigh.gov.uk -m 
1451 Councillor Janice Asman
50000738 Councillor Maud Attrill
50000483 Councillor Tim Bearder
50000737 Councillor Steve Beer
1446 Councillor Paul Bicknell
500000103 Councillor Alex Bourne
174 Councillor Alan Broadhurst
50000683 Councillor Steven Broomfield
50000684 Councillor Anne Buckley
50000203 Councillor Ian Corben
50000282 Councillor Nicholas Couldrey
180 Councillor Tonia Craig
731 Councillor Malcolm Cross
500000114 Councillor Ray Dean
50000731 Councillor Bhavin Dedhia
50000484 Councillor James Duguid
745 Councillor Cynthia Garton
500000119 Councillor Richard Gomer
500000098 Councillor Tim Groves
50000736 Councillor Leigh Hadaway
644 Councillor Steve Holes
197 Councillor Keith House
204 Councillor Wayne Irish
50000739 Councillor Liz Jarvis
50000685 Councillor Dave Kinloch
208 Councillor Rupert Kyrle
50000084 Councillor Darshan Mann
500000092 Councillor Adam Manning
50000482 Councillor Michelle Marsh
50000682 Councillor Tanya Park
500000049 Councillor Louise Parker-Jones
50000082 Councillor David Pragnell
192 Councillor Derek Pretty
50000140 Councillor Jane Rich
50000740 Councillor Cameron Spencer
918 Councillor Bruce Tennent
500000050 Councillor Gin Tidridge
500000108 Councillor Sara Tyson-Payne
173 Councillor Jane Welsh

# List a council member details
% moderngov meetings.eastleigh.gov.uk -M 197
memberid             197   
fullusername         Councillor Keith House
photosmallurl        https://meetings.eastleigh.gov.uk/UserData/7/9/1/Info00000197/smallpic.jpg
photobigurl          https://meetings.eastleigh.gov.uk/UserData/7/9/1/Info00000197/bigpic.jpg
politicalpartytitle  Liberal Democrat
politicalgrouptitle  none  
districttitle        Hamble
representing         none  
keyposts             Leader of the Council; Cabinet Member for Planning and Property

# List the known committees
% moderngov meetings.eastleigh.gov.uk -b
255 Administration Committee
267 Airport Consultative Committee
496 Audit and Resources Committee
432 Audit and Risk Management Committee
249 Bishopstoke, Fair Oak and Horton Heath Local Area Committee
265 Bursledon Windmill Joint Management Committee
250 Bursledon, Hamble-le-Rice and Hound Local Area Committee
254 Cabinet
251 Chandler's Ford and Hiltingbury Local Area Committee
434 Community Wellbeing Scrutiny Panel
276 Council
306 Eastleigh Local Area Committee
264 Eastleigh Museum Joint Management Committee
333 Eastleigh Strategic Partnership
359 Eastleigh Strategic Partnership - Executive
258 Environment & Transport Scrutiny Panel
433 Environment Scrutiny Panel
335 Environmental Health and Control Committee
253 Hedge End, West End and Botley Local Area Committee
336 Highways And Planning Committee
337 Highways And Works Committee
510 Horton Heath Development Management Committee
338 Housing And Health Committee
330 Joint Area Committee
508 Joint Meeting of Policy and Performance Scrutiny Panel and Audit and Resources Committee
427 Joint Meeting of the Scrutiny Panels
339 Leisure Centre Consultative Group
340 Leisure Services Committee
425 Licensed Transport Forum
332 Licensing Committee
356 Licensing Panel
358 Performance Review Scrutiny Panel
262 Places Leisure Eastleigh Consultative Group
341 Planning And Transportation Committee
486 Policy and Performance Scrutiny Panel
342 Policy And Resources Committee
293 Prosperity Scrutiny Panel
343 Recreation And Amenities Committee
259 Resources Scrutiny Panel
436 Scrutiny Management Group
260 Social Policy Scrutiny Panel
257 Special Joint Committee
256 Standards Committee
495 Standards Sub Committee (Third stage)
```

