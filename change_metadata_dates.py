from datetime import datetime, timedelta
import piexif
import os
import subprocess
from PIL import Image
import shutil
import click
from tqdm import tqdm


def change_timestamp(new_timestamp, fname, new_fname):
    img = Image.open(fname)

    exif_dict = piexif.load(img.info["exif"])
    prev_ts = exif_dict["0th"][piexif.ImageIFD.DateTime]
    new_date = new_timestamp.strftime("%Y:%m:%d %H:%M:%S")
    exif_dict["0th"][piexif.ImageIFD.DateTime] = new_date
    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_date
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_date
    exif_bytes = piexif.dump(exif_dict)
    img.save(new_fname, "jpeg", exif=exif_bytes, quality="keep", optimize=True)


@click.command()
@click.option("--src-dir", required=True, help="path to directory of original pictures")
@click.option(
    "--tgt-dir",
    required=True,
    help="desired path to directory for re-timestamped pictures. Will delete specified target path and remake the directory",
)
@click.option(
    "--new-timestamp-base-str",
    default=f"{datetime.today().strftime('%Y/%m/%d')} 03:00",
    required=True,
    help="timestamp to assign first picture sorted lexicographically.  Defaults to today at 3AM.",
)
def main(src_dir, tgt_dir, new_timestamp_base_str):

    new_path = tgt_dir
    shutil.rmtree(tgt_dir, ignore_errors=True)
    os.mkdir(new_path)

    fnames = sorted(os.listdir(src_dir))
    base_ts = datetime.strptime(new_timestamp_base_str, "%Y/%m/%d %H:%M")

    for i, fname in enumerate(tqdm(fnames)):
        fpath = f"{src_dir}/{fname}"
        new_fpath = f"{new_path}/{fname}"
        new_ts = base_ts + timedelta(minutes=i)
        change_timestamp(new_ts, fpath, new_fpath)


if __name__ == "__main__":
    main()
