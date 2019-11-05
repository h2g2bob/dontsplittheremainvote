# dontsplittheremainvote.com

The aims are to identify areas where: 

- remain parties working together could affect the result; and
- there is only one remain party which could win (under a variety of assumptions)

And in those areas, advise that a coalition would be helpful.


## Design choices

It's a static html website, which means it looks bad. On the plus side, it's difficult to make it fall over.

The only dynamic bit is postcodes.php, which uses a sqlite database file full of postcodes.


## Building it

Run:

```
python3 -m dontsplithteremainvote
```

and it will read a bunch of CSV spreadsheets and generate some html files from jinja2 templates.

You'll probably want to comment out `make_sqlite()` in `dontsplittheremainvote/generate_pages.py`.

Or: `wget 'https://dontsplittheremainvote.com/postcodes.sqlite3' -O generated/` to download the 130MB postcode database.


## Updating external sources

Run this to update the files in `data/`.

```
./update_extenral.sh
```

It does nothing if you updates less than 2 hours ago, which lets you
`./update_extenral.sh && python3 -m dontsplithteremainvote` every time


## Deployment

Make `config.sh` containing `RSYNC_LOCATION="XXXX@XXXX:dontsplittheremainvote.com/"`

And run `./do_rsync.sh`
