import csv
import sys
from collections import defaultdict

def main():
    [_cmd, filename] = sys.argv

    votes_by_area = defaultdict(list)
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            votes_by_area[row['ons_id']].append(int(row['votes']))

    votes_for_mp = 0
    total_votes = 0
    total_mp = 0
    minority_votes_mp = 0
    for votes in votes_by_area.values():
        votes_for_mp += max(votes)
        total_votes += sum(votes)
        total_mp += 1
        minority_votes_mp += 1 if (max(votes) / sum(votes)) < 0.5 else 0

    print('votes_for_mp={}'.format(votes_for_mp))
    print('total_votes={}'.format(total_votes))
    print('votes_for_mp_pct={}'.format(100 * votes_for_mp / total_votes))

    print('mps_elected_on_minority_vote={} / {}'.format(minority_votes_mp, total_mp))

    print('worst_mps={}'.format(tuple(sorted([(max(votes) / sum(votes), onsid) for onsid, votes in votes_by_area.items()]))[:20]))

if __name__ == '__main__':
    main()
