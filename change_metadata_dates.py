from datetime import datetime, timedelta
import piexif
import os
import multiprocessing as mp


from tqdm import tqdm
import subprocess
from PIL import Image
import shutil
import click
from functools import partial


def change_timestamp_star(args):
    return change_timestamp(*args)


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

    shutil.rmtree(tgt_dir, ignore_errors=True)
    os.mkdir(tgt_dir)

    sorted_fnames = sorted(os.listdir(src_dir))
    src_fnames = [f"{src_dir}/{x}" for x in sorted_fnames]
    tgt_fnames = [f"{tgt_dir}/{x}" for x in sorted_fnames]
    new_timestamps = [
        datetime.strptime(new_timestamp_base_str, "%Y/%m/%d %H:%M")
        + timedelta(microseconds=i)
        for i in range(len(sorted_fnames))
    ]
    args = list(zip(new_timestamps, src_fnames, tgt_fnames))

    num_processes = mp.cpu_count()
    print(f"num_processes: {num_processes}")
    with mp.Pool(num_processes) as pool:
        for _ in tqdm(
            pool.imap_unordered(change_timestamp_star, args), total=len(args)
        ):
            pass


if __name__ == "__main__":
    main()
