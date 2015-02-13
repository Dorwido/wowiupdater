# wowiupdater
Easily update addons on wowinterface using the curseforge data

Its still work in progress, but I updated 3 addons of mine successfully with it.

How it works:
It fetches the addon list from here, you can then choose which addon to update it looks then on curseforge for the lateast release of that file (it skips alphas,betas) it compares then the filename of the latest release with the latest release filename from here if they match it stops if not it grabes then the filename, version, addon description (it strips out the default image if there is any and convert html to bbcode) and download the file.
Then it post here the new version, updating the version and also the addon description.

**Be aware of the part with the addon description there is currently no option to turn it off, its converted from html to bbcode**

It requires requests and html2bbcode both mentioned in the requirements.txt

How to use:
```python
python sync.py fetch # to get the addon list here
python sync.py update <addonname> #example of one of my addon python sync.py update "Flight Map Enhanced & Times"
```

Thats it.

First time you use it it will ask for you wowinterface username/password
First time you update an addon it will ask for the curseforge slug name, in the above example that would be: flight-map-enhanced

To do:
adding a changelog handler (many ppl do it different on curseforge, so there is no way todo it one way for all)
rechecking addon details before doing the update, currently it looks in the saved addon list only and even on fetch dont update existing addons only on doing an update which could lead to wrong last file name, if doing an update without the script.
