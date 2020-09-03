# HanDic.py
A Python script for using the CC-CEDICT Chinese dictionary file offline.

Requires the CC-CEDICT file to use. Available on the MDBG dictionary
website:
https://www.mdbg.net/chinese/dictionary?page=cedict

Inspired by the bash script on this page:
https://mandarinportal.com/a-script-to-easily-search-traditional-chinese-words-with-cc-cedict-in-linux/

There are two versions: `handic.py` and `handic_lite.py`. The lite version
removes the use of regex in the script, avoiding an error that occurs
on some systems with the standard version, and is also formatted for ease
of use on narrower terminals such as on phones or very small screens.

### Usage
To use, simply place the CC-CEDICT file named as `cedict_ts.u8` in the
same directory and run `python3 handic.py`.

### Changes
Feel free to suggest changes, though my Python abilities are very limited
so I can unfortunately make no promises.

If I can spare the time, I plan to make a graphical version at some point.

### Disclaimer
This is likely not good code, nor the simplest or most practical way of
going about making such a program. I make no guarantee it will even run,
and take no responsibility for any damage or frustration caused by trying
to make it work.
