# satadd
CLI pipeline for Planet, Satellogic, Google Earth Engine and Digital Globe Imagery

Google Earth Engine opened the door for the possibility of getting a curated list of public datasets already ingested in an analysis platform. With over 450+ raster datasets alone, they form one of the most unique collections for publicly available datasets and are still growing. While this was happening for free and open source datasets more and more data was coming in and companies were opening their doors to open data and has missions to include researchers, users, developers and everyone else who wanted to use this datasets. This included but is not limited to companies like Planet, Digital Globe and Satellogic making large chunks of their datasets open for users. Also introduction of high temporal resolution datasets like PlanetScope, high spatial resolution like Skysat and Digital Globe and high spectral resolution images like hyperspectral data from Satellogic was changing our approach to problem solving. While there has been development in building standard API and data access methods there is still room for growth and standrardization and above all easy access to these resources. Planet's [Open California Program](https://www.planet.com/products/open-california/), the [Education and Research Program](https://www.planet.com/markets/education-and-research/) , Digital Globe's [Open Data Program](https://www.digitalglobe.com/opendata) and [Education and Research program under Satellogic and their Open Data](https://github.com/satellogic/open-impact) it became obvious that questions we can ask from these sensors could get interesting.

This tool was built with a focus on the same issues and borrow parts from my other projects such as [ppipe](https://pypi.org/project/ppipe/) for handling Planet's datasets, [gee2drive](https://pypi.org/project/gee2drive/) to handle download collections already available in Google Earth Engine (GEE), [pygbdx](https://pypi.org/project/pygbdx/) which is a relatively new project to explore Digital Globe assets and I have now integrated tools to access and download Satellogic imagery. Core components from a lot of these tools have gone into building [satadd](https://pypi.org/project/satadd/) based on the idea of adding satelite data as needed. These tools include authentications setups for every account, and access to datasets, metadata among other tools. This was not build however for heavy lifting though I have tested this on hundreds and thousands of assets delivery so it behaves robustly for now. The tool is build and rebuilt as companies change their authentication protocal and delivery mechanisms and allow for improving many aspects of data delivery and preprocessing in the next iterations.

While almost all of these tools allow for local export, GEE only exports for now to Google Drive or your Google Cloud Storage Buckets, though what is lost in the delivery endpoints is gained in the fact that GEE is already a mature platform to analyze and look at open datasets but also allows you to bring private datasets into GEE for analysis. So while data download and local analysis may have been the norm, it serves us well to think about posting analysis rather in analysis engines. But that is a discussion for a different time. At this point, I am hoping that this tool alows you to do exactly what the intentions might have been from different providers and to bring them together. Since this tool downloads data it is indeed bandwidth heavy and requires a steady internet connection. This tools handles authentication, downloading, and talking to different API end points and services. In the future I am hoping to include additional preprocessing and delivery to non local endpoints like existing ftp, servers or buckets.

The assumption here is
* Every image in the give image have the same band structure, choose the bandlist that you know to common to all images
* If the geomery is too complex use the operator feature to use a bounding box instead.
* For now all it filters is geometry and date, and it is does not filter based on metadata (however in the examples folder I have shown how to import and use additional filter before exporting an image collection)

In the future I will try to integrate some other functionalities to this environment and you can indeed run the tool without the use of the autosuggest terminal as a simple CLI. Hence the terminal feature is optional.

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [satadd Satellite Data Download Addon](#satadd-satellite-data-download-addon)
    * [Initialize and Authenticate](#initialize-and-authenticate)
    * [satadd refresh](#satadd-refresh)
    * [satadd idsearch](#satadd-idsearch)
    * [satadd intersect](#satadd-intersect)
    * [satadd bandtype](#satadd-bandtype)
    * [satadd export](#satadd-export)

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

### satadd refresh
For the past couple of months I have [maintained a catalog of the most current Google Earth Engine assets](https://github.com/samapriya/Earth-Engine-Datasets-List), within their raster data catalog. I update this list every week. This tool downloads the most current version of this list, and also looks into your personal assets to generate your very own asset report which then serve as a master dataset to feed into autosuggestions.

```
satadd refresh -h
usage: satadd refresh [-h]

optional arguments:
  -h, --help  show this help message and exit
```

### satadd idsearch
There is a possibility that you don't really remember the full path to your asset or the public asset. Fortunately when I parse and collect the image list and path for you they have names that are searchable so use a keyword. for example search using "MODIS" or "sentinel". Also it is not case sensitive, so you should be able to type "SENTINEl" or "Sentinel" or "sentinel" and it should still work

```
satadd idsearch -h
usage: satadd idsearch [-h] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  --name NAME  Name or part of name to search for
```

### satadd intersect
This tool allows you to export a report of every asset present in the Earth Engine dataset list and your personal assets that intersects
with your geometry. The tool expects you to provide a start and end date and a geometry to filter. The tool uses the bounds() function to use a bounding box incase the geometry has a complex geometry or too many vertices simply use the operator ``bb``. If the geojson/json/kml keeps giving parsing error go to [geojson.io](geojson.io)

```
usage: satadd intersect [-h] [--start START] [--end END] [--aoi AOI]
                              [--report REPORT] [--operator OPERATOR]

optional arguments:
  -h, --help           show this help message and exit
  --start START        Start date to filter image
  --end END            End date to filter image
  --aoi AOI            Full path to geojson/json/kml to be used for bounds
  --report REPORT      Full path where the report will be exported including
                       type, path & number of intersects

Optional named arguments for geometry only:
  --operator OPERATOR  Use bb for Bounding box incase the geometry is complex
                       or has too many vertices
```

### satadd bandtype
Export requires all the bandtypes to be of the same kind. To do this, I simply generate the band types for you and you can select the band list you want , remember to paste it as a list.

```
usage: satadd bandtype [-h] [--id ID]

optional arguments:
  -h, --help  show this help message and exit
  --id ID     full path for collection or image
```

### satadd export
Finally the export tool, that lets you export an image or a collection clipped to your AOI. This makes use of the bandlist you exported. Incase you are exporting an image and not a collection you don't need a start and end date. The tool uses the bounds() function to use a bounding box incase the geometry has a complex geometry or too many vertices simply use the operator ```bb```. If the geojson/json/kml keeps giving parsing error go to [geojson.io](geojson.io)

```
usage: satadd export [-h] [--id ID] [--type TYPE] [--folder FOLDER]
                        [--aoi AOI] [--start START] [--end END]
                        [--bandlist BANDLIST] [--operator OPERATOR]

optional arguments:
  -h, --help           show this help message and exit
  --id ID              Full path for collection or image
  --type TYPE          Type whether image or collection
  --folder FOLDER      Drive folder path
  --aoi AOI            Full path to geojson/json/kml to be used for bounds

Optional named arguments for image collection only:
  --start START        Start date to filter image
  --end END            End date to filter image
  --bandlist BANDLIST  Bandlist we generated from bandtype export must be same
                       bandtype
  --operator OPERATOR  Use bb for Bounding box incase the geometry is complex
                       or has too many vertices
```

A typical setup would be
```satadd export --id "COPERNICUS/S2" --folder "sentinel-export" --aoi "C:\Users\sam\boulder.geojson" --start "2018-02-01" --end "2018-03-01"
--bandlist ['B2','B3','B4'] --operator "bb" --type "collection"
```

Also as promised earlier , there is a way to add additional filters and then pass it through the export function here is how and I have included this in the Examples folder. This for example uses the Landsat collection but applies the Cloud cover filter before passing it for export

```python
import ee
import os
import sys
import satadd
[head,tail]=os.path.split(satadd.__file__)
os.chdir(head)
sys.path.append(head)
from export import exp
ee.Initialize()
exp(collection=ee.ImageCollection('LANDSAT/LC08/C01/T1_SR').filterMetadata('CLOUD_COVER','less_than',20),
    folderpath="l8-out",start="2018-02-01",end="2018-06-01",
    geojson=r"C:\Users\sam\boulder.geojson",bandnames="['B1','B2']",
    operator="bb",typ="ImageCollection")
```


#### Changelog

##### v0.0.6
* Now export report of all assets intersecting with geometry & date range
* Minor fixes and general improvements

##### v0.0.4
* Can now parse gejson, json,kml
* Minor fixes and general improvements

##### v0.0.3
* Minor Fixes

