# Best for Britain

```
wget https://getvoting.org/NewData.json
```

```
grep -F Reco data/getvoting/NewData.json | cut -d : -f 2 | sort | uniq
 "Anna Soubry",
 "Antoinette Sandbach",
 "David Gauke",
 "Dominic Grieve",
 "Green",
 "Guto Bebb",
 "Lab",
 "Lib Dem",
 "LibLab",
 "none",
 "Philip Hammond",
 "Plaid",
 "Pledge",
```
