import geopandas as gpd
import rasterio
import requests

class DataConnector:
    def read_vector(self, path: str) -> gpd.GeoDataFrame:
        return gpd.read_file(path)

    def read_raster(self, path: str) -> rasterio.io.DatasetReader:
        return rasterio.open(path)

    def read_api_geojson(self, url: str) -> gpd.GeoDataFrame:
        resp = requests.get(url)
        return gpd.read_file(resp.text)

# Map of tool name to connector method
CONNECTORS = {
    "read_vector": DataConnector().read_vector,
    "read_raster": DataConnector().read_raster,
    "read_api_geojson": DataConnector().read_api_geojson,
}