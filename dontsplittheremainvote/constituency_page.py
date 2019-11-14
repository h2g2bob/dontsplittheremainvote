from .analysis import Analysis
from .analysis import get_analysis
from .analysis import outcome_frequency
from .constituency import all_constituencies
from .constituency import Constituency
from .dataset import Dataset
from .other_sites import Aggregation
from .other_sites import OtherSiteSuggestion
from .other_sites import dontsplit_suggestion
from .pacts import Pact
from .party import ANYPARTY
from .ppc import PPC
from .result import Result
from collections import defaultdict
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Tuple

class ConstituencyPage(NamedTuple):
    constituency: Constituency
    datasets: Dict[Dataset, Result]
    other_site_suggestions: List[OtherSiteSuggestion]
    known_ppc: List[PPC]
    pacts: List[Pact]

    @property
    def datasets_election(self):
        return {
            dset: result
            for (dset, result) in self.datasets.items()
            if dset.election_result}

    @property
    def datasets_polling(self):
        return {
            dset: result
            for (dset, result) in self.datasets.items()
            if not dset.election_result}

    @property
    def analysis(self) -> Analysis:
        """From the set of results/outcomes we modelled, return
        an Advice of who to vote for.
        """
        return get_analysis(self.datasets, self.constituency)

    @property
    def aggregation(self) -> Aggregation:
        """From the list of other_site suggestions (plus our own
        suggestion), return an Advice of who to vote for.
        """
        recommendations = defaultdict(int)
        for suggest in self.other_sites_plus_dontsplit:
            recommendations[suggest.party] += 1
        num_any_party = recommendations.pop(ANYPARTY, 0)
        num_recommendations = sum(recommendations.values())

        if num_any_party > num_recommendations:
            return Aggregation(
                template='anyparty.html',
                provisional=num_any_party < 3)

        if num_recommendations < 2:
            return Aggregation(
                template='pending.html')

        # if over 70% of peoples recommendations are for one party, suggest that
        major_rec = [pty for pty, count in recommendations.items() if float(count)/num_recommendations > 0.7]

        if major_rec:
            [party] = major_rec
            if party.short == 'other':
                raise ValueError((self.other_sites_plus_dontsplit, self.constituency))
            return Aggregation(
                party=party,
                template='vote-{}.html'.format(party.short),
                provisional=num_recommendations < 3)

        return Aggregation(
            template='contradict.html')

    @property
    def other_sites_plus_dontsplit(self) -> List[OtherSiteSuggestion]:
        analysis = self.analysis
        if analysis.we_recommend_party is not None:
                our_site_suggestion = [dontsplit_suggestion(analysis.we_recommend_party, self.constituency)]
        else:
                our_site_suggestion = []
        return self.other_site_suggestions + our_site_suggestion

    @property
    def outcomes(self):
        return outcome_frequency(self.datasets.values())

    def most_winning_remain_party(self):
        """Which remain party has the most "wins" or "wins if we have an alliance"
        (This gives a weak suggestion of who we would suggest people vote for)
        """
        remain_wins_per_party = defaultdict(int)
        for result in self.datasets.values():
            main_remain_party = result.classify.remain_allicance_leader_as_party()
            if main_remain_party is not None:
                remain_wins_per_party[main_remain_party] += 1
        total = float(sum(remain_wins_per_party.values()))
        over_half_remain_wins = [
            party
            for party, count in remain_wins_per_party.items()
            if count / total > 0.5]
        if over_half_remain_wins:
            [main_remain_party] = over_half_remain_wins
            return main_remain_party
        else:
            return None

    def as_json(self):
        return {
            'constituency': self.constituency.as_json(),
            'analysis': self.analysis.as_json(),
            'aggregation': self.aggregation.as_json(),
            'outcome_frequency': [
                [classify_result.as_json(), outcome_freq]
                for classify_result, outcome_freq in self.outcomes],
            'other_sites': [
                other_site_suggestion.as_json()
                for other_site_suggestion in self.other_site_suggestions],
            'pacts': [
                pact.as_json()
                for pact in self.pacts],
        }
