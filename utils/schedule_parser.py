import json
import re

from utils.data_utils import read_from_json

# Sample data as a string, each line represents an event
data = { "24-July":
"""
Football
Football
Multiple Venues
18:30
Men's Group C
Parc des Princes
UZB flag
Uzbekistan
-
Spain
ESP flag
18:30
Men's Group B
Geoffroy-Guichard Stadium
ARG flag
Argentina
-
Morocco
MAR flag
20:30
Men's Group C
La Beaujoire Stadium
EGY flag
Egypt
-
Dominican Republic
DOM flag
20:30
Men's Group A
Nice Stadium
GUI flag
Guinea
-
New Zealand
NZL flag
22:30
Men's Group D
Bordeaux Stadium
JPN flag
Japan
-
Paraguay
PAR flag
22:30
Men's Group B
Lyon Stadium
IRQ flag
Iraq
-
Ukraine
UKR flag
Rugby Sevens
Rugby Sevens
Stade de France
19:00
Preliminary Phase
19:30
Preliminary Phase
20:00
Preliminary Phase
20:30
Preliminary Phase
21:00
Preliminary Phase
21:30
Preliminary Phase
22:30
Preliminary Phase
23:00
Preliminary Phase
23:30
Preliminary Phase
""",

"25-July":
"""
Archery
Archery
Invalides
13:00
Women's Individual Ranking Round
17:45
Men's Individual Ranking Round
Football
Football
Multiple Venues
00:30
Men's Group D
Parc des Princes
MLI flag
Mali
-
Israel
ISR flag
00:30
Men's Group A
Marseille Stadium
FRA flag
France
-
United States
USA flag
20:30
Women's Group C
La Beaujoire Stadium
ESP flag
Spain
-
Japan
JPN flag
20:30
Women's Group A
Geoffroy-Guichard Stadium
CAN flag
Canada
-
New Zealand
NZL flag
22:30
Women's Group C
Bordeaux Stadium
NGR flag
Nigeria
-
Brazil
BRA flag
22:30
Women's Group B
Marseille Stadium
GER flag
Germany
-
Australia
AUS flag
Handball
Handball
South Paris Arena 6
12:30
Women's Preliminary Round Group A
SLO flag
Slovenia
-
Denmark
DEN flag
14:30
Women's Preliminary Round Group B
NED flag
Netherlands
-
Angola
ANG flag
17:30
Women's Preliminary Round Group B
ESP flag
Spain
-
Brazil
BRA flag
19:30
Women's Preliminary Round Group A
GER flag
Germany
-
Korea
KOR flag
22:30
Women's Preliminary Round Group B
HUN flag
Hungary
-
France
FRA flag
Rugby Sevens
Rugby Sevens
Stade de France
00:00
Preliminary Phase
00:30
Preliminary Phase
01:00
Preliminary Phase
17:30
Preliminary Phase
18:00
Preliminary Phase
18:30
Preliminary Phase
19:00
Preliminary Phase
19:30
Preliminary Phase
20:00
Preliminary Phase
23:30
Men's Placing 9-12
""",

"26-July":
"""
Football
Football
Multiple Venues
00:30
Women's Group A
Lyon Stadium
FRA flag
France
-
Colombia
COL flag
00:30
Women's Group B
Nice Stadium
USA flag
United States
-
Zambia
ZAM flag
Handball
Handball
South Paris Arena 6
00:30
Women's Preliminary Round Group A
NOR flag
Norway
-
Sweden
SWE flag
Rugby Sevens
Rugby Sevens
Stade de France
00:00
Men's Placing 9-12
00:30
Men's Quarter-final
01:00
Men's Quarter-final
01:30
Men's Quarter-final
02:00
Men's Quarter-final
""",

"27-July":
"""
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
14:30
Men's Qualification - Subdivision 1
19:00
Men's Qualification - Subdivision 2
23:30
Men's Qualification - Subdivision 3
Badminton
Badminton
La Chapelle Arena
12:00
Mixed Doubles Group play stage
12:00
Mixed Doubles Group play stage
12:00
Mixed Doubles Group play stage
12:50
Mixed Doubles Group play stage
12:50
Women's Singles Group play stage
12:50
Women's Singles Group play stage
13:40
Men's Doubles Group play stage
13:40
Men's Doubles Group play stage
13:40
Women's Doubles Group play stage
14:30
Women's Doubles Group play stage
14:30
Men's Singles Group play stage
14:30
Men's Singles Group play stage
17:30
Mixed Doubles Group play stage
17:30
Mixed Doubles Group play stage
17:30
Mixed Doubles Group play stage
18:20
Mixed Doubles Group play stage
18:20
Women's Singles Group play stage
18:20
Women's Singles Group play stage
19:10
Men's Doubles Group play stage
19:10
Men's Doubles Group play stage
19:10
Women's Doubles Group play stage
20:00
Women's Doubles Group play stage
20:00
Men's Doubles Group play stage
20:00
Men's Singles Group play stage
23:00
Women's Singles Group play stage
23:00
Women's Singles Group play stage
23:00
Men's Doubles Group play stage
23:50
Men's Doubles Group play stage
23:50
Men's Doubles Group play stage
23:50
Men's Doubles Group play stage
Basketball
Basketball
Pierre Mauroy Stadium
14:30
Men's Group Phase - Group A
AUS flag
Australia
-
Winner OQT ESP
BK2 flag
17:00
Men's Group Phase - Group B
GER flag
Germany
-
Japan
JPN flag
20:45
Men's Group Phase - Group B
FRA flag
France
-
Winner OQT LAT
BK3 flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
17:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
21:30
Men's or Women's Preliminary Match
22:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
19:00
Women's 54kg - Prelims - Round of 32
19:48
Women's 60kg - Prelims - Round of 32
20:36
Men's 63.5kg - Prelims - Round of 32
21:08
Men's 80kg - Prelims - Round of 32
23:30
Women's 54kg - Prelims - Round of 32
Canoe Slalom
Canoe Slalom
Nautical St - White water
18:30
Men's Canoe Single Heats 1st Run
19:20
Women's Kayak Single Heats 1st Run
20:40
Men's Canoe Single Heats 2nd Run
21:30
Women's Kayak Single Heats 2nd Run
Cycling Road
Cycling Road
Pont Alexandre III
18:00
Women's Individual Time Trial
20:04
Men's Individual Time Trial
Diving
Diving
Aquatics Centre
14:30
Women's Synchronised 3m Springboard Fnl
Equestrian
Equestrian
Château de Versailles
13:00
Eventing Team Dressage
13:00
Eventing Individual Dressage
Fencing
Fencing
Grand Palais
13:30
Women's Épée Individual Table of 64
13:55
Men's Sabre Individual Table of 64
14:20
Women's Épée Individual Table of 32
16:00
Men's Sabre Individual Table of 32
17:40
Women's Épée Individual Table of 16
18:30
Men's Sabre Individual Table of 16
19:20
Women's Épée Individual Table of 8
19:45
Men's Sabre Individual Table of 8
22:30
Women's Épée Individual Semifinal 1
22:55
Women's Épée Individual Semifinal 2
23:20
Men's Sabre Individual Semifinal 1
23:45
Men's Sabre Individual Semifinal 2
Football
Football
Multiple Venues
18:30
Men's Group C
Bordeaux Stadium
DOM flag
Dominican Republic
-
Spain
ESP flag
18:30
Men's Group B
Lyon Stadium
ARG flag
Argentina
-
Iraq
IRQ flag
20:30
Men's Group C
La Beaujoire Stadium
UZB flag
Uzbekistan
-
Egypt
EGY flag
20:30
Men's Group B
Geoffroy-Guichard Stadium
UKR flag
Ukraine
-
Morocco
MAR flag
22:30
Men's Group A
Marseille Stadium
NZL flag
New Zealand
-
United States
USA flag
22:30
Men's Group D
Parc des Princes
ISR flag
Israel
-
Paraguay
PAR flag
Handball
Handball
South Paris Arena 6
12:30
Men's Preliminary Round Group A
ESP flag
Spain
-
Slovenia
SLO flag
14:30
Men's Preliminary Round Group B
HUN flag
Hungary
-
Egypt
EGY flag
17:30
Men's Preliminary Round Group A
CRO flag
Croatia
-
Japan
JPN flag
19:30
Men's Preliminary Round Group B
NOR flag
Norway
-
Argentina
ARG flag
22:30
Men's Preliminary Round Group A
GER flag
Germany
-
Sweden
SWE flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Men's Pool A
GBR flag
Great Britain
-
Spain
ESP flag
14:00
Men's Pool B
BEL flag
Belgium
-
Ireland
IRL flag
16:15
Men's Pool A
NED flag
Netherlands
-
South Africa
RSA flag
16:45
Men's Pool B
AUS flag
Australia
-
Argentina
ARG flag
20:30
Men's Pool A
GER flag
Germany
-
France
FRA flag
21:00
Men's Pool B
IND flag
India
-
New Zealand
NZL flag
23:15
Women's Pool B
ARG flag
Argentina
-
United States
USA flag
23:45
Women's Pool A
NED flag
Netherlands
-
France
FRA flag
Judo
Judo
Champ-de-Mars Arena
13:30
Women -48 kg Elimination Round of 64
13:30
Men -60 kg Elimination Round of 64
13:58
Women -48 kg Elimination Round of 32
13:58
Men -60 kg Elimination Round of 32
15:50
Women -48 kg Elimination Round of 16
15:50
Men -60 kg Elimination Round of 16
16:46
Women -48 kg Quarterfinals
16:46
Men -60 kg Quarterfinals
19:30
Women -48 kg Repechage
19:47
Women -48 kg Semifinals
20:04
Men -60 kg Repechage
20:21
Men -60 kg Semifinals
20:48
Women -48 kg Contest for Bronze Medal A
20:58
Women -48 kg Contest for Bronze Medal B
21:08
Women -48 kg Final
21:19
Men -60 kg Contest for Bronze Medal A
21:29
Men -60 kg Contest for Bronze Medal B
21:39
Men -60 kg Final
Rowing
Rowing
Nautical St - Flat water
12:30
Men's Single Sculls Heats
13:42
Women's Single Sculls Heats
15:00
Men's Double Sculls Heats
15:30
Women's Double Sculls Heats
16:00
Men's Quad. Sculls Heats
16:20
Women's Quad. Sculls Heats
Rugby Sevens
Rugby Sevens
Stade de France
18:00
Men's Placing 5-8
18:30
Men's Placing 5-8
19:00
Men's Semi-final
19:30
Men's Semi-final
20:00
Men's Placing 11-12
20:30
Men's Placing 9-10
21:30
Men's Placing 7-8
22:00
Men's Placing 5-6
22:30
Men's Bronze Medal Match
23:15
Men's Gold Medal Match
Shooting
Shooting
Chateauroux Shooting Ctr
12:30
10m Air Rifle Mixed Team Qualification
14:00
10m Air Rifle Mixed Team Bronze Medal
14:00
10m Air Pistol Men's Qualification
14:30
10m Air Rifle Mixed Team Gold Medal
16:00
10m Air Pistol Women's Qualification
Skateboarding
Skateboarding
La Concorde 3
15:30
Men's Street Prelims
20:30
Men's Street Final
Surfing
Surfing
Teahupo'o, Tahiti
22:30
Men's Round 1
Swimming
Swimming
Paris La Defense Arena
14:30
Women's 100m Butterfly - Heats
14:30
Women's 400m Freestyle - Heats
14:30
Men's 100m Breaststroke - Heats
14:30
Men's 400m Freestyle - Heats
14:30
Women's 4 x 100m Freestyle Relay - Heats
14:30
Men's 4 x 100m Freestyle Relay - Heats
Table Tennis
Table Tennis
South Paris Arena 4
18:30
Men's & Women's Singles Preliminary Rnd
20:00
Mixed Doubles Round of 16
23:30
Men's & Women's Singles Round of 64
Tennis
Tennis
Roland-Garros Stadium
15:30
MS First Rnd/WS First Rnd
15:30
MS & WS First Rnd/MD & WD First Rnd
15:30
MS & WS First Rnd/MD & WD First Rnd
15:30
MS & WS First Rnd/MD & WD First Rnd
22:30
MS First Rnd/WS First Rnd
Volleyball
Volleyball
South Paris Arena 1
12:30
Men's Preliminary Phase
16:30
Men's Preliminary Phase
20:30
Men's Preliminary Phase
Water Polo
Water Polo
Aquatics Centre
17:30
Women's Preliminary Round - Group A
NED flag
Netherlands
-
Hungary
HUN flag
19:05
Women's Preliminary Round - Group B
GRE flag
Greece
-
United States
USA flag
22:00
Women's Preliminary Round - Group B
ESP flag
Spain
-
France
FRA flag
23:35
Women's Preliminary Round - Group A
AUS flag
Australia
-
China
CHN flag
""",

"28-July":
"""
Archery
Archery
Invalides
13:00
Women's Team 1/8 Elimination Round
17:45
Women's Team Quarterfinals
19:17
Women's Team Semifinals
20:18
Women's Team Bronze Medal Match
20:41
Women's Team Gold Medal Match
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
13:00
Women's Qualification - Subdivision 1
15:10
Women's Qualification - Subdivision 2
18:20
Women's Qualification - Subdivision 3
21:30
Women's Qualification - Subdivision 4
Badminton
Badminton
La Chapelle Arena
00:40
Women's Doubles Group play stage
00:40
Women's Doubles Group play stage
00:40
Women's Doubles Group play stage
01:30
Women's Doubles Group play stage
01:30
Men's Singles Group play stage
01:30
Men's Singles Group play stage
12:00
Mixed Doubles Group play stage
12:00
Mixed Doubles Group play stage
12:00
Women's Singles Group play stage
12:50
Women's Singles Group play stage
12:50
Women's Singles Group play stage
12:50
Men's Doubles Group play stage
13:40
Men's Doubles Group play stage
13:40
Women's Doubles Group play stage
13:40
Women's Doubles Group play stage
14:30
Men's Singles Group play stage
14:30
Men's Singles Group play stage
14:30
Men's Singles Group play stage
17:30
Mixed Doubles Group play stage
17:30
Mixed Doubles Group play stage
17:30
Men's Doubles Group play stage
18:20
Women's Doubles Group play stage
18:20
Women's Singles Group play stage
18:20
Women's Singles Group play stage
19:10
Women's Singles Group play stage
19:10
Women's Singles Group play stage
19:10
Men's Singles Group play stage
20:00
Men's Singles Group play stage
20:00
Men's Singles Group play stage
20:00
Men's Singles Group play stage
23:00
Mixed Doubles Group play stage
23:00
Mixed Doubles Group play stage
23:00
Mixed Doubles Group play stage
23:50
Mixed Doubles Group play stage
23:50
Men's Doubles Group play stage
23:50
Women's Singles Group play stage
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Men's Group Phase - Group A
BK1 flag
Winner OQT GRE
-
Canada
CAN flag
14:30
Men's Group Phase - Group C
SSD flag
South Sudan
-
Winner OQT PUR
BK4 flag
17:00
Women's Group Phase - Group A
ESP flag
Spain
-
China
CHN flag
20:45
Men's Group Phase - Group C
SRB flag
Serbia
-
United States
USA flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
01:30
Men's or Women's Preliminary Match
02:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
23:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
00:18
Women's 60kg - Prelims - Round of 32
01:06
Men's 63.5kg - Prelims - Round of 32
01:38
Men's 80kg - Prelims - Round of 32
14:30
Men's 57kg - Prelims - Round of 32
14:46
Men's 71kg - Prelims - Round of 32
15:18
Men's 92kg - Prelims - Round of 32
15:50
Women's 50kg - Prelims - Round of 32
16:22
Women's 66kg - Prelims - Round of 32
19:00
Men's 57kg - Prelims - Round of 32
19:16
Men's 71kg - Prelims - Round of 32
19:32
Men's 92kg - Prelims - Round of 16
20:20
Women's 50kg - Prelims - Round of 32
20:52
Women's 66kg - Prelims - Round of 32
23:30
Men's 71kg - Prelims - Round of 32
23:46
Men's 92kg - Prelims - Round of 16
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Women's Kayak Single Semifinal
21:15
Women's Kayak Single Final
Cycling Mountain Bike
Cycling Mountain Bike
Elancourt Hill
17:40
Women's Cross-country
Equestrian
Equestrian
Château de Versailles
14:00
Eventing Team Cross Country
14:00
Eventing Individual Cross Country
Fencing
Fencing
Grand Palais
00:10
Women's Épée Individual Bronze Mdl Bout
00:35
Men's Sabre Individual Bronze Mdl Bout
01:00
Women's Épée Individual Gold Medal Bout
01:25
Men's Sabre Individual Gold Medal Bout
13:00
Women's Foil Individual Table of 64
13:30
Men's Épée Individual Table of 64
13:55
Women's Foil Individual Table of 32
15:55
Men's Épée Individual Table of 32
17:35
Women's Foil Individual Table of 16
18:35
Men's Épée Individual Table of 16
19:25
Women's Foil Individual Table of 8
19:55
Men's Épée Individual Table of 8
22:30
Women's Foil Individual Semifinal 1
23:00
Women's Foil Individual Semifinal 2
23:30
Men's Épée Individual Semifinal 1
23:55
Men's Épée Individual Semifinal 2
Football
Football
Multiple Venues
00:30
Men's Group D
Bordeaux Stadium
JPN flag
Japan
-
Mali
MLI flag
00:30
Men's Group A
Nice Stadium
FRA flag
France
-
Guinea
GUI flag
20:30
Women's Group C
Parc des Princes
BRA flag
Brazil
-
Japan
JPN flag
20:30
Women's Group A
Lyon Stadium
NZL flag
New Zealand
-
Colombia
COL flag
22:30
Women's Group C
La Beaujoire Stadium
ESP flag
Spain
-
Nigeria
NGR flag
22:30
Women's Group B
Nice Stadium
AUS flag
Australia
-
Zambia
ZAM flag
Handball
Handball
South Paris Arena 6
00:30
Men's Preliminary Round Group B
DEN flag
Denmark
-
France
FRA flag
12:30
Women's Preliminary Round Group B
BRA flag
Brazil
-
Hungary
HUN flag
14:30
Women's Preliminary Round Group A
KOR flag
Korea
-
Slovenia
SLO flag
17:30
Women's Preliminary Round Group A
SWE flag
Sweden
-
Germany
GER flag
19:30
Women's Preliminary Round Group A
DEN flag
Denmark
-
Norway
NOR flag
22:30
Women's Preliminary Round Group B
ANG flag
Angola
-
Spain
ESP flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Women's Pool A
BEL flag
Belgium
-
China
CHN flag
14:00
Women's Pool A
GER flag
Germany
-
Japan
JPN flag
16:15
Women's Pool B
AUS flag
Australia
-
South Africa
RSA flag
16:45
Women's Pool B
GBR flag
Great Britain
-
Spain
ESP flag
20:30
Men's Pool A
GER flag
Germany
-
Spain
ESP flag
21:00
Men's Pool B
BEL flag
Belgium
-
New Zealand
NZL flag
23:15
Men's Pool A
NED flag
Netherlands
-
France
FRA flag
23:45
Men's Pool A
RSA flag
South Africa
-
Great Britain
GBR flag
Judo
Judo
Champ-de-Mars Arena
13:30
Men -66 kg Elimination Round of 64
13:30
Women -52 kg Elimination Round of 64
13:58
Men -66 kg Elimination Round of 32
13:58
Women -52 kg Quarterfinals
15:50
Men -66 kg Elimination Round of 16
16:46
Men -66 kg Quarterfinals
19:30
Men -66 kg Repechage
19:47
Men -66 kg Semifinals
20:04
Women -52 kg Repechage
20:21
Women -52 kg Semifinals
20:48
Men -66 kg Contest for Bronze Medal A
20:58
Men -66 kg Contest for Bronze Medal B
21:08
Men -66 kg Final
21:19
Women -52 kg Contest for Bronze Medal A
21:29
Women -52 kg Contest for Bronze Medal B
21:39
Women -52 kg Final
Rowing
Rowing
Nautical St - Flat water
12:30
Women's Single Sculls Repechages
13:06
Men's Single Sculls Repechages
13:40
Women's Double Sculls Repechages
13:50
Men's Double Sculls Repechages
14:00
Women's Pair Heats
14:30
Men's Pair Heats
15:00
LWT Women's Double Sculls Heats
15:30
LWT Men's Double Sculls Heats
16:00
Women's Four Heats
16:20
Men's Four Heats
Rugby Sevens
Rugby Sevens
Stade de France
19:00
Preliminary Phase
19:30
Preliminary Phase
20:00
Preliminary Phase
20:30
Preliminary Phase
21:00
Preliminary Phase
21:30
Preliminary Phase
22:30
Preliminary Phase
23:00
Preliminary Phase
23:30
Preliminary Phase
Sailing
Sailing
Marseille Marina
13:00
Women's Windsurfing - Race 1
13:00
Women's Windsurfing - Race 2
13:00
Men's Windsurfing - Race 3
13:00
Men's Windsurfing - Race 1
13:00
Men's Windsurfing - Race 2
13:00
Women's Windsurfing - Race 3
13:00
Men's Windsurfing - Race 4
13:00
Women's Windsurfing - Race 4
13:00
Women's Skiff - Race 1
13:00
Men's Skiff - Race 1
13:00
Women's Skiff - Race 2
13:00
Men's Skiff - Race 2
13:00
Men's Skiff - Race 3
13:00
Women's Skiff - Race 3
Shooting
Shooting
Chateauroux Shooting Ctr
12:45
10m Air Rifle Women's Qualification
13:00
10m Air Pistol Men's Final
14:45
10m Air Rifle Men's Qualification
15:30
10m Air Pistol Women's Final
Skateboarding
Skateboarding
La Concorde 3
15:30
Women's Street Prelims
20:30
Women's Street Final
Surfing
Surfing
Teahupo'o, Tahiti
03:18
Women's Round 1
22:30
Women's Round 2
Swimming
Swimming
Paris La Defense Arena
00:00
Women's 100m Butterfly Semifinals
00:12
Men's 400m Freestyle Final
00:25
Women's 400m Freestyle Final
00:45
Men's 100m Breaststroke Semifinals
01:07
Women's 4 x 100m Freestyle Relay Final
01:20
Men's 4 x 100m Freestyle Relay Final
14:30
Men's 200m Freestyle - Heats
14:30
Men's 400m Individual Medley - Heats
14:30
Women's 100m Breaststroke - Heats
14:30
Men's 100m Backstroke - Heats
14:30
Women's 200m Freestyle - Heats
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Singles Round of 64
19:30
Mixed Doubles Quarterfinal
23:30
Men's & Women's Singles Round of 64
Tennis
Tennis
Roland-Garros Stadium
15:30
MS First Rnd/WS First Rnd
15:30
MS & WS First Rnd/MD & WD First Rnd
15:30
MS & WS First Rnd/MD & WD First Rnd
22:30
MS & WS First Rnd/MD & WD First Rnd
22:30
MS First Rnd/WS First Rnd
Volleyball
Volleyball
South Paris Arena 1
00:30
Men's Preliminary Phase
12:30
Women's Preliminary Round - Pool C
ITA flag
Italy
-
Dominican Republic
DOM flag
16:30
Women's Preliminary Round - Pool B
POL flag
Poland
-
Japan
JPN flag
20:30
Men's Preliminary Phase
Water Polo
Water Polo
Aquatics Centre
14:00
Men's Preliminary Round - Group B
AUS flag
Australia
-
Spain
ESP flag
15:35
Men's Preliminary Round - Group B
SRB flag
Serbia
-
Japan
JPN flag
18:30
Men's Preliminary Round - Group A
ITA flag
Italy
-
United States
USA flag
20:05
Men's Preliminary Round - Group A
CRO flag
Croatia
-
Montenegro
MNE flag
23:00
Men's Preliminary Round - Group B
FRA flag
France
-
Hungary
HUN flag
""",

"29-July":
"""
Archery
Archery
Invalides
13:00
Men's Team 1/8 Elimination Round
17:45
Men's Team Quarterfinals
19:17
Men's Team Semifinals
20:18
Men's Team Bronze Medal Match
20:41
Men's Team Gold Medal Match
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
00:40
Women's Qualification - Subdivision 5
21:00
Men's Team Final
Badminton
Badminton
La Chapelle Arena
00:40
Women's Singles Group play stage
00:40
Women's Doubles Group play stage
00:40
Men's Singles Group play stage
01:30
Men's Singles Group play stage
12:00
Mixed Doubles Group play stage
12:00
Mixed Doubles Group play stage
12:00
Mixed Doubles Group play stage
12:50
Mixed Doubles Group play stage
12:50
Men's Doubles Group play stage
12:50
Men's Doubles Group play stage
13:40
Women's Singles Group play stage
13:40
Women's Singles Group play stage
13:40
Women's Doubles Group play stage
14:30
Women's Doubles Group play stage
14:30
Men's Singles Group play stage
14:30
Men's Singles Group play stage
17:30
Mixed Doubles Group play stage
17:30
Mixed Doubles Group play stage
17:30
Men's Doubles Group play stage
18:20
Women's Doubles Group play stage
18:20
Women's Singles Group play stage
18:20
Women's Singles Group play stage
19:10
Women's Singles Group play stage
19:10
Men's Singles Group play stage
19:10
Men's Singles Group play stage
20:00
Men's Singles Group play stage
23:00
Mixed Doubles Group play stage
23:00
Mixed Doubles Group play stage
23:00
Women's Singles Group play stage
23:50
Women's Singles Group play stage
23:50
Women's Singles Group play stage
23:50
Men's Doubles Group play stage
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Women's Group Phase - Group A
SRB flag
Serbia
-
Puerto Rico
PUR flag
14:30
Women's Group Phase - Group B
NGR flag
Nigeria
-
Australia
AUS flag
17:00
Women's Group Phase - Group C
GER flag
Germany
-
Belgium
BEL flag
20:45
Women's Group Phase - Group B
CAN flag
Canada
-
France
FRA flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Preliminary Match
01:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
23:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
00:34
Women's 50kg - Prelims - Round of 32
01:06
Women's 66kg - Prelims - Round of 32
14:30
Women's 60kg - Prelims - Round of 16
15:18
Men's 63.5kg - Prelims - Round of 16
16:06
Men's 92kg - Prelims - Round of 16
19:00
Women's 60kg - Prelims - Round of 16
19:32
Men's 63.5kg - Prelims - Round of 16
20:20
Men's +92kg - Prelims - Round of 16
23:30
Women's 60kg - Prelims - Round of 16
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Men's Canoe Single Semifinal
20:50
Men's Canoe Single Final
Cycling Mountain Bike
Cycling Mountain Bike
Elancourt Hill
17:40
Men's Cross-country
Diving
Diving
Aquatics Centre
14:30
Men's Synchronised 10m Platform Final
Equestrian
Equestrian
Château de Versailles
14:30
Eventing Individual Jumping Qualifier
14:30
Eventing Team Jumping Final
14:30
Eventing Individual Jumping Final
Fencing
Fencing
Grand Palais
00:20
Women's Foil Individual Bronze Mdl Bout
00:50
Men's Épée Individual Bronze Medal Bout
01:15
Women's Foil Individual Gold Medal Bout
01:45
Men's Épée Individual Gold Medal Bout
13:00
Women's Sabre Individual Table of 64
13:25
Men's Foil Individual Table of 64
13:55
Women's Sabre Individual Table of 32
15:35
Men's Foil Individual Table of 32
17:35
Women's Sabre Individual Table of 16
18:25
Men's Foil Individual Table of 16
19:25
Women's Sabre Individual Table of 8
19:50
Men's Foil Individual Table of 8
22:30
Women's Sabre Individual Semifinal 1
22:55
Women's Sabre Individual Semifinal 2
23:20
Men's Foil Individual Semifinal 1
23:50
Men's Foil Individual Semifinal 2
Football
Football
Multiple Venues
00:30
Women's Group A
Geoffroy-Guichard Stadium
FRA flag
France
-
Canada
CAN flag
00:30
Women's Group B
Marseille Stadium
USA flag
United States
-
Germany
GER flag
Handball
Handball
South Paris Arena 6
00:30
Women's Preliminary Round Group B
FRA flag
France
-
Netherlands
NED flag
12:30
Men's Preliminary Round Group A
JPN flag
Japan
-
Germany
GER flag
14:30
Men's Preliminary Round Group A
SLO flag
Slovenia
-
Croatia
CRO flag
17:30
Men's Preliminary Round Group B
EGY flag
Egypt
-
Denmark
DEN flag
19:30
Men's Preliminary Round Group A
SWE flag
Sweden
-
Spain
ESP flag
22:30
Men's Preliminary Round Group B
FRA flag
France
-
Norway
NOR flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Men's Pool B
IRL flag
Ireland
-
Australia
AUS flag
14:00
Women's Pool A
JPN flag
Japan
-
China
CHN flag
16:15
Men's Pool B
IND flag
India
-
Argentina
ARG flag
16:45
Women's Pool B
ESP flag
Spain
-
United States
USA flag
20:30
Women's Pool B
GBR flag
Great Britain
-
Australia
AUS flag
21:00
Women's Pool B
RSA flag
South Africa
-
Argentina
ARG flag
23:15
Women's Pool A
GER flag
Germany
-
Netherlands
NED flag
23:45
Women's Pool A
FRA flag
France
-
Belgium
BEL flag
Judo
Judo
Champ-de-Mars Arena
13:30
Women -57 kg Elimination Round of 64
13:30
Men -73 kg Elimination Round of 64
13:58
Women -57 kg Elimination Round of 32
13:58
Men -73 kg Elimination Round of 32
15:50
Women -57 kg Elimination Round of 16
15:50
Men -73 kg Elimination Round of 16
16:46
Women -57 kg Quarterfinals
16:46
Men -73 kg Quarterfinals
19:30
Women -57 kg Repechage
19:47
Women -57 kg Semifinals
20:04
Men -73 kg Repechage
20:21
Men -73 kg Semifinals
20:48
Women -57 kg Contest for Bronze Medal A
20:58
Women -57 kg Contest for Bronze Medal B
21:08
Women -57 kg Final
21:19
Men -73 kg Contest for Bronze Medal A
21:29
Men -73 kg Contest for Bronze Medal B
21:39
Men -73 kg Final
Rowing
Rowing
Nautical St - Flat water
13:00
Men's Single Sculls Semifinal E/F 1
13:12
Men's Single Sculls Semifinal E/F 2
13:24
Women's Single Sculls Semifinal E/F 1
13:36
Women's Single Sculls Semifinal E/F 2
13:50
Men's Pair Repechages
14:00
Women's Pair Repechages
14:10
LWT Men's Double Sculls Repechages
14:30
LWT Women's Double Sculls Repechages
14:50
Men's Quad. Sculls Repechages
15:00
Women's Quad. Sculls Repechages
15:10
Men's Eight Heats
15:30
Women's Eight Heats
Rugby Sevens
Rugby Sevens
Stade de France
00:00
Preliminary Phase
00:30
Preliminary Phase
01:00
Preliminary Phase
17:30
Preliminary Phase
18:00
Preliminary Phase
18:30
Preliminary Phase
19:00
Preliminary Phase
19:30
Preliminary Phase
20:00
Preliminary Phase
23:30
Women's Placing 9-12
Sailing
Sailing
Marseille Marina
15:30
Women's Skiff - Race 4
15:30
Women's Skiff - Race 5
15:30
Women's Skiff - Race 6
15:30
Men's Skiff - Race 4
15:30
Men's Skiff - Race 5
15:30
Men's Skiff - Race 6
15:30
Women's Windsurfing - Race 5
15:30
Men's Windsurfing - Race 5
15:30
Women's Windsurfing - Race 6
15:30
Men's Windsurfing - Race 6
15:30
Women's Windsurfing - Race 7
15:30
Men's Windsurfing - Race 7
15:30
Women's Windsurfing - Race 8
15:30
Men's Windsurfing - Race 8
Shooting
Shooting
Chateauroux Shooting Ctr
12:30
Trap Men's Qualification - Day 1
12:45
10m Air Pistol Mixed Team Qualification
13:00
10m Air Rifle Women's Final
15:30
10m Air Rifle Men's Final
Surfing
Surfing
Teahupo'o, Tahiti
03:18
Men's Round 2
22:30
Men's Round 3
Swimming
Swimming
Paris La Defense Arena
00:00
Men's 400m Individual Medley Final
00:15
Women's 100m Butterfly Final
00:21
Men's 200m Freestyle Semifinals
00:45
Women's 100m Breaststroke Semifinals
01:07
Men's 100m Backstroke Semifinals
01:24
Men's 100m Breaststroke Final
01:30
Women's 200m Freestyle Semifinals
14:30
Women's 400m Individual Medley - Heats
14:30
Women's 100m Backstroke - Heats
14:30
Men's 800m Freestyle - Heats
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Singles Round of 64
20:30
Mixed Doubles Semifinal
23:30
Men's & Women's Singles Round of 32
Tennis
Tennis
Roland-Garros Stadium
15:30
MS Second Rnd/WS Second Rnd
15:30
MS & WS 2nd Rnd/MD & WD 2nd Rnd/XD 1st R
15:30
MS & WS 2nd Rnd/MD & WD 2nd Rnd/XD 1st R
15:30
MS & WS 2nd Rnd/MD & WD 2nd Rnd/XD 1st R
22:30
MS Second Rnd/WS Second Rnd
Volleyball
Volleyball
South Paris Arena 1
00:30
Men's Preliminary Phase
12:30
Women's Preliminary Round - Pool C
TUR flag
Türkiye
-
Netherlands
NED flag
16:30
Women's Preliminary Round - Pool B
BRA flag
Brazil
-
Kenya
KEN flag
20:30
Women's Preliminary Round - Pool A
USA flag
United States
-
China
CHN flag
Water Polo
Water Polo
Aquatics Centre
00:35
Men's Preliminary Round - Group A
ROU flag
Romania
-
Greece
GRE flag
17:30
Women's Preliminary Round - Group B
FRA flag
France
-
Italy
ITA flag
19:05
Women's Preliminary Round - Group B
USA flag
United States
-
Spain
ESP flag
22:00
Women's Preliminary Round - Group A
CHN flag
China
-
Netherlands
NED flag
23:35
Women's Preliminary Round - Group A
HUN flag
Hungary
-
Canada
CAN flag
""",

"30-July":
"""
Archery
Archery
Invalides
15:30
Men's Individual 1/32 Elimination Round
15:56
Women's Individual 1/32 Elimination Rnd
16:22
Men's Individual 1/16 Elimination Round
16:35
Women's Individual 1/16 Elimination Rnd
21:15
Men's Individual 1/32 Elimination Round
21:41
Women's Individual 1/32 Elimination Rnd
22:07
Men's Individual 1/16 Elimination Round
22:20
Women's Individual 1/16 Elimination Rnd
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
21:45
Women's Team Final
Badminton
Badminton
La Chapelle Arena
00:40
Women's Doubles Group play stage
00:40
Men's Singles Group play stage
00:40
Men's Singles Group play stage
01:30
Men's Singles Group play stage
12:00
Women's Singles Group play stage
12:00
Women's Singles Group play stage
12:00
Women's Singles Group play stage
12:50
Women's Singles Group play stage
12:50
Men's Doubles Group play stage
12:50
Men's Doubles Group play stage
13:40
Women's Doubles Group play stage
13:40
Women's Doubles Group play stage
13:40
Women's Doubles Group play stage
14:30
Women's Doubles Group play stage
14:30
Men's Singles Group play stage
14:30
Men's Singles Group play stage
17:30
Men's Doubles Group play stage
17:30
Men's Doubles Group play stage
17:30
Men's Doubles Group play stage
18:20
Men's Doubles Group play stage
18:20
Women's Doubles Group play stage
18:20
Women's Doubles Group play stage
19:10
Women's Singles Group play stage
19:10
Women's Singles Group play stage
19:10
Women's Singles Group play stage
20:00
Men's Singles Group play stage
20:00
Men's Singles Group play stage
23:00
Women's Singles Group play stage
23:00
Women's Singles Group play stage
23:00
Women's Singles Group play stage
23:50
Men's Doubles Group play stage
23:50
Men's Doubles Group play stage
23:50
Women's Doubles Group play stage
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Women's Group Phase - Group C
USA flag
United States
-
Japan
JPN flag
14:30
Men's Group Phase - Group A
BK2 flag
Winner OQT ESP
-
Winner OQT GRE
BK1 flag
17:00
Men's Group Phase - Group A
CAN flag
Canada
-
Australia
AUS flag
20:45
Men's Group Phase - Group B
JPN flag
Japan
-
France
FRA flag
Basketball 3x3
Basketball 3x3
La Concorde 1
21:00
Women's Pool Round
USA flag
United States
-
Germany
GER flag
21:30
Women's Pool Round
AUS flag
Australia
-
Canada
CAN flag
22:05
Men's Pool Round
LTU flag
Lithuania
-
Latvia
LAT flag
22:35
Men's Pool Round
NED flag
Netherlands
-
China
CHN flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Preliminary Match
01:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
23:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
00:18
Men's 63.5kg - Prelims - Round of 16
00:50
Men's +92kg - Prelims - Round of 16
14:30
Men's 51kg - Prelims - Round of 16
15:18
Men's 80kg - Prelims - Round of 16
15:50
Women's 54kg - Prelims - Round of 16
16:38
Women's 57kg - Prelims - Round of 32
19:00
Men's 51kg - Prelims - Round of 16
19:48
Men's 80kg - Prelims - Round of 16
20:20
Women's 54kg - Prelims - Round of 16
21:08
Women's 57kg - Prelims - Round of 32
23:30
Men's 51kg - Prelims - Round of 16
Canoe Slalom
Canoe Slalom
Nautical St - White water
18:30
Women's Canoe Single Heats 1st Run
19:30
Men's Kayak Single Heats 1st Run
20:40
Women's Canoe Single Heats 2nd Run
21:40
Men's Kayak Single Heats 2nd Run
Cycling BMX Freestyle
Cycling BMX Freestyle
La Concorde 2
16:55
Women's Park Qualification
18:42
Men's Park Qualification
Equestrian
Equestrian
Château de Versailles
14:30
Dressage Team Grand Prix Day 1
14:30
Dressage Individual Grand Prix Day 1
Fencing
Fencing
Grand Palais
00:20
Women's Sabre Individual Brz Mdl Bout
00:45
Men's Foil Individual Bronze Medal Bout
01:15
Women's Sabre Individual Gold Mdl Bout
01:40
Men's Foil Individual Gold Medal Bout
17:00
Women's Épée Team Table of 8
18:30
Women's Épée Team Classifications 5-8
19:20
Women's Épée Team Semifinal 2
19:20
Women's Épée Team Semifinal 1
20:10
Women's Épée Team Placement 7-8
20:10
Women's Épée Team Placement 5-6
23:00
Women's Épée Team Bronze Medal Match
Football
Football
Multiple Venues
18:30
Men's Group C
Parc des Princes
DOM flag
Dominican Republic
-
Uzbekistan
UZB flag
18:30
Men's Group C
Bordeaux Stadium
ESP flag
Spain
-
Egypt
EGY flag
20:30
Men's Group B
Lyon Stadium
UKR flag
Ukraine
-
Argentina
ARG flag
20:30
Men's Group B
Nice Stadium
MAR flag
Morocco
-
Iraq
IRQ flag
22:30
Men's Group A
Geoffroy-Guichard Stadium
USA flag
United States
-
Guinea
GUI flag
22:30
Men's Group A
Marseille Stadium
NZL flag
New Zealand
-
France
FRA flag
Handball
Handball
South Paris Arena 6
00:30
Men's Preliminary Round Group B
ARG flag
Argentina
-
Hungary
HUN flag
12:30
Women's Preliminary Round Group A
GER flag
Germany
-
Slovenia
SLO flag
14:30
Women's Preliminary Round Group A
NOR flag
Norway
-
Korea
KOR flag
17:30
Women's Preliminary Round Group B
NED flag
Netherlands
-
Spain
ESP flag
19:30
Women's Preliminary Round Group B
HUN flag
Hungary
-
Angola
ANG flag
22:30
Women's Preliminary Round Group B
FRA flag
France
-
Brazil
BRA flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Men's Pool A
ESP flag
Spain
-
France
FRA flag
14:00
Men's Pool A
RSA flag
South Africa
-
Germany
GER flag
16:15
Men's Pool A
GBR flag
Great Britain
-
Netherlands
NED flag
16:45
Men's Pool B
IRL flag
Ireland
-
India
IND flag
20:30
Men's Pool B
ARG flag
Argentina
-
New Zealand
NZL flag
23:15
Men's Pool B
AUS flag
Australia
-
Belgium
BEL flag
Judo
Judo
Champ-de-Mars Arena
13:30
Men -81 kg Elimination Round of 64
13:30
Women -63 kg Elimination Round of 64
13:58
Men -81 kg Elimination Round of 32
13:58
Women -63 kg Elimination Round of 32
15:50
Men -81 kg Elimination Round of 16
15:50
Women -63 kg Elimination Round of 16
16:46
Men -81 kg Quarterfinals
16:46
Women -63 kg Quarterfinals
19:30
Men -81 kg Repechage
19:47
Men -81 kg Semifinals
20:04
Women -63 kg Repechage
20:21
Women -63 kg Semifinals
20:48
Men -81 kg Contest for Bronze Medal A
20:58
Men -81 kg Contest for Bronze Medal B
21:08
Men -81 kg Final
21:19
Women -63 kg Contest for Bronze Medal A
21:29
Women -63 kg Contest for Bronze Medal B
21:39
Women -63 kg Final
Rowing
Rowing
Nautical St - Flat water
13:00
Women's Single Sculls Quarterfinals
13:40
Men's Single Sculls Quarterfinals
14:20
Women's Double Sculls Semifinal A/B 1
14:30
Women's Double Sculls Semifinal A/B 2
14:40
Men's Double Sculls Semifinal A/B 1
14:50
Men's Double Sculls Semifinal A/B 2
15:00
Women's Four Repechages
15:10
Men's Four Repechages
Rugby Sevens
Rugby Sevens
Stade de France
00:00
Women's Placing 9-12
00:30
Women's Quarter-final
01:00
Women's Quarter-final
01:30
Women's Quarter-final
02:00
Women's Quarter-final
18:00
Women's Placing 5-8
18:30
Women's Placing 5-8
19:00
Women's Semi-final
19:30
Women's Semi-final
20:00
Women's Placing 11-12
20:30
Women's Placing 9-10
21:30
Women's Placing 7-8
22:00
Women's Placing 5-6
22:30
Women's Bronze Medal Match
23:15
Women's Gold Medal Match
Sailing
Sailing
Marseille Marina
15:30
Women's Windsurfing - Race 9
15:30
Women's Windsurfing - Race 10
15:30
Women's Windsurfing - Race 11
15:30
Women's Windsurfing - Race 12
15:30
Men's Windsurfing - Race 9
15:30
Men's Windsurfing - Race 10
15:30
Men's Windsurfing - Race 11
15:30
Men's Windsurfing - Race 12
15:30
Women's Skiff - Race 7
15:30
Women's Skiff - Race 8
15:30
Women's Skiff - Race 9
15:30
Men's Skiff - Race 7
15:30
Men's Skiff - Race 8
15:30
Men's Skiff - Race 9
Shooting
Shooting
Chateauroux Shooting Ctr
13:30
Trap Men's Qualification - Day 2
13:30
Trap Women's Qualification - Day 1
13:00
10m Air Pistol Mixed Team Bronze Medal
13:30
10m Air Pistol Mixed Team Gold Medal
19:00
Trap Men's Final
Surfing
Surfing
Teahupo'o, Tahiti
03:18
Women's Round 3
22:30
Men's Quarterfinals
Swimming
Swimming
Paris La Defense Arena
00:00
Women's 400m Individual Medley Final
00:13
Men's 200m Freestyle Final
00:30
Women's 100m Backstroke Semifinals
00:52
Men's 100m Backstroke Final
01:02
Women's 100m Breaststroke Final
01:18
Women's 200m Freestyle Final
14:30
Men's 200m Butterfly - Heats
14:30
Men's 100m Freestyle - Heats
14:30
Women's 1500m Freestyle - Heats
14:30
Women's 100m Freestyle - Heats
14:30
Men's 200m Breaststroke - Heats
14:30
Men's 4 x 200m Freestyle Relay - Heats
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Singles Round of 32
17:00
Mixed Doubles Bronze Medal Match
18:00
Mixed Doubles Gold Medal Match
Tennis
Tennis
Roland-Garros Stadium
15:30
MS Second Rnd/WS Third Rnd
15:30
MS R2/WS R3/MD R3/WD R2/XD R1
15:30
MS R2/WS R3/MD R3/WD R2/XD R2
15:30
MS R2/WS R3/MD R3/WD R2/XD R3
22:30
MS Second Rnd/WS Third Rnd
Triathlon
Triathlon
Pont Alexandre III
11:30
Men's Individual
Volleyball
Volleyball
South Paris Arena 1
00:30
Women's Preliminary Round - Pool A
FRA flag
France
-
Serbia
SRB flag
12:30
Men's Preliminary Round - Pool B
ITA flag
Italy
-
Egypt
EGY flag
16:30
Men's Preliminary Round - Pool C
USA flag
United States
-
Germany
GER flag
20:30
Men's Preliminary Round - Pool A
SLO flag
Slovenia
-
Serbia
SRB flag
Water Polo
Water Polo
Aquatics Centre
14:00
Men's Preliminary Round - Group B
AUS flag
Australia
-
Serbia
SRB flag
15:35
Men's Preliminary Round - Group A
CRO flag
Croatia
-
Italy
ITA flag
18:30
Men's Preliminary Round - Group B
JPN flag
Japan
-
France
FRA flag
20:05
Men's Preliminary Round - Group A
USA flag
United States
-
Romania
ROU flag
23:00
Men's Preliminary Round - Group A
MNE flag
Montenegro
-
Greece
GRE flag
""",

"31-July":
"""
Archery
Archery
Invalides
15:30
Men's Individual 1/32 Elimination Round
15:56
Women's Individual 1/32 Elimination Rnd
16:22
Men's Individual 1/16 Elimination Round
16:35
Women's Individual 1/16 Elimination Rnd
21:15
Men's Individual 1/32 Elimination Round
21:41
Women's Individual 1/32 Elimination Rnd
22:07
Men's Individual 1/16 Elimination Round
22:20
Women's Individual 1/16 Elimination Rnd
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
21:00
Men's All-Around Final
Badminton
Badminton
La Chapelle Arena
00:40
Women's Doubles Group play stage
00:40
Men's Singles Group play stage
00:40
Men's Singles Group play stage
01:30
Men's Singles Group play stage
12:00
Women's Singles Group play stage
12:00
Women's Singles Group play stage
12:00
Women's Singles Group play stage
12:50
Women's Singles Group play stage
12:50
Women's Singles Group play stage
12:50
Men's Singles Group play stage
13:40
Men's Singles Group play stage
13:40
Men's Singles Group play stage
13:40
Men's Singles Group play stage
14:30
Men's Singles Group play stage
14:30
Men's Singles Group play stage
17:30
Women's Singles Group play stage
17:30
Women's Singles Group play stage
17:30
Women's Singles Group play stage
18:20
Women's Singles Group play stage
18:20
Women's Singles Group play stage
18:20
Men's Singles Group play stage
19:10
Men's Singles Group play stage
19:10
Men's Singles Group play stage
19:10
Men's Singles Group play stage
20:00
Men's Singles Group play stage
20:00
Men's Singles Group play stage
23:00
Women's Singles Group play stage
23:00
Women's Singles Group play stage
23:00
Men's Singles Group play stage
23:50
Men's Singles Group play stage
23:50
Men's Singles Group play stage
23:50
Mixed Doubles Quarterfinal
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Men's Group Phase - Group B
BK3 flag
Winner OQT LAT
-
Germany
GER flag
14:30
Women's Group Phase - Group A
PUR flag
Puerto Rico
-
Spain
ESP flag
17:00
Women's Group Phase - Group A
CHN flag
China
-
Serbia
SRB flag
20:45
Men's Group Phase - Group C
BK4 flag
Winner OQT PUR
-
Serbia
SRB flag
Basketball 3x3
Basketball 3x3
La Concorde 1
00:30
Women's Pool Round
AZE flag
Azerbaijan
-
Spain
ESP flag
01:00
Women's Pool Round
FRA flag
France
-
China
CHN flag
01:35
Men's Pool Round
FRA flag
France
-
Poland
POL flag
02:05
Men's Pool Round
USA flag
United States
-
Serbia
SRB flag
21:00
Women's Pool Round
AUS flag
Australia
-
Germany
GER flag
21:30
Women's Pool Round
CAN flag
Canada
-
China
CHN flag
22:05
Men's Pool Round
LAT flag
Latvia
-
Netherlands
NED flag
22:35
Men's Pool Round
SRB flag
Serbia
-
China
CHN flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Preliminary Match
01:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
23:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
00:02
Men's 80kg - Prelims - Round of 16
01:06
Women's 54kg - Prelims - Round of 16
01:38
Women's 57kg - Prelims - Round of 32
14:30
Men's 57kg - Prelims - Round of 16
15:02
Men's 71kg - Prelims - Round of 16
15:34
Women's 75kg - Prelims - Round of 16
16:38
Women's 60kg - Quarterfinal
19:00
Men's 57kg - Prelims - Round of 16
19:48
Men's 71kg - Prelims - Round of 16
20:36
Women's 75kg - Prelims - Round of 16
21:08
Women's 60kg - Quarterfinal
23:30
Men's 57kg - Prelims - Round of 16
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Women's Canoe Single Semifinal
20:55
Women's Canoe Single Final
Cycling BMX Freestyle
Cycling BMX Freestyle
La Concorde 2
16:40
Women's Park Final
18:15
Men's Park Final
Diving
Diving
Aquatics Centre
14:30
Women's Synchronised 10m Platform Final
Equestrian
Equestrian
Château de Versailles
13:30
Dressage Team Grand Prix Day 2
13:30
Dressage Individual Grand Prix Day 2
Fencing
Fencing
Grand Palais
00:00
Women's Épée Team Gold Medal Match
17:00
Men's Sabre Team Table of 8
18:30
Men's Sabre Team Classifications 5-8
19:20
Men's Sabre Team Semifinal 2
19:20
Men's Sabre Team Semifinal 1
20:10
Men's Sabre Team Placement 7-8
20:10
Men's Sabre Team Placement 5-6
23:00
Men's Sabre Team Bronze Medal Match
Football
Football
Multiple Venues
00:30
Men's Group D
Parc des Princes
PAR flag
Paraguay
-
Mali
MLI flag
00:30
Men's Group D
La Beaujoire Stadium
ISR flag
Israel
-
Japan
JPN flag
20:30
Women's Group C
La Beaujoire Stadium
JPN flag
Japan
-
Nigeria
NGR flag
20:30
Women's Group C
Bordeaux Stadium
BRA flag
Brazil
-
Spain
ESP flag
22:30
Women's Group B
Geoffroy-Guichard Stadium
ZAM flag
Zambia
-
Germany
GER flag
22:30
Women's Group B
Marseille Stadium
AUS flag
Australia
-
United States
USA flag
Handball
Handball
South Paris Arena 6
00:30
Women's Preliminary Round Group A
SWE flag
Sweden
-
Denmark
DEN flag
12:30
Men's Preliminary Round Group B
NOR flag
Norway
-
Hungary
HUN flag
14:30
Men's Preliminary Round Group A
CRO flag
Croatia
-
Germany
GER flag
17:30
Men's Preliminary Round Group A
ESP flag
Spain
-
Japan
JPN flag
19:30
Men's Preliminary Round Group A
SLO flag
Slovenia
-
Sweden
SWE flag
22:30
Men's Preliminary Round Group B
FRA flag
France
-
Egypt
EGY flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Women's Pool B
ARG flag
Argentina
-
Spain
ESP flag
14:00
Women's Pool B
RSA flag
South Africa
-
Great Britain
GBR flag
16:15
Women's Pool A
FRA flag
France
-
Germany
GER flag
16:45
Women's Pool B
AUS flag
Australia
-
United States
USA flag
20:30
Women's Pool A
BEL flag
Belgium
-
Japan
JPN flag
21:00
Men's Pool A
GER flag
Germany
-
Netherlands
NED flag
23:15
Men's Pool A
ESP flag
Spain
-
South Africa
RSA flag
23:45
Women's Pool A
NED flag
Netherlands
-
China
CHN flag
Judo
Judo
Champ-de-Mars Arena
13:30
Women -70 kg Elimination Round of 64
13:30
Men -90 kg Elimination Round of 64
13:58
Women -70 kg Elimination Round of 32
13:58
Men -90 kg Elimination Round of 32
15:50
Women -70 kg Elimination Round of 16
15:50
Men -90 kg Elimination Round of 16
16:46
Women -70 kg Quarterfinals
16:46
Men -90 kg Quarterfinals
19:30
Women -70 kg Repechage
19:47
Women -70 kg Semifinals
20:04
Men -90 kg Repechage
20:21
Men -90 kg Semifinals
20:48
Women -70 kg Contest for Bronze Medal A
20:58
Women -70 kg Contest for Bronze Medal B
21:08
Women -70 kg Final
21:19
Men -90 kg Contest for Bronze Medal A
21:29
Men -90 kg Contest for Bronze Medal B
21:39
Men -90 kg Final
Rowing
Rowing
Nautical St - Flat water
13:00
LWT Men's Double Sculls Final C
13:12
LWT Women's Double Sculls Final C
13:24
Men's Single Sculls Semifinal C/D 1
13:34
Men's Single Sculls Semifinal C/D 2
13:44
Women's Single Sculls Semifinal C/D 1
13:54
Women's Single Sculls Semifinal C/D 2
14:04
Men's Pair Semifinal A/B 1
14:14
Men's Pair Semifinal A/B 2
14:24
Women's Pair Semifinal A/B 1
14:34
Women's Pair Semifinal A/B 2
14:44
LWT Men's Double Sculls Semifinal A/B 1
14:54
LWT Men's Double Sculls Semifinal A/B 2
15:04
LWT Women's Double Sculls Semi A/B 1
15:14
LWT Women's Double Sculls Semi A/B 2
15:32
Men's Quad. Sculls Final B
15:44
Women's Quad. Sculls Final B
15:56
Men's Quad. Sculls Final A
16:08
Women's Quad. Sculls Final A
Sailing
Sailing
Marseille Marina
15:30
Women's Skiff - Race 10
15:30
Women's Skiff - Race 11
15:30
Women's Skiff - Race 12
15:30
Men's Skiff - Race 10
15:30
Men's Skiff - Race 11
15:30
Men's Skiff - Race 12
15:30
Men's Windsurfing - Race 13
15:30
Men's Windsurfing - Race 14
15:30
Men's Windsurfing - Race 15
15:30
Men's Windsurfing - Race 16
15:30
Women's Windsurfing - Race 13
15:30
Women's Windsurfing - Race 14
15:30
Women's Windsurfing - Race 15
15:30
Women's Windsurfing - Race 16
Shooting
Shooting
Chateauroux Shooting Ctr
12:30
50m Rifle 3 Pos. Men's Qualification
12:30
Trap Women's Qualification - Day 2
19:00
Trap Women's Final
Surfing
Surfing
Teahupo'o, Tahiti
00:54
Women's Quarterfinals
03:18
Men's Semifinals
04:30
Women's Semifinals
05:42
Men's Bronze Medal Match
06:23
Women's Bronze Medal Match
07:04
Men's Gold Medal Match
07:45
Women's Gold Medal Match
Swimming
Swimming
Paris La Defense Arena
00:00
Men's 100m Freestyle Semifinals
00:11
Men's 200m Butterfly Semifinals
00:27
Women's 100m Backstroke Final
00:33
Men's 800m Freestyle Final
00:55
Women's 100m Freestyle Semifinals
01:16
Men's 200m Breaststroke Semifinals
01:29
Men's 4 x 200m Freestyle Relay Final
14:30
Women's 200m Breaststroke - Heats
14:30
Men's 200m Backstroke - Heats
14:30
Women's 200m Butterfly - Heats
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Singles Round of 32
18:30
Men's & Women's Singles Round of 16
23:30
Men's & Women's Singles Round of 16
Tennis
Tennis
Roland-Garros Stadium
15:30
MS Third Rnd/WS Quarterfinals
15:30
MS Third Rnd/WS QF/MD SF/WD QF/XD QF
15:30
MS Third Rnd/MD SF/WD QF/XD QF
15:30
MS Third Rnd/WD QF/XD QF
22:30
MS Third Rnd/WS Quarterfinals
Triathlon
Triathlon
Pont Alexandre III
11:30
Women's Individual
Volleyball
Volleyball
South Paris Arena 1
00:30
Men's Preliminary Round - Pool A
FRA flag
France
-
Canada
CAN flag
12:30
Men's Preliminary Round - Pool B
POL flag
Poland
-
Brazil
BRA flag
16:30
Men's Preliminary Round - Pool C
JPN flag
Japan
-
Argentina
ARG flag
20:30
Women's Preliminary Round - Pool A
USA flag
United States
-
Serbia
SRB flag
Water Polo
Water Polo
Aquatics Centre
00:35
Men's Preliminary Round - Group B
ESP flag
Spain
-
Hungary
HUN flag
17:30
Women's Preliminary Round - Group A
NED flag
Netherlands
-
Australia
AUS flag
19:05
Women's Preliminary Round - Group A
CAN flag
Canada
-
China
CHN flag
22:00
Women's Preliminary Round - Group B
ITA flag
Italy
-
United States
USA flag
23:35
Women's Preliminary Round - Group B
ESP flag
Spain
-
Greece
GRE flag
""",

"1-August":
"""
Archery
Archery
Invalides
13:00
Men's Individual 1/32 Elimination Round
13:26
Women's Individual 1/32 Elimination Rnd
13:52
Men's Individual 1/16 Elimination Round
14:05
Women's Individual 1/16 Elimination Rnd
19:00
Men's Individual 1/32 Elimination Round
19:26
Women's Individual 1/32 Elimination Rnd
19:52
Men's Individual 1/16 Elimination Round
20:05
Women's Individual 1/16 Elimination Rnd
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
21:45
Women's All-Around Final
Athletics
Athletics
Trocadéro
11:00
Men's 20km Race Walk
12:50
Women's 20km Race Walk
Badminton
Badminton
La Chapelle Arena
00:40
Mixed Doubles Quarterfinal
00:40
Mixed Doubles Quarterfinal
01:00
Mixed Doubles Quarterfinal
12:00
Women's Doubles Quarterfinal
12:00
Women's Doubles Quarterfinal
12:00
Women's Doubles Quarterfinal
13:10
Men's Singles Round of 16
13:10
Men's Singles Round of 16
13:10
Women's Doubles Quarterfinal
16:30
Men's Doubles Quarterfinal
16:30
Men's Doubles Quarterfinal
16:30
Men's Doubles Quarterfinal
17:40
Men's Singles Round of 16
17:40
Men's Singles Round of 16
17:40
Men's Doubles Quarterfinal
18:50
Men's Singles Round of 16
22:00
Women's Singles Round of 16
22:00
Women's Singles Round of 16
22:00
Women's Singles Round of 16
23:00
Women's Singles Round of 16
23:00
Women's Singles Round of 16
23:00
Mixed Doubles Semifinal
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Men's Group Phase - Group C
USA flag
United States
-
South Sudan
SSD flag
14:30
Women's Group Phase - Group C
JPN flag
Japan
-
Germany
GER flag
17:00
Women's Group Phase - Group B
AUS flag
Australia
-
Canada
CAN flag
20:45
Women's Group Phase - Group B
FRA flag
France
-
Nigeria
NGR flag
Basketball 3x3
Basketball 3x3
La Concorde 1
00:30
Women's Pool Round
ESP flag
Spain
-
France
FRA flag
01:00
Women's Pool Round
USA flag
United States
-
Azerbaijan
AZE flag
01:35
Men's Pool Round
LTU flag
Lithuania
-
France
FRA flag
02:05
Men's Pool Round
USA flag
United States
-
Poland
POL flag
12:30
Women's Pool Round
CHN flag
China
-
Australia
AUS flag
13:00
Women's Pool Round
GER flag
Germany
-
Canada
CAN flag
13:35
Men's Pool Round
NED flag
Netherlands
-
Serbia
SRB flag
14:05
Men's Pool Round
CHN flag
China
-
Latvia
LAT flag
16:00
Women's Pool Round
AZE flag
Azerbaijan
-
France
FRA flag
16:30
Women's Pool Round
USA flag
United States
-
Australia
AUS flag
17:05
Men's Pool Round
POL flag
Poland
-
Lithuania
LTU flag
17:35
Men's Pool Round
FRA flag
France
-
Netherlands
NED flag
21:30
Women's Pool Round
CHN flag
China
-
Spain
ESP flag
22:00
Women's Pool Round
GER flag
Germany
-
Azerbaijan
AZE flag
22:35
Men's Pool Round
LTU flag
Lithuania
-
United States
USA flag
23:05
Men's Pool Round
CHN flag
China
-
Poland
POL flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Preliminary Match
01:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
23:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
00:18
Men's 71kg - Prelims - Round of 16
01:06
Women's 75kg - Prelims - Round of 16
01:38
Women's 60kg - Quarterfinal
14:30
Women's 50kg - Prelims - Round of 16
15:18
Women's 66kg - Prelims - Round of 16
16:06
Women's 54kg - Quarterfinal
16:22
Men's 63.5kg - Quarterfinal
16:38
Men's 92kg - Quarterfinal
19:00
Women's 50kg - Prelims - Round of 16
19:48
Women's 66kg - Prelims - Round of 16
20:36
Women's 54kg - Quarterfinals
21:08
Men's 63.5kg - Quarterfinal
21:24
Men's 92kg - Quarterfinal
23:30
Women's 50kg - Prelims - Round of 16
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Men's Kayak Single Semifinal
21:00
Men's Kayak Single Final
Cycling BMX Racing
Cycling BMX Racing
BMX Stadium
23:30
Men, Quarterfinals Run 1
23:50
Women, Quarterfinals Run 1
Equestrian
Equestrian
Château de Versailles
14:30
Jumping Team Qualifier
Fencing
Fencing
Grand Palais
00:00
Men's Sabre Team Gold Medal Match
15:20
Women's Foil Team Table of 8
17:10
Women's Foil Team Classifications 5-8
18:20
Women's Foil Team Semifinal 2
18:20
Women's Foil Team Semifinal 1
19:30
Women's Foil Team Placement 7-8
19:30
Women's Foil Team Placement 5-6
22:40
Women's Foil Team Bronze Medal Match
Football
Football
Multiple Venues
00:30
Women's Group A
Lyon Stadium
NZL flag
New Zealand
-
France
FRA flag
00:30
Women's Group A
Nice Stadium
COL flag
Colombia
-
Canada
CAN flag
Golf
Golf
Le Golf National
12:30
Men's Round 1
Handball
Handball
South Paris Arena 6
00:30
Men's Preliminary Round Group B
DEN flag
Denmark
-
Argentina
ARG flag
12:30
Women's Preliminary Round Group B
NED flag
Netherlands
-
Brazil
BRA flag
14:30
Women's Preliminary Round Group A
KOR flag
Korea
-
Sweden
SWE flag
17:30
Women's Preliminary Round Group B
ESP flag
Spain
-
Hungary
HUN flag
19:30
Women's Preliminary Round Group B
ANG flag
Angola
-
France
FRA flag
22:30
Women's Preliminary Round Group A
GER flag
Germany
-
Denmark
DEN flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Men's Pool B
IND flag
India
-
Belgium
BEL flag
14:00
Men's Pool B
NZL flag
New Zealand
-
Australia
AUS flag
16:15
Men's Pool A
FRA flag
France
-
Great Britain
GBR flag
16:45
Men's Pool B
ARG flag
Argentina
-
Ireland
IRL flag
20:30
Women's Pool B
USA flag
United States
-
Great Britain
GBR flag
21:00
Women's Pool B
ESP flag
Spain
-
South Africa
RSA flag
23:15
Women's Pool A
JPN flag
Japan
-
France
FRA flag
23:45
Women's Pool B
ARG flag
Argentina
-
Australia
AUS flag
Judo
Judo
Champ-de-Mars Arena
13:30
Men -100 kg Elimination Round of 64
13:30
Women -78 kg Elimination Round of 64
13:58
Men -100 kg Elimination Round of 32
13:58
Women -78 kg Elimination Round of 32
15:50
Men -100 kg Elimination Round of 16
15:50
Women -78 kg Elimination Round of 16
16:46
Men -100 kg Quarterfinals
16:46
Women -78 kg Quarterfinals
19:30
Men -100 kg Repechage
19:47
Men -100 kg Semifinals
20:04
Women -78 kg Repechage
20:21
Women -78 kg Semifinals
20:48
Men -100 kg Contest for Bronze Medal A
20:58
Men -100 kg Contest for Bronze Medal B
21:08
Men -100 kg Final
21:19
Women -78 kg Contest for Bronze Medal A
21:29
Women -78 kg Contest for Bronze Medal B
21:39
Women -78 kg Final
Rowing
Rowing
Nautical St - Flat water
13:00
Women's Single Sculls Semifinal A/B 1
13:10
Women's Single Sculls Semifinal A/B 2
13:20
Men's Single Sculls Semifinal A/B 1
13:30
Men's Single Sculls Semifinal A/B 2
13:40
Women's Eight Repechages
13:50
Men's Eight Repechages
14:00
Women's Double Sculls Final B
14:12
Men's Double Sculls Final B
14:24
Women's Four Final B
14:36
Men's Four Final B
14:48
Women's Double Sculls Final A
15:00
Men's Double Sculls Final A
15:20
Women's Four Final A
15:40
Men's Four Final A
Sailing
Sailing
Marseille Marina
15:30
Men's Skiff Medal Race
15:30
Women's Skiff Medal Race
15:30
Men's Dinghy - Race 1
15:30
Men's Dinghy - Race 2
15:30
Women's Dinghy - Race 1
15:30
Women's Dinghy - Race 2
15:30
Women's Windsurfing - Race 17
15:30
Women's Windsurfing - Race 18
15:30
Women's Windsurfing - Race 19
15:30
Women's Windsurfing - Race 20
15:30
Men's Windsurfing - Race 17
15:30
Men's Windsurfing - Race 18
15:30
Men's Windsurfing - Race 19
15:30
Men's Windsurfing - Race 20
Shooting
Shooting
Chateauroux Shooting Ctr
13:00
50m Rifle 3 Positions Men's Final
15:30
50m Rifle 3 Pos. Women's Qualification
Swimming
Swimming
Paris La Defense Arena
00:00
Women's 100m Freestyle Final
00:06
Men's 200m Butterfly Final
00:12
Women's 200m Butterfly Semifinals
00:34
Women's 1500m Freestyle Final
01:04
Men's 200m Backstroke Semifinals
01:16
Women's 200m Breaststroke Semifinals
01:38
Men's 200m Breaststroke Final
01:45
Men's 100m Freestyle Final
14:30
Women's 200m Backstroke - Heats
14:30
Men's 50m Freestyle - Heats
14:30
Men's 200m Individual Medley - Heats
14:30
Women's 4 x 200m Freestyle Relay - Heats
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Women's Singles Quarterfinals
15:30
Men's Singles Quarterfinal
18:30
Women's Singles Quarterfinal
19:30
Men's Singles Quarterfinals
23:30
Women's Singles Quarterfinal
Tennis
Tennis
Roland-Garros Stadium
15:30
MS Quarterfinals/WS Semifinals
15:30
MS QF/WD Semifinals/XD Semifinals
15:30
WD Semifinals/XD Semifinals
22:30
MS Quarterfinals/WS Semifinals
Volleyball
Volleyball
South Paris Arena 1
00:30
Women's Preliminary Round - Pool B
POL flag
Poland
-
Kenya
KEN flag
12:30
Women's Preliminary Round - Pool C
TUR flag
Türkiye
-
Dominican Republic
DOM flag
16:30
Women's Preliminary Round - Pool B
BRA flag
Brazil
-
Japan
JPN flag
20:30
Women's Preliminary Round - Pool C
ITA flag
Italy
-
Netherlands
NED flag
Water Polo
Water Polo
Aquatics Centre
14:00
Men's Preliminary Round - Group A
GRE flag
Greece
-
United States
USA flag
15:35
Men's Preliminary Round - Group B
SRB flag
Serbia
-
Spain
ESP flag
18:30
Men's Preliminary Round - Group B
FRA flag
France
-
Australia
AUS flag
20:05
Men's Preliminary Round - Group A
ITA flag
Italy
-
Montenegro
MNE flag
23:00
Men's Preliminary Round - Group A
ROU flag
Romania
-
Croatia
CRO flag
""",

"2-August":
"""
Archery
Archery
Invalides
13:00
Mixed Team 1/8 Elimination Round
17:45
Mixed Team Quarterfinals
19:01
Mixed Team Semifinals
19:54
Mixed Team Bronze Medal Match
20:13
Mixed Team Gold Medal Match
Athletics
Athletics
Stade de France
13:35
Men's Decathlon 100m
13:40
Men's Hammer Throw Qualification - Gp A
13:45
Women's High Jump Qualification
14:05
Women's 100m Preliminary Round
14:25
Men's Decathlon Long Jump
14:35
Men's 1500m Round 1
15:05
Men's Hammer Throw Qualification - Gp B
15:20
Women's 100m Round 1
15:45
Men's Decathlon Shot Put
21:30
Men's Decathlon High Jump
21:40
Women's 5000m Round 1
21:45
Women's Triple Jump Qualification
22:25
Women's Discus Throw Qualification-Gp A
22:40
4 x 400m Relay Mixed Round 1
23:15
Women's 800m Round 1
23:40
Men's Shot Put Qualification
23:50
Women's Discus Throw Qualification-Gp B
Badminton
Badminton
La Chapelle Arena
00:00
Mixed Doubles Semifinal
12:00
Women's Doubles Semifinal
13:10
Women's Doubles Semifinal
14:20
Men's Doubles Semifinal
15:30
Men's Doubles Semifinal
18:30
Mixed Doubles Bronze Medal Match
19:40
Mixed Doubles Gold Medal Match
21:10
Men's Singles Quarterfinal
22:20
Men's Singles Quarterfinal
23:30
Men's Singles Quarterfinal
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Women's Group Phase - Group C
BEL flag
Belgium
-
United States
USA flag
14:30
Men's Group Phase - Group B
JPN flag
Japan
-
Winner OQT LAT
BK3 flag
17:00
Men's Group Phase - Group A
AUS flag
Australia
-
Winner OQT GRE
BK1 flag
20:45
Men's Group Phase - Group A
CAN flag
Canada
-
Winner OQT ESP
BK2 flag
Basketball 3x3
Basketball 3x3
La Concorde 1
01:00
Women's Pool Round
USA flag
United States
-
Spain
ESP flag
01:30
Women's Pool Round
CAN flag
Canada
-
France
FRA flag
02:05
Men's Pool Round
SRB flag
Serbia
-
France
FRA flag
02:35
Men's Pool Round
LAT flag
Latvia
-
United States
USA flag
12:30
Women's Pool Round
GER flag
Germany
-
China
CHN flag
13:00
Women's Pool Round
AUS flag
Australia
-
Azerbaijan
AZE flag
13:35
Men's Pool Round
LTU flag
Lithuania
-
China
CHN flag
14:05
Men's Pool Round
POL flag
Poland
-
Netherlands
NED flag
16:00
Women's Pool Round
AUS flag
Australia
-
Spain
ESP flag
16:30
Women's Pool Round
FRA flag
France
-
United States
USA flag
17:05
Men's Pool Round
NED flag
Netherlands
-
Lithuania
LTU flag
17:35
Men's Pool Round
LAT flag
Latvia
-
France
FRA flag
21:00
Women's Pool Round
AZE flag
Azerbaijan
-
China
CHN flag
21:30
Women's Pool Round
CAN flag
Canada
-
United States
USA flag
22:05
Men's Pool Round
USA flag
United States
-
France
FRA flag
22:35
Men's Pool Round
SRB flag
Serbia
-
Latvia
LAT flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Preliminary Match
01:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
18:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
23:30
Men's or Women's Preliminary Match
Boxing
Boxing
North Paris Arena
00:02
Women's 66kg - Prelims - Round of 16
00:34
Women's 54kg - Quarterfinal
00:50
Men's 63.5kg - Quarterfinals
01:22
Men's 92kg - Quarterfinals
19:00
Women's 57kg - Prelims - Round of 16
20:04
Men's 51kg - Quarterfinals
20:36
Men's 80kg - Quarterfinals
21:08
Men's +92kg - Quarterfinals
23:30
Women's 57kg - Prelims - Round of 16
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Women's Kayak Cross Time Trial
20:10
Men's Kayak Cross Time Trial
Cycling BMX Racing
Cycling BMX Racing
BMX Stadium
00:10
Men, Quarterfinals Run 2
00:30
Women, Quarterfinals Run 2
00:50
Men, Quarterfinals Run 3
01:10
Women, Quarterfinals Run 3
01:35
Men, Last Chance Race
01:45
Women, Last Chance Race
23:30
Men, Semifinals Run 1
23:45
Women, Semifinals Run 1
Diving
Diving
Aquatics Centre
14:30
Men's Synchronised 3m Springboard Final
Equestrian
Equestrian
Château de Versailles
17:30
Jumping Team Final
Fencing
Fencing
Grand Palais
00:00
Women's Foil Team Gold Medal Match
17:00
Men's Épée Team Table of 8
18:30
Men's Épée Team Classifications 5-8
19:20
Men's Épée Team Semifinal 2
19:20
Men's Épée Team Semifinal 1
20:10
Men's Épée Team Placement 7-8
20:10
Men's Épée Team Placement 5-6
23:00
Men's Épée Team Bronze Medal Match
Football
Football
Multiple Venues
18:30
Men's Quarter-final
Parc des Princes
20:30
Men's Quarter-final
Lyon Stadium
22:30
Men's Quarter-final
Marseille Stadium
Golf
Golf
Le Golf National
12:30
Men's Round 2
Handball
Handball
South Paris Arena 6
00:30
Women's Preliminary Round Group A
SLO flag
Slovenia
-
Norway
NOR flag
12:30
Men's Preliminary Round Group B
HUN flag
Hungary
-
Denmark
DEN flag
14:30
Men's Preliminary Round Group B
ARG flag
Argentina
-
France
FRA flag
17:30
Men's Preliminary Round Group A
CRO flag
Croatia
-
Sweden
SWE flag
19:30
Men's Preliminary Round Group A
GER flag
Germany
-
Spain
ESP flag
22:30
Men's Preliminary Round Group A
JPN flag
Japan
-
Slovenia
SLO flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Women's Pool A
CHN flag
China
-
Germany
GER flag
14:00
Men's Pool A
NED flag
Netherlands
-
Spain
ESP flag
16:15
Women's Pool A
BEL flag
Belgium
-
Netherlands
NED flag
16:45
Men's Pool B
AUS flag
Australia
-
India
IND flag
20:30
Men's Pool B
NZL flag
New Zealand
-
Ireland
IRL flag
21:00
Men's Pool B
BEL flag
Belgium
-
Argentina
ARG flag
23:15
Men's Pool A
FRA flag
France
-
South Africa
RSA flag
23:45
Men's Pool A
GBR flag
Great Britain
-
Germany
GER flag
Judo
Judo
Champ-de-Mars Arena
13:30
Women +78 kg Elimination Round of 64
13:30
Men +100 kg Elimination Round of 64
13:58
Women +78 kg Elimination Round of 32
13:58
Men +100 kg Elimination Round of 32
15:50
Women +78 kg Elimination Round of 16
15:50
Men +100 kg Elimination Round of 16
16:46
Women +78 kg Quarterfinals
16:46
Men +100 kg Quarterfinals
19:30
Women +78 kg Repechage
19:47
Women +78 kg Semifinals
20:04
Men +100 kg Repechage
20:21
Men +100 kg Semifinals
20:48
Women +78 kg Contest for Bronze Medal A
20:58
Women +78 kg Contest for Bronze Medal B
21:08
Women +78 kg Final
21:19
Men +100 kg Contest for Bronze Medal A
21:29
Men +100 kg Contest for Bronze Medal B
21:39
Men +100 kg Final
Rowing
Rowing
Nautical St - Flat water
13:00
Men's Single Sculls Final F
13:12
Women's Single Sculls Final F
13:24
Men's Single Sculls Final E
13:36
Women's Single Sculls Final E
13:48
Men's Single Sculls Final D
14:00
Women's Single Sculls Final D
14:12
Men's Pair Final B
14:24
Women's Pair Final B
14:36
LWT Men's Double Sculls Final B
14:48
LWT Women's Double Sculls Final B
15:00
Men's Pair Final A
15:12
Women's Pair Final A
15:32
LWT Men's Double Sculls Final A
15:52
LWT Women's Double Sculls Final A
Sailing
Sailing
Marseille Marina
15:30
Mixed Dinghy - Race 1
15:30
Mixed Dinghy - Race 2
15:30
Women's Windsurfing Quarterfinal
15:30
Men's Windsurfing Quarterfinal
15:30
Women's Windsurfing Semifinal
15:30
Men's Windsurfing Semifinal
15:30
Women's Windsurfing Final
15:30
Men's Windsurfing Final
15:30
Women's Dinghy - Race 3
15:30
Women's Dinghy - Race 4
15:30
Men's Dinghy - Race 3
15:30
Men's Dinghy - Race 4
Shooting
Shooting
Chateauroux Shooting Ctr
12:30
Skeet Men's Qualification - Day 1
12:30
25m Pistol Women's Qual. Precision
13:00
50m Rifle 3 Positions Women's Final
Swimming
Swimming
Paris La Defense Arena
00:00
Women's 200m Butterfly Final
00:07
Men's 200m Backstroke Final
00:14
Men's 50m Freestyle Semifinals
00:33
Women's 200m Breaststroke Final
00:40
Women's 200m Backstroke Semifinals
01:04
Men's 200m Individual Medley Semifinals
01:18
Women's 4 x 200m Freestyle Relay Final
14:30
Men's 100m Butterfly - Heats
14:30
Women's 200m Individual Medley - Heats
14:30
Women's 800m Freestyle - Heats
14:30
Mixed 4 x 100m Medley Relay - Heats
Table Tennis
Table Tennis
South Paris Arena 4
00:30
Men's Singles Quarterfinal
13:30
Women's Singles Semifinal
14:30
Men's Singles Semifinal
17:00
Women's Singles Semifinal
18:00
Men's Singles Semifinal
Tennis
Tennis
Roland-Garros Stadium
15:30
Men's Singles Semi-final
15:30
Women's Singles Bronze Medal Match
15:30
Men's Doubles Bronze Medal Match
15:30
Mixed Doubles Bronze Medal Match
22:30
Men's Singles Semi-final
22:30
Mixed Doubles Gold Medal Match
Trampoline
Trampoline
Bercy Arena
15:30
Women's Qualification
17:20
Women's Final
21:30
Men's Qualification
23:15
Men's Final
Volleyball
Volleyball
South Paris Arena 1
00:30
Women's Preliminary Round - Pool A
FRA flag
France
-
China
CHN flag
12:30
Men's Preliminary Round - Pool C
ARG flag
Argentina
-
Germany
GER flag
16:30
Men's Preliminary Round - Pool B
BRA flag
Brazil
-
Egypt
EGY flag
20:30
Men's Preliminary Round - Pool A
FRA flag
France
-
Slovenia
SLO flag
Water Polo
Water Polo
Aquatics Centre
00:35
Men's Preliminary Round - Group B
HUN flag
Hungary
-
Japan
JPN flag
17:30
Women's Preliminary Round - Group A
AUS flag
Australia
-
Canada
CAN flag
19:05
Women's Preliminary Round - Group B
GRE flag
Greece
-
Italy
ITA flag
22:00
Women's Preliminary Round - Group B
USA flag
United States
-
France
FRA flag
23:35
Women's Preliminary Round - Group A
CHN flag
China
-
Hungary
HUN flag
""",

"3-August":
"""
Archery
Archery
Invalides
13:00
Women's Individual 1/8 Elimination Round
16:30
Women's Individual Quarterfinals
17:22
Women's Individual Semifinals
18:03
Women's Individual Bronze Medal Match
18:16
Women's Individual Gold Medal Match
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
19:00
Men's Floor Exercise Final
19:50
Women's Vault Final
20:40
Men's Pommel Horse Final
Athletics
Athletics
Stade de France
00:20
Men's Decathlon 400m
00:50
Men's 10,000m Final
13:35
Men's Decathlon 110m Hurdles
13:40
Men's Pole Vault Qualification
14:05
Men's 100m Preliminary Round
14:25
Men's Decathlon Discus Throw - Group A
14:40
Women's 800m Repechage Round
15:15
Men's 100m Round 1
15:30
Men's Decathlon Discus Throw - Group B
17:10
Men's Decathlon Pole Vault
22:40
Men's Decathlon Javelin Throw - Group A
22:45
Men's 1500m Repechage Round
23:05
Men's Shot Put Final
23:20
Women's 100m Semi-Final
23:40
Men's Decathlon Javelin Throw - Group B
23:50
Women's Triple Jump Final
Badminton
Badminton
La Chapelle Arena
00:40
Men's Singles Quarterfinal
12:00
Women's Singles Quarterfinal
13:10
Women's Singles Quarterfinal
14:20
Women's Singles Quarterfinal
15:30
Women's Singles Quarterfinal
18:30
Women's Doubles Bronze Medal Match
19:40
Women's Doubles Gold Medal Match
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Men's Group Phase - Group B
FRA flag
France
-
Germany
GER flag
14:30
Women's Group Phase - Group A
CHN flag
China
-
Puerto Rico
PUR flag
17:00
Women's Group Phase - Group A
SRB flag
Serbia
-
Spain
ESP flag
20:45
Men's Group Phase - Group C
BK4 flag
Winner OQT PUR
-
United States
USA flag
Basketball 3x3
Basketball 3x3
La Concorde 1
00:30
Women's Pool Round
ESP flag
Spain
-
Canada
CAN flag
01:00
Women's Pool Round
GER flag
Germany
-
France
FRA flag
01:35
Men's Pool Round
POL flag
Poland
-
Serbia
SRB flag
02:05
Men's Pool Round
CHN flag
China
-
United States
USA flag
21:00
Women's Pool Round
CAN flag
Canada
-
Azerbaijan
AZE flag
21:30
Women's Pool Round
ESP flag
Spain
-
Germany
GER flag
22:05
Women's Pool Round
FRA flag
France
-
Australia
AUS flag
22:35
Women's Pool Round
CHN flag
China
-
United States
USA flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Preliminary Match
01:30
Men's or Women's Preliminary Match
12:30
Men's or Women's Preliminary Match
13:30
Men's or Women's Preliminary Match
14:30
Men's or Women's Preliminary Match
15:30
Men's or Women's Preliminary Match
19:30
Men's or Women's Preliminary Match
20:30
Men's or Women's Preliminary Match
21:30
Men's or Women's LL round match
Boxing
Boxing
North Paris Arena
00:34
Men's 51kg - Quarterfinals
01:06
Men's 80kg - Quarterfinals
01:38
Men's +92kg - Quarterfinals
19:00
Men's 57kg - Quarterfinals
19:32
Men's 71kg - Quarterfinals
20:04
Women's 50kg - Quarterfinals
20:36
Women's 66kg - Quarterfinals
21:08
Women's 60kg - Semifinal
23:30
Men's 57kg - Quarterfinals
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Women's Kayak Cross Round 1
20:10
Men's Kayak Cross Round 1
21:35
Women's Kayak Cross Repechage
22:15
Men's Kayak Cross Repechage
Cycling BMX Racing
Cycling BMX Racing
BMX Stadium
00:00
Men, Semifinals Run 2
00:15
Women, Semifinals Run 2
00:30
Men, Semifinals Run 3
00:45
Women, Semifinals Run 3
01:05
Men, Final
01:20
Women, Final
Cycling Road
Cycling Road
Trocadéro
14:30
Men's Road Race
Equestrian
Equestrian
Château de Versailles
13:30
Dressage Team Grand Prix Special
Fencing
Fencing
Grand Palais
00:00
Men's Épée Team Gold Medal Match
16:30
Women's Sabre Team Table of 8
18:00
Women's Sabre Team Classifications 5-8
18:50
Women's Sabre Team Semifinal 2
18:50
Women's Sabre Team Semifinal 1
19:40
Women's Sabre Team Placement 7-8
19:40
Women's Sabre Team Placement 5-6
22:30
Women's Sabre Team Bronze Medal Match
23:30
Women's Sabre Team Gold Medal Match
Football
Football
Multiple Venues
00:30
Men's Quarter-final
Bordeaux Stadium
18:30
Women's Quarter-final
Parc des Princes
20:30
Women's Quarter-final
Lyon Stadium
22:30
Women's Quarter-final
Marseille Stadium
Golf
Golf
Le Golf National
12:30
Men's Round 3
Handball
Handball
South Paris Arena 6
00:30
Men's Preliminary Round Group B
NOR flag
Norway
-
Egypt
EGY flag
12:30
Women's Preliminary Round Group B
HUN flag
Hungary
-
Netherlands
NED flag
14:30
Women's Preliminary Round Group B
ESP flag
Spain
-
France
FRA flag
17:30
Women's Preliminary Round Group B
BRA flag
Brazil
-
Angola
ANG flag
19:30
Women's Preliminary Round Group A
SLO flag
Slovenia
-
Sweden
SWE flag
22:30
Women's Preliminary Round Group A
NOR flag
Norway
-
Germany
GER flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Women's Pool B
GBR flag
Great Britain
-
Argentina
ARG flag
14:00
Women's Pool A
NED flag
Netherlands
-
Japan
JPN flag
16:15
Women's Pool B
AUS flag
Australia
-
Spain
ESP flag
16:45
Women's Pool B
USA flag
United States
-
South Africa
RSA flag
20:30
Women's Pool A
CHN flag
China
-
France
FRA flag
23:15
Women's Pool A
GER flag
Germany
-
Belgium
BEL flag
Judo
Judo
Champ-de-Mars Arena
11:30
Mixed Team Preliminary Rounds
11:30
Mixed Team Elimination Round of 16
13:10
Mixed Team Quarterfinals
14:10
Mixed Team Repechage
14:45
Mixed Team Semifinals
19:30
Mixed Team Bronze Medal A
20:10
Mixed Team Bronze Medal B
20:50
Mixed Team Final
Rowing
Rowing
Nautical St - Flat water
13:00
Women's Single Sculls Final C
13:12
Men's Single Sculls Final C
13:24
Women's Single Sculls Final B
13:36
Men's Single Sculls Final B
13:48
Women's Single Sculls Final A
14:00
Men's Single Sculls Final A
14:20
Women's Eight Final A
14:40
Men's Eight Final A
Sailing
Sailing
Marseille Marina
13:00
Men's Dinghy - Race 5
13:00
Men's Dinghy - Race 6
13:00
Women's Dinghy - Race 5
13:00
Women's Dinghy - Race 6
13:00
Mixed Multihull - Race 1
13:00
Mixed Multihull - Race 2
13:00
Mixed Multihull - Race 3
13:00
Mixed Dinghy - Race 3
13:00
Mixed Dinghy - Race 4
Shooting
Shooting
Chateauroux Shooting Ctr
13:00
Skeet Men's Qualification - Day 2
13:00
Skeet Women's Qualification - Day 1
13:00
25m Pistol Women's Final
19:00
Skeet Men's Final
Swimming
Swimming
Paris La Defense Arena
00:00
Men's 50m Freestyle Final
00:09
Women's 200m Backstroke Final
00:19
Men's 200m Individual Medley Final
00:39
Men's 100m Butterfly Semifinals
01:04
Women's 200m Ind. Medley Semifinals
14:30
Women's 50m Freestyle - Heats
14:30
Men's 1500m Freestyle - Heats
14:30
Men's 4 x 100m Medley Relay - Heats
14:30
Women's 4 x 100m Medley Relay - Heats
Table Tennis
Table Tennis
South Paris Arena 4
17:00
Women's Singles Bronze Medal Match
18:00
Women's Singles Gold Medal Match
Tennis
Tennis
Roland-Garros Stadium
13:00
Men's Singles Bronze Medal Match
13:00
Women's Singles Gold Medal Match
13:00
Men's Doubles Gold Medal Match
Volleyball
Volleyball
South Paris Arena 1
00:30
Men's Preliminary Round - Pool C
JPN flag
Japan
-
United States
USA flag
12:30
Women's Preliminary Round - Pool C
NED flag
Netherlands
-
Dominican Republic
DOM flag
16:30
Women's Preliminary Round - Pool B
JPN flag
Japan
-
Kenya
KEN flag
20:30
Men's Preliminary Round - Pool B
POL flag
Poland
-
Italy
ITA flag
Water Polo
Water Polo
Aquatics Centre
14:00
Men's Preliminary Round - Group B
ESP flag
Spain
-
Japan
JPN flag
15:35
Men's Preliminary Round - Group A
CRO flag
Croatia
-
Greece
GRE flag
18:30
Men's Preliminary Round - Group B
AUS flag
Australia
-
Hungary
HUN flag
20:05
Men's Preliminary Round - Group A
MNE flag
Montenegro
-
United States
USA flag
23:00
Men's Preliminary Round - Group B
SRB flag
Serbia
-
France
FRA flag
""",

"4-August":
"""
Archery
Archery
Invalides
13:00
Men's Individual 1/8 Elimination Round
16:30
Men's Individual Quarterfinals
17:22
Men's Individual Semifinals
18:03
Men's Individual Bronze Medal Match
18:16
Men's Individual Gold Medal Match
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
18:30
Men's Rings Final
19:10
Women's Uneven Bars Final
19:55
Men's Vault Final
Athletics
Athletics
Stade de France
00:25
4 x 400m Relay Mixed Final
00:50
Women's 100m Final
01:15
Men's Decathlon 1500m
13:35
Women's 3000m Steeplechase Round 1
13:50
Women's Hammer Throw Qualification-Gp A
14:25
Women's 200m Round 1
14:30
Men's Long Jump Qualification
15:15
Women's Hammer Throw Qualification-Gp B
15:20
Men's 110m Hurdles Round 1
16:05
Women's 400m Hurdles Round 1
22:35
Men's 400m Round 1
23:20
Women's High Jump Final
23:30
Men's 100m Semi-Final
Badminton
Badminton
La Chapelle Arena
12:00
Women's Singles Semifinal
13:10
Women's Singles Semifinal
14:20
Men's Singles Semifinal
15:30
Men's Singles Semifinal
18:30
Men's Doubles Bronze Medal Match
19:40
Men's Doubles Gold Medal Match
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Men's Group Phase - Group C
SRB flag
Serbia
-
South Sudan
SSD flag
14:30
Women's Group Phase - Group C
JPN flag
Japan
-
Belgium
BEL flag
17:00
Women's Group Phase - Group B
CAN flag
Canada
-
Nigeria
NGR flag
20:45
Women's Group Phase - Group C
GER flag
Germany
-
United States
USA flag
Basketball 3x3
Basketball 3x3
La Concorde 1
01:00
Women's Play-in Games
01:35
Women's Play-in Games
21:00
Men's Pool Round
FRA flag
France
-
China
CHN flag
21:30
Men's Pool Round
LAT flag
Latvia
-
Poland
POL flag
22:05
Men's Pool Round
SRB flag
Serbia
-
Lithuania
LTU flag
22:35
Men's Pool Round
USA flag
United States
-
Netherlands
NED flag
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's LL round match
01:30
Men's or Women's LL round match
02:30
Men's or Women's LL round match
12:30
Men's or Women's Round of 16 Match
13:30
Men's or Women's Round of 16 Match
16:30
Men's or Women's Round of 16 Match
17:30
Men's or Women's Round of 16 Match
20:30
Men's or Women's Round of 16 Match
21:30
Men's or Women's Round of 16 Match
Boxing
Boxing
North Paris Arena
00:02
Men's 71kg - Quarterfinals
00:34
Women's 50kg - Quarterfinals
01:06
Women's 66kg - Quarterfinals
01:38
Women's 60kg - Semifinal
14:30
Women's 57kg - Quarterfinals
15:02
Women's 75kg - Quarterfinals
15:34
Women's 54kg - Semifinal
15:50
Men's 51kg - Semifinal
16:06
Men's 63.5kg - Semifinal
16:22
Men's 80kg - Semifinal
16:38
Men's 92kg - Semifinal
19:00
Women's 57kg - Quarterfinals
19:32
Women's 75kg - Quarterfinals
20:04
Women's 54kg - Semifinal
20:20
Men's 51kg - Semifinal
20:36
Men's 63.5kg - Semifinal
20:52
Men's 80kg - Semifinal
21:08
Men's 92kg - Semifinal
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Men's Kayak Cross Heats
20:15
Women's Kayak Cross Heats
Cycling Road
Cycling Road
Trocadéro
17:30
Women's Road Race
Equestrian
Equestrian
Château de Versailles
13:30
Dressage Individual Grand Prix Freestyle
Fencing
Fencing
Grand Palais
15:20
Men's Foil Team Table of 8
17:10
Men's Foil Team Classifications 5-8
18:20
Men's Foil Team Semifinal 2
18:20
Men's Foil Team Semifinal 1
19:30
Men's Foil Team Placement 7-8
19:30
Men's Foil Team Placement 5-6
22:40
Men's Foil Team Bronze Medal Match
Football
Football
La Beaujoire Stadium
00:30
Women's Quarter-final
Golf
Golf
Le Golf National
12:30
Men's Round 4
Handball
Handball
South Paris Arena 6
00:30
Women's Preliminary Round Group A
DEN flag
Denmark
-
Korea
KOR flag
12:30
Men's Preliminary Round Group A
SWE flag
Sweden
-
Japan
JPN flag
14:30
Men's Preliminary Round Group B
EGY flag
Egypt
-
Argentina
ARG flag
17:30
Men's Preliminary Round Group A
GER flag
Germany
-
Slovenia
SLO flag
19:30
Men's Preliminary Round Group B
HUN flag
Hungary
-
France
FRA flag
22:30
Men's Preliminary Round Group B
DEN flag
Denmark
-
Norway
NOR flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Men's Quarter-final
16:00
Men's Quarter-final
21:00
Men's Quarter-final
23:30
Men's Quarter-final
Sailing
Sailing
Marseille Marina
15:30
Mixed Multihull - Race 4
15:30
Mixed Multihull - Race 5
15:30
Mixed Multihull - Race 6
15:30
Men's Dinghy - Race 7
15:30
Men's Dinghy - Race 8
15:30
Women's Dinghy - Race 7
15:30
Women's Dinghy - Race 8
15:30
Men's Kite - Race 1
15:30
Women's Kite - Race 1
15:30
Men's Kite - Race 2
15:30
Women's Kite - Race 2
15:30
Men's Kite - Race 3
15:30
Women's Kite - Race 3
15:30
Men's Kite - Race 4
15:30
Women's Kite - Race 4
15:30
Mixed Dinghy - Race 5
15:30
Mixed Dinghy - Race 6
Shooting
Shooting
Chateauroux Shooting Ctr
12:30
25m Rapid Fire Pistol Men's Qual-Stage 1
13:00
Skeet Women's Qualification - Day 2
19:00
Skeet Women's Final
Swimming
Swimming
Paris La Defense Arena
00:00
Men's 100m Butterfly Final
00:09
Women's 50m Freestyle Semifinals
00:29
Women's 200m Individual Medley Final
00:39
Women's 800m Freestyle Final
01:03
Mixed 4 x 100m Medley Relay Final
22:00
Women's 50m Freestyle Final
22:06
Men's 1500m Freestyle Final
22:42
Men's 4 x 100m Medley Relay Final
23:05
Women's 4 x 100m Medley Relay Final
Table Tennis
Table Tennis
South Paris Arena 4
17:00
Men's Singles Bronze Medal Match
18:00
Men's Singles Gold Medal Match
Tennis
Tennis
Roland-Garros Stadium
13:30
Women's Doubles Bronze Medal Match
13:30
Men's Singles Gold Medal Match
13:30
Women's Doubles Gold Medal Match
Volleyball
Volleyball
South Paris Arena 1
00:30
Men's Preliminary Round - Pool A
CAN flag
Canada
-
Serbia
SRB flag
12:30
Women's Preliminary Round - Pool C
ITA flag
Italy
-
Türkiye
TUR flag
16:30
Women's Preliminary Round - Pool A
FRA flag
France
-
United States
USA flag
20:30
Women's Preliminary Round - Pool A
CHN flag
China
-
Serbia
SRB flag
Water Polo
Water Polo
Aquatics Centre
00:35
Men's Preliminary Round - Group A
ITA flag
Italy
-
Romania
ROU flag
17:30
Women's Preliminary Round - Group A
HUN flag
Hungary
-
Australia
AUS flag
19:05
Women's Preliminary Round - Group B
ITA flag
Italy
-
Spain
ESP flag
22:00
Women's Preliminary Round - Group A
CAN flag
Canada
-
Netherlands
NED flag
23:35
Women's Preliminary Round - Group B
FRA flag
France
-
Greece
GRE flag
""",

"5-August":
"""
Artistic Gymnastics
Artistic Gymnastics
Bercy Arena
15:15
Men's Parallel Bars Final
16:06
Women's Balance Beam Final
17:01
Men's Horizontal Bar Final
17:50
Women's Floor Exercise Final
Artistic Swimming
Artistic Swimming
Aquatics Centre
23:00
Team Technical Routine
Athletics
Athletics
Stade de France
00:00
Men's Hammer Throw Final
00:10
Women's 800m Semi-Final
00:45
Men's 1500m Semi-Final
01:25
Men's 100m Final
13:35
Men's 400m Hurdles Round 1
13:40
Men's Discus Throw Qualification - Gp A
14:10
Women's Pole Vault Qualification
14:20
Women's 400m Hurdles Repechage Round
14:50
Men's 400m Repechage Round
15:05
Men's Discus Throw Qualification - Gp B
15:25
Women's 400m Round 1
16:20
Women's 200m Repechage Round
22:30
Men's Pole Vault Final
22:34
Men's 3000m Steeplechase Round 1
23:25
Men's 200m Round 1
Badminton
Badminton
La Chapelle Arena
13:15
Women's Singles Bronze Medal Match
14:25
Women's Singles Gold Medal Match
18:00
Men's Singles Bronze Medal Match
19:10
Men's Singles Gold Medal Match
Basketball
Basketball
Pierre Mauroy Stadium
00:30
Women's Group Phase - Group B
AUS flag
Australia
-
France
FRA flag
Basketball 3x3
Basketball 3x3
La Concorde 1
01:00
Men's Play-in Games
01:35
Men's Play-in Games
21:00
Women's Semifinal
21:30
Men's Semifinal
22:00
Women's Semifinal
22:30
Men's Semifinal
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Round of 16 Match
01:30
Men's or Women's Round of 16 Match
12:30
Men's or Women's Round of 16 Match
13:30
Men's or Women's Round of 16 Match
16:30
Men's or Women's Round of 16 Match
17:30
Men's or Women's Round of 16 Match
20:30
Men's or Women's Round of 16 Match
21:30
Men's or Women's Round of 16 Match
Canoe Slalom
Canoe Slalom
Nautical St - White water
19:00
Women's Kayak Cross Quarterfinal
19:22
Men's Kayak Cross Quarterfinal
19:45
Women's Kayak Cross Semifinal
19:58
Men's Kayak Cross Semifinal
20:13
Women's Kayak Cross Small Final
20:18
Men's Kayak Cross Small Final
20:25
Women's Kayak Cross Final
20:30
Men's Kayak Cross Final
Cycling Track
Cycling Track
National Velodrome
20:30
Women's Team Sprint, Qualifying
20:57
Men's Team Pursuit, Qualifying
22:25
Women's Team Sprint, First Round
22:39
Men's Team Sprint, Qualifying
23:16
Women's Team Sprint, Final for place 7-8
23:19
Women's Team Sprint, Final for place 5-6
23:23
Women's Team Sprint, Finals - For Bronze
23:28
Women's Team Sprint, Finals - For Gold
Diving
Diving
Aquatics Centre
13:30
Women's 10m Platform Preliminary
18:30
Women's 10m Platform Semifinal
Equestrian
Equestrian
Château de Versailles
17:30
Jumping Individual Qualifier
Fencing
Fencing
Grand Palais
00:00
Men's Foil Team Gold Medal Match
Football
Football
Marseille Stadium
21:30
Men's Semi-final
Handball
Handball
South Paris Arena 6
00:30
Men's Preliminary Round Group A
ESP flag
Spain
-
Croatia
CRO flag
Hockey
Hockey
Yves-du-Manoir Stadium
13:30
Women's Quarter-final
16:00
Women's Quarter-final
21:00
Women's Quarter-final
23:30
Women's Quarter-final
Sailing
Sailing
Marseille Marina
13:30
Men's Kite - Race 5
13:30
Women's Kite - Race 5
13:30
Men's Kite - Race 6
13:30
Women's Kite - Race 6
13:30
Men's Kite - Race 7
13:30
Women's Kite - Race 7
13:30
Men's Kite - Race 8
13:30
Women's Kite - Race 8
13:30
Mixed Multihull - Race 7
13:30
Mixed Multihull - Race 8
13:30
Mixed Multihull - Race 9
13:30
Women's Dinghy - Race 9
13:30
Women's Dinghy - Race 10
13:30
Men's Dinghy - Race 9
13:30
Men's Dinghy - Race 10
13:30
Mixed Dinghy - Race 7
13:30
Mixed Dinghy - Race 8
Shooting
Shooting
Chateauroux Shooting Ctr
12:30
Skeet Mixed Team Qualification
13:00
25m Rapid Fire Pistol Men's Final
18:30
Skeet Mixed Team Gold Medal
Sport Climbing
Sport Climbing
Le Bourget Climbing Venue
13:30
Men's Boulder & Lead, Semifinal Boulder
16:30
Women's Speed, Qualification - Seeding
17:10
Women's Speed, Qualification Elimination
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Team Round of 16
18:30
Men's & Women's Team Round of 16
23:30
Men's & Women's Team Round of 16
Triathlon
Triathlon
Pont Alexandre III
11:30
Mixed Relay
Volleyball
Volleyball
South Paris Arena 1
00:30
Women's Preliminary Round - Pool B
BRA flag
Brazil
-
Poland
POL flag
12:30
Men's Quarterfinals
16:30
Men's Quarterfinals
20:30
Men's Quarterfinals
Water Polo
Water Polo
Paris La Defense Arena
15:30
Men's Preliminary Round - Group B
HUN flag
Hungary
-
Serbia
SRB flag
17:05
Men's Preliminary Round - Group B
AUS flag
Australia
-
Japan
JPN flag
18:40
Men's Preliminary Round - Group A
GRE flag
Greece
-
Italy
ITA flag
22:00
Men's Preliminary Round - Group A
CRO flag
Croatia
-
United States
USA flag
23:35
Men's Preliminary Round - Group B
FRA flag
France
-
Spain
ESP flag
Wrestling
Wrestling
Champ-de-Mars Arena
18:30
MGR 60kg 1/8 Final
18:30
WFS 68kg 1/8 Final
18:30
MGR 130kg 1/8 Final
19:50
MGR 60kg 1/4 Final
19:50
WFS 68kg 1/4 Final
19:50
MGR 130kg 1/4 Final
""",

"6-August":
"""
Artistic Swimming
Artistic Swimming
Aquatics Centre
23:00
Team Free Routine
Athletics
Athletics
Stade de France
00:00
Women's Discus Throw Final
00:15
Women's 200m Semi-Final
00:40
Women's 5000m Final
01:15
Women's 800m Final
13:35
Women's 1500m Round 1
13:50
Men's Javelin Throw Qualification - Gp A
14:20
Men's 110m Hurdles Repechage Round
14:45
Women's Long Jump Qualification
14:50
Women's 400m Repechage Round
15:20
Men's Javelin Throw Qualification - Gp B
15:30
Men's 400m Hurdles Repechage Round
16:00
Men's 200m Repechage Round
23:05
Men's 400m Semi-Final
23:30
Women's Hammer Throw Final
23:37
Women's 400m Hurdles Semi-Final
23:50
Men's Long Jump Final
Basketball
Basketball
Bercy Arena
14:30
Men's Quarterfinal
18:00
Men's Quarterfinal
21:30
Men's Quarterfinal
Basketball 3x3
Basketball 3x3
La Concorde 1
00:30
Women's Bronze Medal Game
01:00
Men's Bronze Medal Game
01:35
Women's Gold Medal Game
02:05
Men's Gold Medal Game
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Round of 16 Match
01:30
Men's or Women's Round of 16 Match
20:30
Men's or Women's Quarterfinal
21:30
Men's or Women's Quarterfinal
Canoe Sprint
Canoe Sprint
Nautical St - Flat water
13:00
Men's Kayak Four 500m Heats
13:30
Women's Kayak Four 500m Heats
14:00
Men's Canoe Double 500m Heats
14:30
Women's Canoe Double 500m Heats
15:00
Men's Kayak Double 500m Heats
15:40
Women's Kayak Double 500m Heats
16:40
Men's Kayak Four 500m Quarterfinals
16:50
Women's Canoe Double 500m Quarterfinals
17:20
Men's Canoe Double 500m Quarterfinals
17:40
Women's Kayak Double 500m Quarterfinals
18:00
Men's Kayak Double 500m Quarterfinals
Cycling Track
Cycling Track
National Velodrome
21:00
Women's Team Pursuit, Qualifying
22:29
Men's Team Sprint, First Round
22:44
Men's Team Pursuit, First Round
23:25
Men's Team Sprint, Finals for places 7-8
23:28
Men's Team Sprint, Finals for places 5-6
23:32
Men's Team Sprint, Finals - For Bronze
23:37
Men's Team Sprint, Finals - For Gold
Diving
Diving
Aquatics Centre
13:30
Men's 3m Springboard Preliminary
18:30
Women's 10m Platform Final
Equestrian
Equestrian
Château de Versailles
13:30
Jumping Individual Final
Football
Football
Lyon Stadium
00:30
Men's Semi-final
21:30
Women's Semi-final
Handball
Handball
Pierre Mauroy Stadium
13:00
Women's Quarterfinal
17:00
Women's Quarterfinal
21:00
Women's Quarterfinal
Hockey
Hockey
Yves-du-Manoir Stadium
17:30
Men's Semi-final
22:30
Men's Semi-final
Sailing
Sailing
Marseille Marina
13:30
Women's Dinghy Medal Race
13:30
Men's Dinghy Medal Race
13:30
Women's Kite - Race 9
13:30
Men's Kite - Race 9
13:30
Women's Kite - Race 10
13:30
Men's Kite - Race 10
13:30
Women's Kite - Race 11
13:30
Men's Kite - Race 11
13:30
Women's Kite - Race 12
13:30
Men's Kite - Race 12
13:30
Mixed Dinghy - Race 9
13:30
Mixed Dinghy - Race 10
13:30
Mixed Multihull - Race 10
13:30
Mixed Multihull - Race 11
13:30
Mixed Multihull - Race 12
Skateboarding
Skateboarding
La Concorde 4
16:00
Women's Park Prelims
21:00
Women's Park Final
Sport Climbing
Sport Climbing
Le Bourget Climbing Venue
13:30
Women's Boulder & Lead, Semi Boulder
16:30
Men's Speed, Qualification - Seeding
17:10
Men's Speed, Qualification - Elimination
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Team Round of 16
18:30
Men's & Women's Team Quarterfinals
23:30
Men's & Women's Team Quarterfinals
Volleyball
Volleyball
South Paris Arena 1
00:30
Men's Quarterfinals
12:30
Women's Quarterfinals
16:30
Women's Quarterfinals
20:30
Women's Quarterfinals
Water Polo
Water Polo
Paris La Defense Arena
01:10
Men's Preliminary Round - Group A
ROU flag
Romania
-
Montenegro
MNE flag
17:30
Women's Quarterfinal
19:05
Women's Quarterfinal
22:30
Women's Quarterfinal
Wrestling
Wrestling
Champ-de-Mars Arena
00:30
MGR 60kg Semifinal
00:50
MGR 130kg Semifinal
01:10
WFS 68kg Semifinal
14:30
MGR 60kg Repechage
14:30
WFS 68kg Repechage
14:30
MGR 130kg Repechage
15:00
MGR 77kg 1/8 Final
15:00
WFS 50kg 1/8 Final
15:00
MGR 97kg 1/8 Final
16:20
MGR 77kg 1/4 Finals
16:20
WFS 50kg 1/4 Final
16:20
MGR 97kg 1/4 Final
21:45
MGR 77kg Semifinal
22:05
MGR 97kg Semifinal
22:25
WFS 50kg Semifinal
23:00
MGR 60kg Bronze Medal Match
23:25
MGR 60kg Final
23:35
MGR 130kg Bronze Medal Match
""",

"7-August":
"""
Artistic Swimming
Artistic Swimming
Aquatics Centre
23:00
Team Acrobatic Routine
Athletics
Athletics
Multiple Venues
00:20
Men's 1500m Final
Stade de France
00:40
Women's 3000m Steeplechase Final
Stade de France
01:10
Women's 200m Final
Stade de France
11:00
Marathon Race Walk Relay Mixed
Trocadéro
13:35
Men's High Jump Qualification
Stade de France
13:45
Women's 100m Hurdles Round 1
Stade de France
13:55
Women's Javelin Throw Qualification-Gp A
Stade de France
14:40
Men's 5000m Round 1
Stade de France
15:20
Women's Javelin Throw Qualification-Gp B
Stade de France
15:25
Men's 800m Round 1
Stade de France
16:15
Women's 1500m Repechage Round
Stade de France
22:30
Women's Pole Vault Final
Stade de France
22:35
Men's 110m Hurdles Semi-Final
Stade de France
22:45
Men's Triple Jump Qualification
Stade de France
23:05
Men's 400m Hurdles Semi-Final
Stade de France
23:32
Men's 200m Semi-Final
Stade de France
23:55
Men's Discus Throw Final
Stade de France
Basketball
Basketball
Bercy Arena
01:00
Men's Quarterfinal
14:30
Women's Quarterfinal
18:00
Women's Quarterfinal
21:30
Women's Quarterfinal
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Quarterfinal
01:30
Men's or Women's Quarterfinal
20:30
Men's or Women's Quarterfinal
21:30
Men's or Women's Quarterfinal
Boxing
Boxing
Roland-Garros Stadium
01:00
Men's 71kg - Semifinal
01:16
Men's 71kg - Semifinal
01:32
Women's 50kg - Semifinal
01:48
Women's 50kg - Semifinal
02:04
Women's 66kg - Semifinal
02:20
Women's 66kg - Semifinal
02:36
Women's 60kg - Final
Canoe Sprint
Canoe Sprint
Nautical St - Flat water
13:00
Women's Kayak Single 500m Heats
14:10
Men's Kayak Single 1000m Heats
15:10
Men's Canoe Single 1000m Heats
17:00
Women's Kayak Single 500m Quarterfinals
17:40
Men's Kayak Single 1000m Quarterfinals
18:10
Men's Canoe Single 1000m Quarterfinals
Cycling Track
Cycling Track
National Velodrome
16:15
Men's Sprint, Qualifying
16:56
Women's Keirin, First Round
17:22
Women's Team Pursuit, First Round
18:00
Men's Sprint, 1/32 Finals
18:40
Women's Keirin, Repechages
19:00
Men's Sprint, 1/32 Finals Repechages
21:00
Men's Sprint, 1/16 Finals
21:34
Men's Team Pursuit Finals for places 7-8
21:40
Men's Team Pursuit Finals for places 5-6
21:55
Men's Team Pursuit, Finals - For Bronze
22:03
Men's Team Pursuit, Finals - For Gold
22:12
Men's Sprint, 1/16 Finals Repechages
22:27
Women's Team Pursuit, Finals - For Gold
23:08
Men's Sprint, 1/8 Finals
23:44
Men's Sprint, 1/8 Finals Repechages
Diving
Diving
Aquatics Centre
13:30
Men's 3m Springboard Semifinal
18:30
Women's 3m Springboard Preliminary
Football
Football
Marseille Stadium
00:30
Women's Semi-final
Golf
Golf
Le Golf National
12:30
Women's Round 1
Handball
Handball
Pierre Mauroy Stadium
01:00
Women's Quarterfinal
13:00
Men's Quarterfinal
17:00
Men's Quarterfinal
21:00
Men's Quarterfinal
Hockey
Hockey
Yves-du-Manoir Stadium
17:30
Women's Semi-final
22:30
Women's Semi-final
Sailing
Sailing
Marseille Marina
13:00
Mixed Multihull Medal Race
13:00
Mixed Dinghy Medal Race
13:00
Women's Kite - Race 13
13:00
Men's Kite - Race 13
13:00
Women's Kite - Race 14
13:00
Men's Kite - Race 14
13:00
Women's Kite - Race 15
13:00
Men's Kite - Race 15
13:00
Women's Kite - Race 16
13:00
Men's Kite - Race 16
Skateboarding
Skateboarding
La Concorde 4
16:00
Men's Park Prelims
21:00
Men's Park Final
Sport Climbing
Sport Climbing
Le Bourget Climbing Venue
13:30
Men's Boulder & Lead, Semifinal - Lead
15:58
Women's Speed, Quarterfinals
16:16
Women's Speed, Semifinals
16:25
Women's Speed, Final
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's & Women's Team Quarterfinals
18:30
Men's & Women's Team Quarterfinals
23:30
Men's Team Semifinal
Taekwondo
Taekwondo
Grand Palais
12:30
Women -49kg Round of 16
12:40
Men -58kg Round of 16
18:00
Women -49kg Quarterfinals
18:10
Men -58kg Quarterfinals
19:41
Women -49kg Semifinals
19:54
Men -58kg Semifinals
23:00
Women -49kg Repechage
23:10
Men -58kg Repechage
23:49
Women -49kg Bronze Medal Contests
Volleyball
Volleyball
South Paris Arena 1
00:30
Women's Quarterfinals
19:30
Men's Semifinals
23:30
Men's Semifinals
Water Polo
Water Polo
Paris La Defense Arena
00:05
Women's Quarterfinal
17:30
Men's Quarterfinal
19:05
Men's Quarterfinal
22:30
Men's Quarterfinal
Weightlifting
Weightlifting
South Paris Arena 6
18:30
Men's 61kg
23:00
Women's 49kg
Wrestling
Wrestling
Champ-de-Mars Arena
00:00
MGR 130kg Final
00:20
WFS 68kg Bronze Medal Match
00:45
WFS 68kg Final
14:30
MGR 77kg Repechage
14:30
WFS 50kg Repechage
14:30
MGR 97kg Repechage
15:00
MGR 67kg 1/8 Finals
15:00
WFS 53kg 1/8 Final
15:00
MGR 87kg 1/8 Final
16:20
MGR 67kg 1/4 Finals
16:20
WFS 53kg 1/4 Final
16:20
MGR 87kg 1/4 Final
21:45
MGR 67kg Semifinal
22:05
MGR 87kg Semifinal
22:25
WFS 53kg Semifinal
23:00
MGR 77kg Bronze Medal Match
23:25
MGR 77kg Final
23:35
MGR 97kg Bronze Medal Match
""",

"8-August":
"""
Athletics
Athletics
Stade de France
00:15
Women's 400m Semi-Final
00:50
Men's 400m Final
01:10
Men's 3000m Steeplechase Final
13:35
Women's Heptathlon 100m Hurdles
13:55
Women's Shot Put Qualification
14:05
Women's 100m Hurdles Repechage Round
14:35
Women's Heptathlon High Jump
14:40
Women's 4 x 100m Relay Round 1
15:05
Men's 4 x 100m Relay Round 1
15:30
Men's 800m Repechage Round
23:05
Women's 1500m Semi-Final
23:05
Women's Heptathlon Shot Put
23:30
Women's Long Jump Final
23:55
Men's Javelin Throw Final
Basketball
Basketball
Bercy Arena
01:00
Women's Quarterfinal
21:00
Men's Semifinal
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Quarterfinal
01:30
Men's or Women's Quarterfinal
20:30
Men's or Women's Semifinal
21:30
Men's or Women's Semifinal
Boxing
Boxing
Roland-Garros Stadium
01:00
Women's 57kg - Semifinal
01:16
Women's 57kg - Semifinal
01:32
Men's +92kg - Semifinal
01:48
Men's +92kg - Semifinal
02:04
Men's 63.5kg - Final
02:21
Men's 80kg - Final
Canoe Sprint
Canoe Sprint
Nautical St - Flat water
14:00
Women's Canoe Single 200m Heats
14:50
Men's Canoe Double 500m Semifinal 1
15:00
Men's Canoe Double 500m Semifinal 2
15:10
Women's Kayak Four 500m Semifinal 1
15:20
Men's Kayak Four 500m Semifinal 1
15:30
Men's Kayak Four 500m Semifinal 2
16:10
Women's Canoe Single 200m Quarterfinals
16:50
Men's Canoe Double 500m Final B
17:00
Men's Canoe Double 500m Final A
17:10
Women's Kayak Four 500m Final A
17:20
Men's Kayak Four 500m Final A
Cycling Track
Cycling Track
National Velodrome
20:30
Men's Omnium, Scratch Race 1/4
20:48
Women's Keirin, Quarterfinals
21:08
Men's Omnium, Tempo Race 2/4
21:31
Men's Sprint, Quarterfinals - Race 1
21:45
Women's Keirin, Semifinals
21:55
Men's Omnium, Elimination Race 3/4
22:17
Men's Sprint, Quarterfinals - Race 2
22:31
Women's Keirin, Final for places 7-12
22:41
Women's Keirin, Final for Gold
22:48
Men's Sprint, Quarterfinals - Decider
22:57
Men's Omnium, Points Race 4/4
23:34
Men's Sprint, Final for 5th-8th Places
Diving
Diving
Aquatics Centre
13:30
Women's 3m Springboard Semifinal
18:30
Men's 3m Springboard Final
Football
Football
La Beaujoire Stadium
20:30
Men's Bronze Medal Match
Golf
Golf
Le Golf National
12:30
Women's Round 2
Handball
Handball
Pierre Mauroy Stadium
01:00
Men's Quarterfinal
20:00
Women's Semifinal
Hockey
Hockey
Yves-du-Manoir Stadium
17:30
Men's Bronze Medal Match
22:30
Men's Gold Medal Match
Marathon Swimming
Marathon Swimming
Pont Alexandre III
11:00
Women's 10km
Modern Pentathlon
Modern Pentathlon
North Paris Arena
14:30
Men's Fencing Ranking Round
18:00
Women's Fencing Ranking Round
Rhythmic Gymnastics
Rhythmic Gymnastics
La Chapelle Arena
13:30
Individual All-Around Qual - Part 1 of 2
18:30
Individual All-Around Qual - Part 2 of 2
Sailing
Sailing
Marseille Marina
15:30
Men's Kite - Semifinal A - Race 1
15:30
Men's Kite - Semifinal B - Race 1
15:30
Men's Kite - Semifinal A - Race 2
15:30
Men's Kite - Semifinal B - Race 2
15:30
Men's Kite - Semifinal A - Race 3
15:30
Men's Kite - Semifinal B - Race 3
15:30
Men's Kite - Semifinal A - Race 4
15:30
Men's Kite - Semifinal B - Race 4
15:30
Men's Kite - Semifinal A - Race 5
15:30
Men's Kite - Semifinal B - Race 5
15:30
Men's Kite - Semifinal A - Race 6
15:30
Men's Kite - Semifinal B - Race 6
13:30
Women's Kite - Semifinal A - Race 1
13:30
Women's Kite - Semifinal B - Race 1
13:30
Women's Kite - Semifinal A - Race 2
13:30
Women's Kite - Semifinal B - Race 2
13:30
Women's Kite - Semifinal A - Race 3
13:30
Women's Kite - Semifinal B - Race 3
13:30
Women's Kite - Semifinal A - Race 4
13:30
Women's Kite - Semifinal B - Race 4
13:30
Women's Kite - Semifinal A - Race 5
15:30
Women's Kite - Semifinal B - Race 5
13:30
Women's Kite - Semifinal A - Race 6
13:30
Women's Kite - Semifinal B - Race 6
13:30
Men's Kite Final - Race 1
15:30
Men's Kite Final - Race 2
15:30
Men's Kite Final - Race 3
15:30
Men's Kite Final - Race 4
15:30
Men's Kite Final - Race 5
15:30
Men's Kite Final - Race 6
15:30
Women's Kite Final - Race 1
15:30
Women's Kite Final - Race 2
15:30
Women's Kite Final - Race 3
15:30
Women's Kite Final - Race 4
15:30
Women's Kite Final - Race 5
15:30
Women's Kite Final - Race 6
Sport Climbing
Sport Climbing
Le Bourget Climbing Venue
13:30
Women's Boulder & Lead, Semifinal Lead
15:58
Men's Speed, Quarterfinals
16:16
Men's Speed, Semifinals
16:25
Men's Speed, Final
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's Team Semifinal
18:30
Women's Team Semifinal
23:30
Women's Team Semifinal
Taekwondo
Taekwondo
Grand Palais
00:05
Men -58kg Bronze Medal Contests
00:21
Women -49kg Bronze Medal Contests
00:37
Men -58kg Bronze Medal Contests
00:53
Women -49kg Gold Medal Contest
01:09
Men -58kg Gold Medal Contest
12:30
Men -68kg Round of 16
12:40
Women -57kg Round of 16
18:00
Men -68kg Quarterfinals
18:10
Women -57kg Quarterfinals
19:41
Men -68kg Semifinals
19:54
Women -57kg Semifinals
23:00
Men -68kg Repechage
23:10
Women -57kg Repechage
23:49
Men -68kg Bronze Medal Contests
Volleyball
Volleyball
South Paris Arena 1
19:30
Women's Semifinals
23:30
Women's Semifinals
Water Polo
Water Polo
Paris La Defense Arena
00:05
Men's Quarterfinal
16:30
Women's Classification 5th-8th
18:05
Women's Semifinal
21:30
Women's Classification 5th-8th
23:05
Women's Semifinal
Weightlifting
Weightlifting
South Paris Arena 6
18:30
Women's 59kg
23:00
Men's 73kg
Wrestling
Wrestling
Champ-de-Mars Arena
00:00
MGR 97kg Final
00:20
WFS 50kg Bronze Medal Match
00:45
WFS 50kg Final
14:30
MGR 67kg Repechage
14:30
WFS 53kg Repechage
14:30
MGR 87kg Repechage
15:00
MFS 57kg 1/8 Final
15:00
WFS 57kg 1/8 Final
15:00
MFS 86kg 1/8 Final
16:20
MFS 57kg 1/4 Final
16:20
WFS 57kg 1/4 Final
16:20
MFS 86kg 1/4 Final
21:45
MFS 57kg Semifinal
22:05
MFS 86kg Semifinal
22:25
WFS 57kg Semifinal
23:00
MGR 67kg Bronze Medal Match
23:25
MGR 67kg Final
23:35
MGR 87kg Bronze Medal Match
""",

"9-August":
"""
Artistic Swimming
Artistic Swimming
Aquatics Centre
23:00
Duet Technical Routine
Athletics
Athletics
Stade de France
00:00
Men's 200m Final
00:25
Women's Heptathlon 200m
00:55
Women's 400m Hurdles Final
01:15
Men's 110m Hurdles Final
13:35
Women's Heptathlon Long Jump
14:10
Women's 4 x 400m Relay Round 1
14:35
Men's 4 x 400m Relay Round 1
14:50
Women's Heptathlon Javelin Throw - Gp A
15:00
Men's 800m Semi-Final
15:35
Women's 100m Hurdles Semi-Final
16:00
Women's Heptathlon Javelin Throw - Gp B
23:00
Women's 4 x 100m Relay Final
23:10
Women's Shot Put Final
23:15
Men's 4 x 100m Relay Final
23:30
Women's 400m Final
23:40
Men's Triple Jump Final
23:45
Women's Heptathlon 800m
Basketball
Basketball
Bercy Arena
00:30
Men's Semifinal
21:00
Women's Semifinal
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's or Women's Semifinal
01:30
Men's or Women's Semifinal
Boxing
Boxing
Roland-Garros Stadium
01:00
Men's 57kg - Semifinal
01:16
Men's 57kg - Semifinal
01:32
Women's 75kg - Semifinal
01:48
Women's 75kg - Semifinal
02:04
Men's 51kg - Final
02:21
Women's 54kg - Final
Breaking
Breaking
La Concorde 1
19:30
B-Girls Round Robin
23:30
B-Girls Quarterfinal 1
23:37
B-Girls Quarterfinal 2
23:44
B-Girls Quarterfinal 3
23:51
B-Girls Quarterfinal 4
Canoe Sprint
Canoe Sprint
Nautical St - Flat water
14:00
Women's Canoe Double 500m Semifinal 1
14:10
Women's Canoe Double 500m Semifinal 2
14:20
Women's Kayak Double 500m Semifinal 1
14:30
Women's Kayak Double 500m Semifinal 2
14:40
Men's Kayak Double 500m Semifinal 1
14:50
Men's Kayak Double 500m Semifinal 2
15:00
Men's Canoe Single 1000m Semifinal 1
15:10
Men's Canoe Single 1000m Semifinal 2
16:10
Women's Canoe Double 500m Final B
16:20
Women's Canoe Double 500m Final A
16:30
Women's Kayak Double 500m Final B
16:40
Women's Kayak Double 500m Final A
16:50
Men's Kayak Double 500m Final B
17:00
Men's Kayak Double 500m Final A
17:10
Men's Canoe Single 1000m Final B
17:20
Men's Canoe Single 1000m Final A
Cycling Track
Cycling Track
National Velodrome
17:30
Women's Sprint, Qualifying
18:11
Men's Sprint, Semifinals - Race 1
18:18
Women's Sprint, 1/32 Finals
18:59
Men's Sprint, Semifinals - Race 2
19:08
Women's Sprint, 1/32 Finals Repechages
19:22
Men's Sprint, Semifinals - Decider
21:30
Men's Sprint, Finals - Race 1
21:39
Women's Madison, Final
22:32
Men's Sprint, Finals - Race 2
22:40
Women's Sprint, 1/16 Finals
23:08
Men's Sprint, Finals - Decider
23:28
Women's Sprint, 1/16 Finals Repechages
Diving
Diving
Aquatics Centre
13:30
Men's 10m Platform Preliminary
18:30
Women's 3m Springboard Final
Football
Football
Multiple Venues
18:30
Women's Bronze Medal Match
Lyon Stadium
21:30
Men's Gold Medal Match
Parc des Princes
Golf
Golf
Le Golf National
12:30
Women's Round 3
Handball
Handball
Pierre Mauroy Stadium
01:00
Women's Semifinal
20:00
Men's Semifinal
Hockey
Hockey
Yves-du-Manoir Stadium
17:30
Women's Bronze Medal Match
23:30
Women's Gold Medal Match
Marathon Swimming
Marathon Swimming
Pont Alexandre III
11:00
Men's 10km
Modern Pentathlon
Modern Pentathlon
Château de Versailles
16:30
Men's SF A Riding Show Jumping
17:10
Men's SF A Fencing Bonus Round
17:40
Men's SF A Swimming 200m Freestyle
18:10
Men's SF A Laser Run
20:30
Men's SF B Riding Show Jumping
21:10
Men's SF B Fencing Bonus Round
21:40
Men's SF B Swimming 200m Freestyle
22:10
Men's SF B Laser Run
Rhythmic Gymnastics
Rhythmic Gymnastics
La Chapelle Arena
13:30
Group All-Around Qual. - Part 1 of 2
14:45
Group All-Around Qual. - Part 2 of 2
18:00
Individual All-Around Final
Sport Climbing
Sport Climbing
Le Bourget Climbing Venue
13:45
Men's Boulder & Lead, Final - Boulder
15:58
Men's Boulder & Lead, Final - Lead
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Men's Team Bronze Medal Team Match
18:30
Men's Team Gold Medal Team Match
Taekwondo
Taekwondo
Grand Palais
00:05
Women -57kg Bronze Medal Contests
00:21
Men -68kg Bronze Medal Contests
00:37
Women -57kg Bronze Medal Contests
00:53
Men -68kg Gold Medal Contest
01:09
Women -57kg Gold Medal Contest
12:30
Women -67kg Round of 16
12:40
Men -80kg Round of 16
18:00
Women -67kg Quarterfinals
18:10
Men -80kg Quarterfinals
19:41
Women -67kg Semifinals
19:54
Men -80kg Semifinals
23:00
Women -67kg Repechage
23:10
Men -80kg Repechage
23:49
Women -67kg Bronze Medal Contests
Volleyball
Volleyball
South Paris Arena 1
19:30
Men's Bronze Medal Match
Water Polo
Water Polo
Paris La Defense Arena
16:30
Men's Classification 5th-8th
18:05
Men's Semifinal
21:30
Men's Classification 5th-8th
23:05
Men's Semifinal
Weightlifting
Weightlifting
South Paris Arena 6
18:30
Men's 89kg
23:00
Women's 71kg
Wrestling
Wrestling
Champ-de-Mars Arena
00:00
MGR 87kg Final
00:20
WFS 53kg Bronze Medal Match
00:45
WFS 53kg Final
14:30
MFS 57kg Repechage
14:30
WFS 57kg Repechage
14:30
MFS 86kg Repechage
15:00
MFS 74kg 1/8 Final
15:00
WFS 62kg 1/8 Final
15:00
MFS 125kg 1/8 Final
16:20
MFS 74kg 1/4 Final
16:20
WFS 62kg 1/4 Final
16:20
MFS 125kg 1/4 Final
21:45
MFS 74kg Semifinal
22:05
MFS 125kg Semifinal
22:25
WFS 62kg Semifinal
23:00
MFS 57kg Bronze Medal Match
23:25
MFS 57kg Final
23:35
MFS 86kg Bronze Medal Match
""",

"10-August":
"""
Artistic Swimming
Artistic Swimming
Aquatics Centre
23:00
Duet Free Routine
Athletics
Athletics
Multiple Venues
00:25
Women's 10,000m Final
Stade de France
01:15
Men's 400m Hurdles Final
Stade de France
11:30
Men's Marathon
Invalides
22:40
Men's High Jump Final
Stade de France
22:55
Men's 800m Final
Stade de France
23:10
Women's Javelin Throw Final
Stade de France
23:15
Women's 100m Hurdles Final
Stade de France
23:30
Men's 5000m Final
Stade de France
23:55
Women's 1500m Final
Stade de France
Basketball
Basketball
Bercy Arena
00:30
Women's Semifinal
14:30
Men's Bronze Medal Game
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Women's Bronze Medal Match
02:00
Women's Gold Medal Match
Boxing
Boxing
Roland-Garros Stadium
01:00
Men's 71kg - Final
01:17
Women's 50kg - Final
02:04
Men's 92kg - Final
02:21
Women's 66kg - Final
Breaking
Breaking
La Concorde 1
00:15
B-Girls Semifinal 1
00:22
B-Girls Semifinal 2
00:44
B-Girls Bronze Medal Battle
00:53
B-Girls Gold Medal Battle
19:30
B-Boys Round Robin
23:30
B-Boys Quarterfinal 1
23:37
B-Boys Quarterfinal 2
23:44
B-Boys Quarterfinal 3
23:51
B-Boys Quarterfinal 4
Canoe Sprint
Canoe Sprint
Nautical St - Flat water
14:00
Women's Kayak Single 500m Semifinal 1
14:10
Women's Kayak Single 500m Semifinal 2
14:20
Women's Kayak Single 500m Semifinal 3
14:30
Women's Kayak Single 500m Semifinal 4
14:40
Men's Kayak Single 1000m Semifinal 1
14:50
Men's Kayak Single 1000m Semifinal 2
15:10
Women's Canoe Single 200m Semifinal 1
15:20
Women's Canoe Single 200m Semifinal 2
16:10
Women's Kayak Single 500m Final C
16:20
Women's Kayak Single 500m Final B
16:30
Women's Kayak Single 500m Final A
16:40
Men's Kayak Single 1000m Final B
16:50
Men's Kayak Single 1000m Final A
17:10
Women's Canoe Single 200m Final B
17:20
Women's Canoe Single 200m Final A
Cycling Track
Cycling Track
National Velodrome
20:30
Women's Sprint, 1/8 Finals
20:49
Men's Keirin, First Round
21:20
Women's Sprint, 1/8 Finals Repechages
21:29
Men's Madison, Final
22:37
Women's Sprint, Quarterfinals - Race 1
22:51
Men's Keirin, Repechages
23:19
Women's Sprint, Quarterfinals - Race 2
23:44
Women's Sprint, Quarterfinals - Decider
Diving
Diving
Aquatics Centre
13:30
Men's 10m Platform Semifinal
18:30
Men's 10m Platform Final
Football
Football
Parc des Princes
20:30
Women's Gold Medal Match
Golf
Golf
Le Golf National
12:30
Women's Round 4
Handball
Handball
Pierre Mauroy Stadium
01:00
Men's Semifinal
13:30
Women's Bronze Medal Match
18:30
Women's Gold Medal Match
Modern Pentathlon
Modern Pentathlon
Château de Versailles
13:00
Women's SF A Riding Show Jumping
13:40
Women's SF A Fencing Bonus Round
14:10
Women's SF A Swimming 200m Freestyle
14:40
Women's SF A Laser Run
17:00
Women's SF B Riding Show Jumping
17:40
Women's SF B Fencing Bonus Round
18:10
Women's SF B Swimming 200m Freestyle
18:40
Women's SF B Laser Run
21:00
Men's Final Riding Show Jumping
21:40
Men's Final Fencing Bonus Round
22:10
Men's Final Swimming 200m Freestyle
22:40
Men's Final Laser Run
Rhythmic Gymnastics
Rhythmic Gymnastics
La Chapelle Arena
17:30
Group All-Around Final
Sport Climbing
Sport Climbing
Le Bourget Climbing Venue
13:45
Women's Boulder & Lead, Final - Boulder
15:58
Women's Boulder & Lead, Final - Lead
Table Tennis
Table Tennis
South Paris Arena 4
13:30
Women's Team Bronze Medal Team Match
18:30
Women's Team Gold Medal Team Match
Taekwondo
Taekwondo
Grand Palais
00:05
Men -80kg Bronze Medal Contests
00:21
Women -67kg Bronze Medal Contests
00:37
Men -80kg Bronze Medal Contests
00:53
Women -67kg Gold Medal Contest
01:09
Men -80kg Gold Medal Contest
12:30
Men +80kg Round of 16
12:40
Women +67kg Round of 16
18:00
Men +80kg Quarterfinals
18:10
Women +67kg Quarterfinals
19:41
Men +80kg Semifinals
19:54
Women +67kg Semifinals
23:00
Men +80kg Repechage
23:10
Women +67kg Repechage
23:49
Men +80kg Bronze Medal Contests
Volleyball
Volleyball
South Paris Arena 1
16:30
Men's Gold Medal Match
20:45
Women's Bronze Medal Match
Water Polo
Water Polo
Paris La Defense Arena
12:30
Women's Classification 7th-8th
14:05
Women's Bronze Medal Match
17:30
Women's Classification 5th-6th
19:05
Women's Gold Medal Match
23:05
Men's Classification 7th-8th
Weightlifting
Weightlifting
South Paris Arena 6
15:00
Men's 102kg
19:30
Women's 81kg
Wrestling
Wrestling
Champ-de-Mars Arena
00:00
MFS 86kg Final
00:20
WFS 57kg Bronze Medal Match
00:45
WFS 57kg Final
14:30
MFS 74kg Repechage
14:30
WFS 62kg Repechage
14:30
MFS 125kg Repechage
15:00
MFS 65kg 1/8 Final
15:00
WFS 76kg 1/8 Final
15:00
MFS 97kg 1/8 Final
16:20
MFS 65kg 1/4 Final
16:20
WFS 76kg 1/4 Final
16:20
MFS 97kg 1/4 Final
21:45
MFS 65kg Semifinal
22:05
MFS 97kg Semifinal
22:25
WFS 76kg Semifinal
23:00
MFS 74kg Bronze Medal Match
23:25
MFS 74kg Final
23:35
MFS 125kg Bronze Medal Match
""",

"11-August":
"""
Athletics
Athletics
Multiple Venues
00:42
Men's 4 x 400m Relay Final
Stade de France
00:52
Women's 4 x 400m Relay Final
Stade de France
11:30
Women's Marathon
Invalides
Basketball
Basketball
Bercy Arena
01:00
Men's Gold Medal Game
15:00
Women's Bronze Medal Game
19:00
Women's Gold Medal Game
Beach Volleyball
Beach Volleyball
Eiffel Tower Stadium
00:30
Men's Bronze Medal Match
02:00
Men's Gold Medal Match
Boxing
Boxing
Roland-Garros Stadium
01:00
Women's 57kg - Final
01:17
Men's 57kg - Final
02:04
Women's 75kg - Final
02:21
Men's +92kg - Final
Breaking
Breaking
La Concorde 1
00:15
B-Boys Semifinal 1
00:22
B-Boys Semifinal 2
00:44
B-Boys Bronze Medal Battle
00:53
B-Boys Gold Medal Battle
Cycling Track
Cycling Track
National Velodrome
14:30
Women's Omnium, Scratch Race 1/4
14:52
Women's Sprint, Semifinals - Race 1
14:59
Men's Keirin, Quarterfinals
15:20
Women's Sprint, Semifinals - Race 2
15:27
Women's Omnium, Tempo Race 2/4
15:48
Women's Sprint, Semifinals - Decider
15:55
Women's Sprint, Final for 5th-8th Places
15:59
Men's Keirin, Semifinals
16:15
Women's Sprint, Finals - Race 1
16:23
Women's Omnium, Elimination Race 3/4
16:45
Women's Sprint, Finals - Race 2
16:53
Men's Keirin, Final for places 7-12
17:02
Men's Keirin, Final for Gold
17:14
Women's Sprint, Finals - Decider
17:26
Women's Omnium, Points Race 4/4
Handball
Handball
Pierre Mauroy Stadium
12:30
Men's Bronze Medal Match
17:00
Men's Gold Medal Match
Modern Pentathlon
Modern Pentathlon
Château de Versailles
14:30
Women's Final Riding Show Jumping
15:10
Women's Final Fencing Bonus Round
15:40
Women's Final Swimming 200m Freestyle
16:10
Women's Final Laser Run
Taekwondo
Taekwondo
Grand Palais
00:05
Women +67kg Bronze Medal Contests
00:21
Men +80kg Bronze Medal Contests
00:37
Women +67kg Bronze Medal Contests
00:53
Men +80kg Gold Medal Contest
01:09
Women +67kg Gold Medal Contest
Volleyball
Volleyball
South Paris Arena 1
16:30
Women's Gold Medal Match
Water Polo
Water Polo
Paris La Defense Arena
12:30
Men's Classification 5th-6th
14:05
Men's Bronze Medal Match
17:30
Men's Gold Medal Match
Weightlifting
Weightlifting
South Paris Arena 6
00:00
Men's +102kg
15:00
Women's +81kg
Wrestling
Wrestling
Champ-de-Mars Arena
00:00
MFS 125kg Final
00:20
WFS 62kg Bronze Medal Match
00:45
WFS 62kg Final
14:30
MFS 65kg Repechage
14:30
WFS 76kg Repechage
14:30
MFS 97kg Repechage
15:30
MFS 65kg Bronze Medal Match
15:55
MFS 65kg Final
16:05
MFS 97kg Bronze Medal Match
16:30
MFS 97kg Final
16:50
WFS 76kg Bronze Medal Match
17:15
WFS 76kg Final
"""
}

