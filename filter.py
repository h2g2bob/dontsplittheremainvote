# cd /tmp
# git clone ~/code/dontsplittheremainvote
# cd dontsplittheremainvote/
# git filter-branch -f --index-filter 'git ls-files | grep -v 'data.json' | xargs -d "\n" git rm --cached' HEAD
# git filter-branch -f --prune-empty
# git filter-branch -f --prune-empty --tree-filter 'python3 /tmp/dontsplittheremainvote/filter.py "$GIT_COMMITTER_DATE" >> /tmp/recomend_by_date.csv'

import csv
import json
import sys

def foo():
    [date] = sys.argv[1:]
    
    with open('generated/data.json') as f:
        data = json.load(f)
    
        for con_name, con_data in data['constituencies'].items():
            con_output = []
            con_output.append(date)
            con_output.append(con_data['constituency']['slug'])
            con_output.append(con_data['constituency']['ons_id'])
    
            for site in con_data['other_sites']:
                yield con_output + [
                    site['who_suggests'],
                    site['party'],
                    site.get('important', None),
                    site.get('they_say', None)]

spamwriter = csv.writer(sys.stdout)
for row in foo():
    spamwriter.writerow(row)
