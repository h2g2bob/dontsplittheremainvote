import csv
import os.path
import subprocess
from .constituency import all_constituencies


SQLITE_COMMANDS = b'''
create table postcodes (
    postcode text unique primary key not null,
    slug text not null);
.mode csv
.import /tmp/postcode_to_constituency.csv postcodes
vacuum
'''
def make_sqlite():
    filename = 'generated/postcodes.sqlite3'
    tmpfile='/tmp/postcode_to_constituency.csv'

    if os.path.exists(filename):
        # this takes ages
        return

    if not os.path.exists(tmpfile):
        postcodes_to_file(tmpfile)

    proc = subprocess.Popen(
        ['sqlite3', filename],
        stdin=subprocess.PIPE)
    proc.communicate(SQLITE_COMMANDS)
    if proc.returncode != 0:
        raise ValueError(proc.returncode)

def postcodes_to_file(filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(postcode_to_constituency())

def postcode_to_constituency():
    for constituency in all_constituencies():
        filename="data/postcodes/{}.csv".format(constituency.ons_id)
        for postcode in postcodes_from_file(filename):
            yield postcode, constituency.slug


def postcodes_from_file(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            postcode = row["Postcode"]
            postcode = postcode.upper().replace(" ", "")
            yield postcode