# List of sports and venues

content = read_from_json(r"C:\Users\dream\IdeaProjects\kheldekho\dataset\schedule.json")
sports_list = list(content.keys())

venues_list = ['Aquatics Centre',
               'Bercy Arena',
               'Champ-de-Mars Arena',
               'Chateauroux Shooting Ctr',
               'Château de Versailles',
               'Eiffel Tower Stadium',
               'Elancourt Hill',
               'Grand Palais',
               'Invalides',
               'La Chapelle Arena',
               'La Concorde 1',
               'Marseille Marina',
               'Nautical St - White water',
               'National Velodrome',
               'North Paris Arena',
               'Paris La Defense Arena',
               'Pierre Mauroy Stadium',
               'Roland-Garros Stadium',
               'South Paris Arena 1',
               'South Paris Arena 4',
               'South Paris Arena 6',
               "Teahupo'o, Tahiti",
               'Yves-du-Manoir Stadium']


day_wise_schedule = {}
for date in data:
    lines = data[date].strip().split('\n')

    sports = list()
    cur_sport = list()
    for line in lines:
        line = line.strip()
        if line in sports_list:
            sports.append(cur_sport)
            cur_sport = list()
        cur_sport.append(line)
    if cur_sport:
        sports.append(cur_sport)

    final_sports = []
    for x in sports:
        if len(x) > 1:
            final_sports.append(x)

    sport_event_dict = {}
    for sport in final_sports:
        sport_name = sport[0]
        if sport[1] == "Multiple Venues":
            venue = None
        else:
            venue = sport[1]

        event = list()
        cur_event = list()
        for i in range(2, len(sport)):
            if re.match(r"^\d{2}:\d{2}$", sport[i]):
                if cur_event:
                    event.append(cur_event)
                cur_event = list()
            cur_event.append(sport[i])
        if cur_event:
            event.append(cur_event)
        sport_event_dict[sport_name] = {
            "Venue": venue,
            "Events": event
        }


    json_event = []

    for key, value in sport_event_dict.items():
        sport_name = key
        sport_venue = value["Venue"]
        events = value["Events"]

        if sport_venue == "Multiple Venues":
            venue = None
        else:
            venue = sport_venue

        for event in events:
            try:
                event_time = event[0]
                event_name = event[1]

                if sport_venue is None:
                    venue = event[2]
                    if len(event) > 3:
                        team_a_flag = event[3]
                        team_a = event[4]
                        team_b = event[6]
                        team_b_flag = event[7]
                        json_event.append({
                            "Sport": sport_name,
                            "Event": event_name,
                            "Team A": team_a,
                            "Team B": team_b,
                            "Time": event_time,
                            "Venue": venue
                        })
                    else:
                        json_event.append({
                            "Sport": sport_name,
                            "Event": event_name,
                            "Time": event_time,
                            "Venue": venue
                        })

                else:
                    if len(event) > 2:
                        team_a_flag = event[2]
                        team_a = event[3]
                        team_b = event[5]
                        team_b_flag = event[6]
                        json_event.append({
                            "Sport": sport_name,
                            "Event": event_name,
                            "Team A": team_a,
                            "Team B": team_b,
                            "Time": event_time,
                            "Venue": venue
                        })
                    else:
                        json_event.append({
                            "Sport": sport_name,
                            "Event": event_name,
                            "Time": event_time,
                            "Venue": venue
                        })

            except Exception as e:
                print(date)
                print(e)
                print(event)
                print(sport_name)
                print(sport_venue)
                print(events)
                raise e

    day_wise_schedule[date] = json_event

# save to a file
output = json.dumps(day_wise_schedule, indent=4)
with open(r"C:\Users\dream\IdeaProjects\kheldekho\dataset\date_schedule.json", "w") as f:
    f.write(output)

