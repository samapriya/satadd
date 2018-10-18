# satadd: CLI pipeline for Planet, Satellogic, Google Earth Engine and Digital Globe Imagery
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1450622.svg)](https://doi.org/10.5281/zenodo.1450622)
[![PyPI version](https://badge.fury.io/py/satadd.svg)](https://badge.fury.io/py/satadd)

Cite as

```
Samapriya Roy. (2018, October 6). samapriya/satadd: satadd: CLI pipeline for Planet, Satellogic,
Google Earth Engine and Digital Globe Imagery (Version 0.0.3). Zenodo. http://doi.org/10.5281/zenodo.1450622
```

Google Earth Engine opened the door for the possibility of getting a curated list of public datasets already ingested in an analysis platform. With over 450+ raster datasets alone, they form one of the most unique collections for publicly available datasets and are still growing. While this was happening for free and open source datasets more and more data was coming in and companies were opening their doors to open data and has missions to include researchers, users, developers and everyone else who wanted to use this datasets. This included but is not limited to companies like Planet, Digital Globe and Satellogic making large chunks of their datasets open for users. Also introduction of high temporal resolution datasets like PlanetScope, high spatial resolution like Skysat and Digital Globe and high spectral resolution images like hyperspectral data from Satellogic was changing our approach to problem solving. While there has been development in building standard API and data access methods there is still room for growth and standrardization and above all easy access to these resources. Planet's [Open California Program](https://www.planet.com/products/open-california/), the [Education and Research Program](https://www.planet.com/markets/education-and-research/) , Digital Globe's [Open Data Program](https://www.digitalglobe.com/opendata) and [Education and Research program under Satellogic and their Open Data](https://github.com/satellogic/open-impact) it became obvious that questions we can ask from these sensors could get interesting.

This tool was built with a focus on the same issues and borrow parts from my other projects such as [ppipe](https://pypi.org/project/ppipe/) for handling Planet's datasets, [gee2drive](https://pypi.org/project/gee2drive/) to handle download collections already available in Google Earth Engine (GEE), [pygbdx](https://pypi.org/project/pygbdx/) which is a relatively new project to explore Digital Globe assets and I have now integrated tools to access and download Satellogic imagery. Core components from a lot of these tools have gone into building [satadd](https://pypi.org/project/satadd/) based on the idea of adding satelite data as needed. These tools include authentications setups for every account, and access to datasets, metadata among other tools. This was not build however for heavy lifting though I have tested this on hundreds and thousands of assets delivery so it behaves robustly for now. The tool is build and rebuilt as companies change their authentication protocal and delivery mechanisms and allow for improving many aspects of data delivery and preprocessing in the next iterations.

While almost all of these tools allow for local export, GEE only exports for now to Google Drive or your Google Cloud Storage Buckets, though what is lost in the delivery endpoints is gained in the fact that GEE is already a mature platform to analyze and look at open datasets but also allows you to bring private datasets into GEE for analysis. So while data download and local analysis may have been the norm, it serves us well to think about posting analysis rather in analysis engines. But that is a discussion for a different time. At this point, I am hoping that this tool alows you to do exactly what the intentions might have been from different providers and to bring them together. Since this tool downloads data it is indeed bandwidth heavy and requires a steady internet connection. This tools handles authentication, downloading, and talking to different API end points and services. In the future I am hoping to include additional preprocessing and delivery to non local endpoints like existing ftp, servers or buckets.

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [satadd Satellite Data Download Addon](#satadd-satellite-data-download-addon)
    * [Initialize and Authenticate](#initialize-and-authenticate)
    * [Planet Tools](#satadd-refresh)
    * [GBDX Tools](#satadd-idsearch)
    * [Satellogic Tools](#satadd-intersect)
    * [GEE Tools](#satadd-bandtype)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

If you get no errors and you have python 2.7.14 or higher you should be good to go. Please note that I have released this as a python 2.7 but can be easily modified for python 3.

**This toolbox also uses some functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install python-gdal
```
For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA

It has been brought to my attention that installing shapely on windows is not simply ```pip install shapely``` so install Shapely separately and [use instructions from their pypi project page](https://pypi.org/project/Shapely/) for Windows installation **Shapely is important requirement for the tool but since the installation varies based on the operating system install it using the earlier instructions anyways before the next steps**. On other operating systems ```pip install shapely``` should work just fine.


To install **satadd**
You can install using two methods

```pip install satadd```

or you can also try

```
git clone https://github.com/samapriya/satadd.git
cd satadd
python setup.py install
```
For linux use sudo. This release also contains a windows installer which bypasses the need for you to have admin permission, it does however require you to have python in the system path meaning when you open up command prompt you should be able to type python and start it within the command prompt window. Post installation using the installer you can just call satadd using the command prompt similar to calling python. Give it a go post installation type

```
satadd -h
```

Installation is an optional step; the application can be also run directly by executing satadd.py script. The advantage of having it installed is being able to execute satadd as any command line tool. I recommend installation within virtual environment. If you don't want to install, browse into the satadd folder and try ```python satadd.py``` to get to the same result.

## Getting started

As usual, to print help:

```
usage: satadd.py [-h]
                 {planetkey,dginit,satinit,eeinit,dasync,savedsearch,metadata,simple_search,footprint,satraster,satmeta,metalist,reproject,refresh,idsearch,intersect,band
type,export}
                 ...

Simple CLI for piping Planet, Satellogic,GEE & GBDX Assets

positional arguments:
  {planetkey,dginit,satinit,eeinit,dasync,savedsearch,metadata,simple_search,footprint,satraster,satmeta,metalist,reproject,refresh,idsearch,intersect,bandtype,export}
    planetkey           Setting up planet API Key
    dginit              Initialize Digital Globe GBDX
    satinit             Initialize Satellogic Tokens
    eeinit              Initialize Google Earth Engine
    credrefresh         Refresh Satellogic & GBDX tokens


    dasync              Uses the Planet Client Async Downloader to download Planet Assets: Does not require activation
    savedsearch         Tool to download saved searches from Planet Explorer
    metadata            Tool to tabulate and convert all metadata files from Planet
                        Item and Asset types for Ingestion into GEE


    simple_search       Simple search to look for DG assets that intersect your AOI handles KML/SHP/GEOJSON
    metadata            Exports metadata for simple search into constitutent folders as JSON files
    footprint           Exports footprint for metadata files extracted earlier
                        and converts them to individual geometries (GeoJSON)and combined geometry (GeoJSON) file


    satraster           Filter and download Satellogic Imagery
    satlist             Get url for band list based on filtered Satellogic Imagery
    multiproc           Multiprocess based downloader based on satlist
    satmeta             Filter and download Satellogic Metadata
    metalist            Generates Basic Metadata list per scene for Satellogic Imagery
    reproject           Batch reproject rasters using EPSG code


    eerefresh           Refreshes your personal asset list and GEE Asset list
    idsearch            Does possible matches using asset name to give you asseth id/full path
    intersect           Exports a report of all assets(Personal & GEE) intersecting with provided geometry
    bandtype            Prints GEE bandtype and generates list to be used for export
    export              Export GEE Collections based on filter

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `satadd idsearch -h`. If you didn't install satadd, then you can run it just by going to *satadd* directory and running `python satadd.py [arguments go here]`

### satadd Satellite Data Download Addon
This tool is designed to augment to the existing facilty of image export using a CLI, whereby you can pass it arguments to filter based on an area of interest geojson file, a start and end date for collection

![cli](/images/satadd.jpg)

### Initialize and Authenticate
This is an autosuggestive terminal which uses the gee2add package to perform all of the functions but has autosuggest for Earth Engine catalog and your own personal catalog. This way you can get access to image id without needing the catalog id in the javascript codeeditor.

```
planetkey           Setting up planet API Key
dginit              Initialize Digital Globe GBDX
satinit             Initialize Satellogic Tokens
eeinit              Initialize Google Earth Engine
credrefresh         Refresh Satellogic & GBDX tokens
```

Each of these authentication tools allow you to link and save credentials for each of these services you can check them by typing something like ```satadd planetkey```. Certain services require the authentication tokens to be refreshed you can simply access it using ```satadd credrefresh```.

### Planet Tools
The Planet Toolsets consists of tools required to access control and download planet labs assets (PlanetScope and RapidEye OrthoTiles) as well as parse metadata in a tabular form which maybe required by other applications. These tools are designed to interact with [Planet's Python Client](https://pypi.org/project/planet/) and the saved search featured embedded in [Planet Explorer](https://www.planet.com/explorer/) and will allow you to access and download planet imagery and metadata as needed. This also allows you to process the metadata incase you are ingesting this to GEE.

```
dasync              Uses the Planet Client Async Downloader to download Planet Assets: Does not require activation
savedsearch         Tool to download saved searches from Planet Explorer
metadata            Tool to tabulate and convert all metadata files from Planet
                    Item and Asset types for Ingestion into GEE
```

### GBDX Tools
This is a simple cli to Digital Globe's GBDX platform, this was designed from the perspective of community user (the freely available tier). This platform allows you to access all of DG's Open data and also open Ikonos data along with Landsat and Sentinel datasets. You can create a [notebook acccount here](https://notebooks.geobigdata.io). The notebook setup offers additional tools, a GUI and interactive framework while CLI simplifies some of the operational needs of batch processing and performing calls using your own local machine. This tool will allow you to perform a simple seach using a geometry to get asset summary, export the metadata as json file and also image footprint as a combined and individual geojson files.

```
simple_search       Simple search to look for DG assets that intersect your AOI handles KML/SHP/GEOJSON
metadata            Exports metadata for simple search into constitutent folders as JSON files
footprint           Exports footprint for metadata files extracted earlier
                    and converts them to individual geometries (GeoJSON)and combined geometry (GeoJSON) file
```

### Satellogic Tools
This tool allows you to access the [open data shared by Satellogic](https://github.com/satellogic/open-impact) and filter and pass a geometry object to get both micro(multiband) and macro (hyperspectral) rasters, metadata and basic metadalist. The download tool is a multipart downloader to handle quick downloads. The metalist tool can be used to create a simple metadata list for you to batch upload imagery into GEE for analysis. The reproject tool is included to handle batch reprojections as needed. The tool uses geometry passed as a geojson object go to [geojson.io](http://geojson.io). Satlist produces the band list urls and you can then use the multiproc tool to use multiprocessing to download the links.

```
satraster           Filter and download Satellogic Imagery
satlist             Get url for band list based on filtered Satellogic Imagery
multiproc           Multiprocess based downloader based on satlist
satmeta             Filter and download Satellogic Metadata
metalist            Generates Basic Metadata list per scene for Satellogic Imagery
reproject           Batch reproject rasters using EPSG code
```

### GEE Tools
This tool allows you to use the gee2drive tool functionalities to explore, match and export existing collections in GEE. Export requires all the bandtypes to be of the same kind. For the past couple of months I have [maintained a catalog of the most current Google Earth Engine assets](https://github.com/samapriya/Earth-Engine-Datasets-List), within their raster data catalog. I update this list every week. This tool downloads the most current version of this list, and allows the user to explore band types and export a collection as needed.

```
eerefresh           Refreshes your personal asset list and GEE Asset list
idsearch            Does possible matches using asset name to give you asseth id/full path
intersect           Exports a report of all assets(Personal & GEE) intersecting with provided geometry
bandtype            Prints GEE bandtype and generates list to be used for export
export              Export GEE Collections based on filter
```

## Changelog

### v0.0.4

- Fixed issue with Shapely install on windows
- Updated credrefresh to better refresh gbdx tokens

### v0.0.3

- Added better filename parsing for Satellogic images
- Added error handling for multiprocessing download of Satellogic images

### v0.0.2

- Now searches for all DG and non DG assets available within GBDX
- Added capability to create url list for rasters and download support using multiprocessing
