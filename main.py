from band_calculator import BandCalculator
from aws_utils import get_bands_files



band_dir = get_bands_files([2,3,4], 'tiles/34/U/DE/2016/5/23/0/', '.')
b = BandCalculator(bands_dir=band_dir)

b.save_rgb()