# Groups to SCIPERs
Auto extract SCIPERs from EPFL Groups to use in EPFL WordPress.

## Install
1. `git clone` that repo and `cd` into it.
1. `python -m venv ./env`
1. `pip install -U Flask BeautifulSoup`
1. `cp secrets.py.dist secrets.py` and add your admins' scipers in `secrets.py` if needed.
1. `python extract_sciper_webapp.py`

## Usage
1. Go to groups.epfl.ch, open the page of your group, and saved it as a "HTML only".
1. Upload that file here, under "HTML webpage".
1. Select if you wish to remove admins SCIPERs. Add more SCIPERs to remove if needed.
1. Press "Upload".
1. The resulting list is to be copy-pasted in the module, under "SCIPERs".

## Why?
Because sometimes you want to have a custom order for these SCIPERs, filtering a few out, etc.
