import rasterio
import numpy as np
path = "tiles34UDE20165230/"
r_path = path + "B04.jp2"
g_path = path + "B03.jp2"
b_path = path + "B02.jp2"



def process(r, g, b, crs, transform):
    with rasterio.open('rgb.tiff', 'w', driver='GTiff', width=10000, height=10000, count=3, dtype=r.dtype, crs=crs, transform=transform) as dst:
        for k, arr in [(1, r), (2, g), (3, b)]:
            dst.write(arr, indexes=k)

def wb(channel, perc=0.05):
    mi, ma = (np.percentile(channel, perc), 2000)  # np.percentile(channel,100.0-perc))
    channel = np.uint8(np.clip((channel - mi) * 255.0 / (ma - mi), 0, 255))
    return channel

with rasterio.open(r_path) as r_band:
    with rasterio.open(g_path) as g_band:
        with rasterio.open(b_path) as b_band:
            with rasterio.open(
                    'rgb.tiff', 'w',
                    driver='GTiff', width=r_band.width, height=r_band.height, count=3,
                    dtype=np.uint8, crs=r_band.crs, transform=r_band.transform) as dst:
                    for ji, window in r_band.block_windows(1):
                        print("Reading {}".format(window))
                        r = wb(r_band.read(1, window=window))
                        g = wb(g_band.read(1, window=window))
                        b = wb(b_band.read(1, window=window))
                        for k, arr in [(1, r), (2, g), (3, b)]:
                            dst.write(arr, indexes=k)


                #result_block = process(r, g, b, r_band.crs, r_band.transform)
