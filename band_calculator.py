from enum import IntEnum
import os
import logging
from contextlib import contextmanager

import numpy
import numpy as np
import rasterio

from timer import Timer


logger = logging.getLogger(__name__)

class Bands(IntEnum):
    B = 2
    G = 3
    R = 4
    NIR = 8


display_min = 1000
display_max = 10000

def display(image, display_min, display_max=display_max): # copied from Bi Rico
    # Here I set copy=True in order to ensure the original image is not
    # modified. If you don't mind modifying the original image, you can
    # set copy=False or skip this step.
    image = np.array(image, copy=True)
    image.clip(display_min, display_max, out=image)
    image -= display_min
    image //= (display_max - display_min + 1) / 256.
    return image.astype(np.uint8)

def lut_display(image, display_min=display_min, display_max=display_max) :
    lut = np.arange(2**16, dtype='uint16')
    lut = display(lut, display_min, display_max)
    return np.take(lut, image)

class BandCalculator:

    def __init__(self, bands_dir='.'):
        self.bands_dir = bands_dir
        self.ndvi_filepath = os.path.join(bands_dir, 'sentinel_ndvi.tiff')
        self.rgb_filepath = os.path.join(bands_dir, 'rgb.tiff')

    @staticmethod
    def wb(channel, perc=0.05):
        mi, ma = (np.percentile(channel, perc), 2000)  # np.percentile(channel,100.0-perc))
        channel = np.uint8(np.clip((channel - mi) * 255.0 / (ma - mi), 0, 255))
        return channel

    @contextmanager
    def get_band(self, band):
        path = os.path.join(self.bands_dir, 'B0{}.jp2'.format(band))
        band = rasterio.open(path)
        logger.info('Opened Band file {}'.format(path))
        yield band
        band.close()

    def save_rgb(self, x=0, y=10000):
        with self.get_band(Bands.R) as r_band:
            with self.get_band(Bands.G) as g_band:
                with self.get_band(Bands.B) as b_band:
                    with Timer('Reading band R'):
                        r = self.wb(r_band.read(1, window=((x, y), (x, y))))
                    with Timer('Reading band G'):
                        g = self.wb(g_band.read(1, window=((x, y), (x, y))))
                    with Timer('Reading band B'):

                        b = self.wb(b_band.read(1, window=((x, y), (x, y))))
                    with Timer('Writing RGB image'):

                        with rasterio.open(self.rgb_filepath, 'w',
                                           driver='GTiff', width=y, height=y, count=3,
                                           dtype=r.dtype, crs=r_band.crs, transform=r_band.transform) as dst:
                            for k, arr in [(1, r), (2, g), (3, b)]:
                                dst.write(arr, indexes=k)
        return self.rgb_filepath

    def save_ndvi(self, x=0, y=10000):
        with self.get_band(Bands.R) as r_band:
            with self.get_band(Bands.NIR) as nir_band:
                    with Timer('Reading band R'):
                        r = r_band.read(1, window=((x, y), (x, y))).astype(numpy.float32)
                    with Timer('Opening band NIR'):
                        nir = nir_band.read(1, window=((x, y), (x, y))).astype(numpy.float32)
                    with Timer('CalculatingNDVI'):
                        ndvi = numpy.true_divide((nir-r), (nir + r))
                    output_band = numpy.rint((ndvi) * 255).astype(numpy.uint8)
                    with Timer("Writing to output file"):
                        with rasterio.open(self.ndvi_filepath, 'w',
                                           driver='GTiff', width=y, height=y, count=1,
                                           dtype=numpy.uint8, crs=r_band.crs, transform=r_band.transform, nodata=0) as dst:
                            for k, arr in [(1, output_band)]:
                                dst.write(arr, indexes=k)
        return self.ndvi_filepath
