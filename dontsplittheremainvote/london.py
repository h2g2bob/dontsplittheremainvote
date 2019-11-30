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
