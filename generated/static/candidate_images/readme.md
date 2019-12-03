For pictures from democracy club

But only of our preferred candidates

`dontsplitthremainvote/ppc.py` will print out commands which will let you download the images.

After you download them, try:

```
for image in *.png; do
  convert "$image" -resize '400x400>' "$image" && optipng -o 3 "$image";
done
```

Or more likely:

```
find generated/static/candidate_images/ -cmin '-60' -type f | while read image; do convert "$image" -resize '400x400>' "$image" && optipng -o 3 "$image"; done
```
