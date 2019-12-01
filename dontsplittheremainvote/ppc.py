import os
from csv import DictReader
from collections import defaultdict
from hashlib import md5
from typing import Dict
from typing import NamedTuple
from typing import Optional

from .constituency import get_constitiuency
from .party import get_party
from .party import Party

_SITTING_MPS = []
def is_sitting_mp(democlub_id: int) -> bool:
    if not _SITTING_MPS:
        with open('data/sitting_mps/mps_by_democlub_ids.txt') as f:
            _SITTING_MPS.extend(int(dcid) for dcid in f)
    return democlub_id in _SITTING_MPS

class PPC(NamedTuple):
    party: Party
    name: str
    link: str
    social_links: Dict[str, str]
    sitting_mp: bool

    democlub_id: Optional[int]
    democlub_image_url: Optional[str]

    def image_cache_path(self):
        return 'candidate_images/{dcid}-{md5}.{ext}'.format(
            dcid=self.democlub_id,
            md5=md5(self.democlub_image_url.encode('ascii')).hexdigest(),
            ext=self.democlub_image_url.split('.')[-1])

    @property
    def image(self):
        if self.democlub_image_url is None:
            return None
        path = self.image_cache_path()
        on_disk_path = 'generated/static/' + path
        if not os.path.exists(on_disk_path):
            print('wget "{}" -O "{}"'.format(self.democlub_image_url, on_disk_path))
            return None
        return '/static/' + path


def candidate_data():
    candidates = defaultdict(list)
    with open('data/democlub-candidates/candidates-parl.2019-12-12.csv', 'r') as f:
        csvf = DictReader(f)
        for row in csvf:
            candidate_name = row['name']
            candidate_link = 'https://whocanivotefor.co.uk/person/{}/'.format(row['id'])

            assert row['post_id'].startswith('WMC:')
            ons_id = row['post_id'][4:]
            constituency = get_constitiuency(ons_id)

            party = get_party(row['party_name'])
            image_url = row['image_url']

            links = []
            if row['wikipedia_url']:
                links.append(('Wikipedia', row['wikipedia_url']))
            if row['homepage_url']:
                if row['homepage_url'].startswith("http"):
                    links.append(('Website', row['homepage_url']))
                else:
                    links.append(('Website', 'http://' + row['homepage_url']))
            if row['twitter_username']:
                links.append(('Twitter', 'https://twitter.com/' + row['twitter_username']))
            if row['facebook_page_url']:
                if row['facebook_page_url'].startswith('http'):
                    links.append(('Facebook', row['facebook_page_url']))
                else:
                    links.append(('Facebook', 'https://www.facebook.com/' + row['facebook_page_url']))
            if row['party_ppc_page_url']:
                if row['party_ppc_page_url'].startswith('http'):
                    links.append(('Candidate page', row['party_ppc_page_url']))
                else:
                    links.append(('Candidate page', 'http://' + row['party_ppc_page_url']))
            assert all(social_url.startswith('http') for _, social_url in links), links

            democlub_id = int(row['id'])

            candidates[constituency].append(PPC(
                party=party,
                name=candidate_name,
                link=candidate_link,
                social_links=links,
                sitting_mp=is_sitting_mp(democlub_id),
                democlub_id=democlub_id,
                democlub_image_url=image_url if image_url else None))
    assert len(candidates) > 600
    return candidates
