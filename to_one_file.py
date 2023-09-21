import warnings
warnings.filterwarnings('ignore')
import os
import re
import numpy as np
from glob import glob

from tifffile import imread, imwrite, TiffSequence
import argparse
from tqdm import tqdm
import logging
logging.basicConfig(encoding='utf-8', level=logging.CRITICAL)

parser = argparse.ArgumentParser(
                    prog='TIFF per Channel to Multi Channel TIFF converter',
                    description='This program converts single channel TIFF files to multi channel TIFF files',
                    epilog='NutriBee Modul 2')
parser.add_argument('inputpath', default="8bit", help="inputpath to TIFF files")           # positional argument

parser.add_argument('-o', '--outputpath', default = None, help = "outputpath, if not set output will be generated in the current directory")      # option that takes a value
parser.add_argument('-v', '--verbose', action='store_true', help = "more output messages")
parser.add_argument('-r', '--recursive', action='store_true', help = "epen directories inside --inputpath recusively")
args = parser.parse_args()
if args.outputpath == None:
    args.outputpath = os.path.join("./out")
    
tifffiles = [f for f in glob(os.path.join(args.inputpath,'**'), recursive=args.recursive) if re.match(r".*Ch.*(tif$)|(tiff$)|(TIF$)|(TIFF$)", f)]
filepaths, channels, suffixes = list((t for t in zip(*[(*f[:f.find('.')].split('_'),f[f.find('.'):]) for f in tifffiles])))
int_channels = sorted([int(c[2:]) for c in set(channels)])
n_channels = len(int_channels)
relevant_suffixes = [suffix for suffix in suffixes[::n_channels]]
assert len(filepaths) % len(relevant_suffixes) == 0


minimum, maximum = 65536, 0
with tqdm(total=len(relevant_suffixes)) as pbar:
    for filepath, suffix in zip(filepaths, relevant_suffixes):
        im = imread([os.path.abspath(f"{filepath}_Ch{channel}{suffix}") for channel in int_channels])
        minimum = min(im.min(), minimum)
        maximum = max(im.max(), maximum)
        tiffilepath = os.path.join(args.outputpath, f"{filepath}{suffix}")
        os.makedirs(os.path.dirname(tiffilepath), exist_ok=1)
        imwrite(tiffilepath, data=np.stack(im), dtype = np.stack(im).dtype )
        pbar.set_postfix(min=minimum, max=maximum, file=os.path.basename(tiffilepath))
        pbar.update()
