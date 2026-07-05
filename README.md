# How to extract fonts from adobe
Adobe stores all of your fonts as basic .otf files, just named as random numbers instead of the actual font name, and without the file extension.
You can find these files on windows in
`AppData\Roaming\Adobe\CoreSync\plugins\livetype`
In that folder is a bunch of folders with cryptic names, in a random one of them your files will exists. (For me they were split across e/ and r/)
Copy your files to a folder somewhere and download the python script in this repo, if this script ever breaks, all it is doing is adding .otf to the end of the filenames, and using the library font tools to find the name from the metadata and rename them.
```
pip install fonttools
python rename_fonts.py
```

Easy!
