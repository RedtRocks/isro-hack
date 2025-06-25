import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import shapes
from shapely.geometry import shape


def compute_slope(src: rasterio.io.DatasetReader) -> rasterio.io.MemoryFile:
    """Compute slope from a DEM using numpy gradient."""
    arr = src.read(1).astype(float)
    x, y = np.gradient(arr, src.res[0], src.res[1])
    slope = np.sqrt(x*x + y*y)

    meta = src.meta.copy()
    meta.update(dtype=rasterio.float32)
    mem = rasterio.io.MemoryFile()
    with mem.open(**meta) as dst:
        dst.write(slope.astype(rasterio.float32), 1)
    return mem


def threshold_raster(src, threshold: float) -> rasterio.io.MemoryFile:
    data = src.read(1)
    mask = (data <= threshold).astype(src.meta['dtype'])
    meta = src.meta.copy()

    mem = rasterio.io.MemoryFile()
    with mem.open(**meta) as dst:
        dst.write(mask, 1)
    return mem


def raster_to_vector(mem: rasterio.io.MemoryFile) -> gpd.GeoDataFrame:
    with mem.open() as src:
        img = src.read(1)
        result = []
        for geom, val in shapes(img, transform=src.transform):
            if val:
                result.append(shape(geom))
        return gpd.GeoDataFrame(geometry=result, crs=src.crs)


def spatial_join(gdf1: gpd.GeoDataFrame, gdf2: gpd.GeoDataFrame, how: str = 'inner') -> gpd.GeoDataFrame:
    return gpd.sjoin(gdf1, gdf2, how=how, predicate='intersects')

