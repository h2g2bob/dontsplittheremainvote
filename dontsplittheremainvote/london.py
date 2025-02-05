"""London doesn't have counties, but a list of 80 constituencies is not very good.

We can use NUTS-2 regions as "counties"
"""
INNER_WEST='Inner West London'
INNER_EAST='Inner East London'
OUTER_EAST='East and North East London'
OUTER_SOUTH='South London'
OUTER_WEST='West and North West London'
LONDON_COUNTY = {
    'barking': OUTER_EAST,
    'battersea': INNER_WEST,
    'beckenham': OUTER_SOUTH,
    'bermondsey-and-old-southwark': INNER_EAST,
    'bethnal-green-and-bow': INNER_EAST,
    'bexleyheath-and-crayford': OUTER_EAST,
    'brent-central': OUTER_WEST,
    'brent-north': OUTER_WEST,
    'brentford-and-isleworth': OUTER_WEST,
    'bromley-and-chislehurst': OUTER_SOUTH,
    'camberwell-and-peckham': INNER_EAST,
    'carshalton-and-wallington': OUTER_SOUTH,
    'chelsea-and-fulham': INNER_WEST,
    'chingford-and-woodford-green': OUTER_EAST,
    'chipping-barnet': OUTER_WEST,
    'cities-of-london-and-westminster': INNER_WEST,
    'croydon-central': OUTER_SOUTH,
    'croydon-north': OUTER_SOUTH,
    'croydon-south': OUTER_SOUTH,
    'dagenham-and-rainham': OUTER_EAST,
    'dulwich-and-west-norwood': INNER_EAST,
    'ealing-central-and-acton': OUTER_WEST,
    'ealing-north': OUTER_WEST,
    'ealing-southall': OUTER_WEST,
    'east-ham': INNER_EAST,
    'edmonton': OUTER_EAST,
    'eltham': OUTER_EAST,
    'enfield-north': OUTER_EAST,
    'enfield-southgate': OUTER_EAST,
    'erith-and-thamesmead': OUTER_EAST,
    'feltham-and-heston': OUTER_WEST,
    'finchley-and-golders-green': OUTER_WEST,
    'greenwich-and-woolwich': OUTER_EAST,
    'hackney-north-and-stoke-newington': INNER_EAST,
    'hackney-south-and-shoreditch': INNER_EAST,
    'hammersmith': INNER_WEST,
    'hampstead-and-kilburn': INNER_WEST,
    'harrow-east': OUTER_WEST,
    'harrow-west': OUTER_WEST,
    'hayes-and-harlington': OUTER_WEST,
    'hendon': OUTER_WEST,
    'holborn-and-st-pancras': INNER_WEST,
    'hornchurch-and-upminster': OUTER_EAST,
    'hornsey-and-wood-green': INNER_EAST,
    'ilford-north': OUTER_EAST,
    'ilford-south': OUTER_EAST,
    'islington-north': INNER_EAST,
    'islington-south-and-finsbury': INNER_EAST,
    'kensington': INNER_WEST,
    'kingston-and-surbiton': OUTER_SOUTH,
    'lewisham-east': INNER_EAST,
    'lewisham-west-and-penge': INNER_EAST,
    'lewisham-deptford': INNER_EAST,
    'leyton-and-wanstead': OUTER_EAST,
    'mitcham-and-morden': OUTER_SOUTH,
    'old-bexley-and-sidcup': OUTER_EAST,
    'orpington': OUTER_SOUTH,
    'poplar-and-limehouse': INNER_EAST,
    'putney': INNER_WEST,
    'richmond-park': OUTER_WEST,
    'romford': OUTER_EAST,
    'ruislip-northwood-and-pinner': OUTER_WEST,
    'streatham': INNER_EAST,
    'sutton-and-cheam': OUTER_SOUTH,
    'tooting': INNER_WEST,
    'tottenham': INNER_EAST,
    'twickenham': OUTER_WEST,
    'uxbridge-and-south-ruislip': OUTER_WEST,
    'vauxhall': INNER_EAST,
    'walthamstow': OUTER_EAST,
    'west-ham': INNER_EAST,
    'westminster-north': INNER_WEST,
    'wimbledon': OUTER_SOUTH,
}

SCOT_E = "Eastern Scotland"
SCOT_SW = "South Western Scotland"
SCOT_NE = "North Eastern Scotland"
SCOT_HI = "Highlands and Islands"
SCOTLAND = {
    "aberdeen-north": SCOT_NE,
    "aberdeen-south": SCOT_NE,
    "airdrie-and-shotts": SCOT_SW,
    "angus": SCOT_E,
    "argyll-and-bute": SCOT_HI,
    "ayr-carrick-and-cumnock": SCOT_SW,
    "banff-and-buchan": SCOT_NE,
    "berwickshire-roxburgh-and-selkirk": SCOT_E,
    "caithness-sutherland-and-easter-ross": SCOT_HI,
    "central-ayrshire": SCOT_SW,
    "coatbridge-chryston-and-bellshill": SCOT_SW,
    "cumbernauld-kilsyth-and-kirkintilloch-east": SCOT_SW,
    "dumfries-and-galloway": SCOT_SW,
    "dumfriesshire-clydesdale-and-tweeddale": SCOT_SW,
    "dundee-east": SCOT_E,
    "dundee-west": SCOT_E,
    "dunfermline-and-west-fife": SCOT_E,
    "east-dunbartonshire": SCOT_SW,
    "east-kilbride-strathaven-and-lesmahagow": SCOT_SW,
    "east-lothian": SCOT_E,
    "east-renfrewshire": SCOT_SW,
    "edinburgh-east": SCOT_E,
    "edinburgh-north-and-leith": SCOT_E,
    "edinburgh-south": SCOT_E,
    "edinburgh-south-west": SCOT_E,
    "edinburgh-west": SCOT_E,
    "na-h-eileanan-an-iar": SCOT_HI,
    "falkirk": SCOT_E,
    "glasgow-central": SCOT_SW,
    "glasgow-east": SCOT_SW,
    "glasgow-north": SCOT_SW,
    "glasgow-north-east": SCOT_SW,
    "glasgow-north-west": SCOT_SW,
    "glasgow-south": SCOT_SW,
    "glasgow-south-west": SCOT_SW,
    "glenrothes": SCOT_E,
    "gordon": SCOT_E,
    "inverclyde": SCOT_SW,
    "inverness-nairn-badenoch-and-strathspey": SCOT_HI,
    "kilmarnock-and-loudoun": SCOT_SW,
    "kirkcaldy-and-cowdenbeath": SCOT_E,
    "lanark-and-hamilton-east": SCOT_SW,
    "linlithgow-and-east-falkirk": SCOT_E,
    "livingston": SCOT_E,
    "midlothian": SCOT_E,
    "moray": SCOT_HI,
    "motherwell-and-wishaw": SCOT_SW,
    "north-ayrshire-and-arran": SCOT_SW,
    "north-east-fife": SCOT_E,
    "ochil-and-south-perthshire": SCOT_E,
    "orkney-and-shetland": SCOT_HI,
    "paisley-and-renfrewshire-north": SCOT_SW,
    "paisley-and-renfrewshire-south": SCOT_SW,
    "perth-and-north-perthshire": SCOT_E,
    "ross-skye-and-lochaber": SCOT_HI,
    "rutherglen-and-hamilton-west": SCOT_SW,
    "stirling": SCOT_E,
    "west-aberdeenshire-and-kincardine": SCOT_NE,
    "west-dunbartonshire": SCOT_SW,
}
