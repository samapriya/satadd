# satadd
CLI pipeline for Planet, Satellogic, Google Earth Engine and Digital Globe Imagery

```
usage: satadd.py [-h]
                 {dginit,satinit,eeinit,simple_search,metadata,footprint,satraster,satmeta,metalist,reproject,refresh,idsearch,intersect,bandtype,export}
                 ...

Simple CLI for piping Planet, Satellogic,GEE & GBDX Assets

positional arguments:
  {dginit,satinit,eeinit,simple_search,metadata,footprint,satraster,satmeta,metalist,reproject,refresh,idsearch,intersect,bandtype,export}
    dginit              Initialize GBDX
    satinit             Initialize Satellogic Tokens
    eeinit              Initialize Google Earth Engine
    eeinit              Refresh Satellogic & GBDX tokens


    simple_search       Simple search to look for DG assets that intersect your AOI handles KML/SHP/GEOJSON
    metadata            Exports metadata for simple search into constitutent folders as JSON files
    footprint           Exports footprint for metadata files extracted earlier
                        and converts them to individual geometries (GeoJSON)and combined geometry (GeoJSON) file


    satraster           Filter and download Satellogic Imagery
    satmeta             Filter and download Satellogic Metadata
    metalist            Generates Basic Metadata list per scene for Satellogic Imagery
    reproject           Batch reproject rasters using EPSG code


    refresh             Refreshes your personal asset list and GEE Asset list
    idsearch            Does possible matches using asset name to give you asseth id/full path
    intersect           Exports a report of all assets(Personal & GEE) intersecting with provided geometry
    bandtype            Prints GEE bandtype and generates list to be used for export
    export              Export GEE Collections based on filter

optional arguments:
  -h, --help            show this help message and exit
  ```
