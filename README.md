# photo_manipulation
random scripts i've used for photo manipulation

Example below will do the following: 
*  Read in all photos from `src-dir`, sort them lexicographically.
*  Change the metadata timestamp to TODAY at 3AM + some millisecond offset.
*  Write the photo out to `tgt-dir`

Note:
*  You can view more options by running `change_metadata_dates.py` with the `--help` option.

```
python3 change_metadata_dates.py --src-dir src/ --tgt-dir tgt/
```
