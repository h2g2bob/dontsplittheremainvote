Parliamentary constituency postcodes

By Chris Bell

From https://www.doogal.co.uk/ElectoralConstituencies.php

```
Contains OS data © Crown copyright and database rights 2019
Contains Royal Mail data © Royal Mail copyright and database rights 2019
Contains National Statistics data © Crown copyright and database rights 2019
```

```
wget 'https://www.doogal.co.uk/ElectoralConstituenciesCSV.ashx' -O locations.csv

cat locations.csv | tail -n +2 | grep -E -o '[^,]+$' | while read code; do
  url="https://www.doogal.co.uk/ElectoralConstituenciesCSV.ashx?constituency=${code}"
  file="${code}.csv"
  [ -e "${file}" ] || wget "${url}" -O "${file}"
done
```
