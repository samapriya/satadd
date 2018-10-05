#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import glob
import subprocess
from gbdx_validate import validate
from simplesearch import search
from gbdx_mexport import mxp
from gbdx_fpexport import fxp
from satellogic_imagery import satfile
from satellogic_metadata import satmeta
from satellogic_metalist import metalist
from satellogic_bandlist import bandlist
from multiproc_pydl import funct
from batchreproject import reproject
from cli_metadata import metadata
from async_download import ddownload
from idsearch import idsearch
from bandtypes import imgexp
from export import exp
from exp_report import intersect
from os import linesep
import textwrap as _textwrap
from argparse import RawTextHelpFormatter
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path=os.path.dirname(os.path.realpath(__file__))

def planet_key_entry(args):
    if args.type=="quiet":
        write_planet_json({'key': args.key})
    elif args.type==None and args.key==None:
        try:
            subprocess.call('planet init',shell=True)
        except Exception as e:
            print('Failed to Initialize')

def dginit():
    subprocess.call('python authenticator.py', shell=True)
def dginit_from_parser(args):
    dginit()

def satinit():
    subprocess.call('python satellogic_auth.py', shell=True)
def satinit_from_parser(args):
    satinit()

def eeinit():
    subprocess.call('earthengine authenticate', shell=True)
def eeinit_from_parser(args):
    eeinit()

def credrefresh():
    subprocess.call('python config_refresh.py', shell=True)
def credrefresh_from_parser(args):
    credrefresh()

def dasync_from_parser(args):
    ddownload(infile=args.infile,
           item=args.item,
           asset=args.asset,
           start=args.start,
           end=args.end,
           cmin=args.cmin,
           cmax=args.cmax,
           dirc=args.local)

def savedsearch_from_parser(args):
    if args.limit==None:
        subprocess.call("python saved_search_download.py "+args.name+' '+args.asset+' '+args.local,shell=True)
    else:
        subprocess.call("python saved_search_download.py "+args.name+' '+args.asset+' '+args.local+' '+args.limit,shell=True)

def metadata_from_parser(args):
    metadata(asset=args.asset,mf=args.mf,mfile=args.mfile,errorlog=args.errorlog,directory=args.dir)

def info_from_parser(args):
    validate()

def simple_search_from_parser(args):
    search(path=args.local,
              start=args.start,
              end=args.end,
              limit=int(args.limit))
def metadata_from_parser(args):
    mxp(path=args.local,
              start=args.start,
              end=args.end,
              limit=int(args.limit))

def footprint_from_parser(args):
    fxp(path=args.local,
              dir=args.dirc,
              output=args.output)

def satraster_from_parser(args):
    satfile(sensor=args.sensor,
        geometry=args.geometry,
        target=args.local)

def satlist_from_parser(args):
    bandlist(sensor=args.sensor,
        geometry=args.geometry,
        target=args.local)

def multiproc_from_parser(args):
    if __name__ == "__main__":
        funct(local=args.bandlist,
            final=args.local)

def satmeta_from_parser(args):
    satmeta(sensor=args.sensor,
        geometry=args.geometry,
        target=args.local)

def metalist_from_parser(args):
    metalist(sensor=args.sensor,
        geometry=args.geometry,
        target=args.local)

def reproject_from_parser(args):
    reproject(dest=args.input,
        output=args.output,
        epsg=args.epsg)

def eerefresh():
    filelist = glob.glob(os.path.join(path, "*.csv"))
    for f in filelist:
        os.remove(f)
    subprocess.call('python ee_rep.py', shell=True)
    subprocess.call('python gitcl.py', shell=True)


def eerefresh_from_parser(args):
    eerefresh()


def idsearch_from_parser(args):
    idsearch(mname=args.name)

def intersect_from_parser(args):
    intersect(start=args.start,
              end=args.end,
              geojson=args.aoi,
              operator=args.operator,
              output=args.report)

def imgexp_from_parser(args):
    imgexp(collection=args.id)


def exp_from_parser(args):
    exp(
        collection=args.id,
        folderpath=args.folder,
        typ=args.type,
        start=args.start,
        end=args.end,
        bandnames=args.bandlist,
        geojson=args.aoi,
        operator=args.operator,
        )

spacing = '                               '

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple CLI for piping Planet, Satellogic,GEE & GBDX Assets', formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()
    parser_planet_key = subparsers.add_parser('planetkey', help='Setting up planet API Key')
    optional_named = parser_planet_key.add_argument_group('Optional named arguments')
    optional_named.add_argument('--type', help='For direct key entry type --type quiet')
    optional_named.add_argument('--key', help='Your Planet API Key')
    parser_planet_key.set_defaults(func=planet_key_entry)

    parser_dginit = subparsers.add_parser('dginit',help='Initialize Digital Globe GBDX')
    parser_dginit.set_defaults(func=dginit_from_parser)

    parser_satinit = subparsers.add_parser('satinit',help='Initialize Satellogic Tokens')
    parser_satinit.set_defaults(func=satinit_from_parser)

    parser_eeinit = subparsers.add_parser('eeinit',help='''Initialize Google Earth Engine''')
    parser_eeinit.set_defaults(func=eeinit_from_parser)

    parser_credrefresh = subparsers.add_parser('credrefresh',help='''Refresh Satellogic & GBDX tokens

        ''')
    parser_credrefresh.set_defaults(func=credrefresh_from_parser)

    parser_dasync=subparsers.add_parser('dasync',help='''Uses the Planet Client Async Downloader to download Planet Assets: Does not require activation''')
    parser_dasync.add_argument('--infile',help='Choose a geojson from geojson.io or the aoi-json you created earlier using ppipe aoijson')
    parser_dasync.add_argument('--item',help='Choose from Planet Item types Example: PSScene4Band, PSOrthoTile, REOrthoTile etc')
    parser_dasync.add_argument('--asset',help='Choose an asset type example: anlaytic, analytic_dn,analytic_sr,analytic_xml etc')
    parser_dasync.add_argument('--local',help='Local Path where Planet Item and asset types are saved')
    optional_named = parser_dasync.add_argument_group('Optional named arguments')
    optional_named.add_argument('--start', help='Start date filter format YYYY-MM-DD',default=None)
    optional_named.add_argument('--end', help='End date filter format YYYY-MM-DD',default=None)
    optional_named.add_argument('--cmin', help='Cloud cover minimum between 0-1',default=None)
    optional_named.add_argument('--cmax', help='Cloud cover maximum between 0-1',default=None)
    parser_dasync.set_defaults(func=dasync_from_parser)

    parser_savedsearch=subparsers.add_parser('savedsearch',help='Tool to download saved searches from Planet Explorer')
    parser_savedsearch.add_argument('--name',help='Name of your saved search(It is case sensitive)')
    parser_savedsearch.add_argument('--asset',help='Choose asset type analytic, analytic_xml, analytic_sr, analytic_dn etc')
    parser_savedsearch.add_argument('--local',help='Local Path (full path address) where PlanetAssets are saved')
    optional_named = parser_savedsearch.add_argument_group('Optional named arguments')
    optional_named.add_argument('--limit', help='Choose number of assets you want to download')
    parser_savedsearch.set_defaults(func=savedsearch_from_parser)

    parser_metadata=subparsers.add_parser('metadata',help='''Tool to tabulate and convert all metadata files from Planet
Item and Asset types for Ingestion into GEE

        ''')
    parser_metadata.add_argument('--asset', help='Choose PS OrthoTile(PSO)|PS OrthoTile DN(PSO_DN)|PS OrthoTile Visual(PSO_V)|PS4Band Analytic(PS4B)|PS4Band DN(PS4B_DN)|PS4Band SR(PS4B_SR)|PS3Band Analytic(PS3B)|PS3Band DN(PS3B_DN)|PS3Band Visual(PS3B_V)|RE OrthoTile (REO)|RE OrthoTile Visual(REO_V)|DigitalGlobe MultiSpectral(DGMS)|DigitalGlobe Panchromatic(DGP)|PolarGeospatial CenterDEM Strip(PGCDEM)?')
    parser_metadata.add_argument('--mf', help='Metadata folder?')
    parser_metadata.add_argument('--mfile',help='Metadata filename to be exported along with Path.csv')
    parser_metadata.add_argument('--errorlog',default='./errorlog.csv',help='Errorlog to be exported along with Path.csv')
    optional_named = parser_metadata.add_argument_group('Optional named arguments')
    optional_named.add_argument('--dir', help='Path to Image Directory to be used to get ImageTags with metadata. use only with PS4B_SR')
    parser_metadata.set_defaults(func=metadata_from_parser)

    parser_simple_search = subparsers.add_parser('simple_search',help='Simple search to look for DG assets that intersect your AOI handles KML/SHP/GEOJSON')
    parser_simple_search.add_argument('--local',help='full path for folder or file with SHP/KML/GEOJSON')
    parser_simple_search.add_argument('--start',help='start date YYYY-MM-DD')
    parser_simple_search.add_argument('--end',help='end date YYYY-MM-DD')
    parser_simple_search.add_argument('--limit',help='Limit the number of items to search')
    parser_simple_search.set_defaults(func=simple_search_from_parser)

    parser_metadata = subparsers.add_parser('metadata',help='''Exports metadata for simple search into constitutent folders as JSON files''')
    parser_metadata.add_argument('--local',help='full path for folder or file with SHP/KML/GEOJSON')
    parser_metadata.add_argument('--start',help='start date YYYY-MM-DD')
    parser_metadata.add_argument('--end',help='end date YYYY-MM-DD')
    parser_metadata.add_argument('--limit',help='Limit the number of items to search')
    parser_metadata.set_defaults(func=metadata_from_parser)

    parser_footprint = subparsers.add_parser('footprint',help='''Exports footprint for metadata files extracted earlier'''+
    linesep+"and converts them to individual geometries (GeoJSON)and combined geometry (GeoJSON) file"+'''

    ''')
    parser_footprint.add_argument('--local',help='full path for folder with metadata JSON files')
    parser_footprint.add_argument('--dirc',help='directory to store individual geometries')
    parser_footprint.add_argument('--output',help="path to combined footprint geometry geojson")
    parser_footprint.set_defaults(func=footprint_from_parser)

    parser_satraster = subparsers.add_parser('satraster',help='''Filter and download Satellogic Imagery''')
    parser_satraster.add_argument('--sensor',help='Choose micro or macro depending on multispec or hyperspectal')
    parser_satraster.add_argument('--local',help='Local Path to save files')
    optional_named = parser_satraster.add_argument_group('Optional named arguments')
    optional_named.add_argument('--geometry',help='''Pass GeoJSON geometry file as filter''')
    parser_satraster.set_defaults(func=satraster_from_parser)

    parser_satlist = subparsers.add_parser('satlist',help='''Get url for band list based on filtered Satellogic Imagery''')
    parser_satlist.add_argument('--sensor',help='Choose micro or macro depending on multispec or hyperspectal')
    parser_satlist.add_argument('--local',help='Full path to csv file to save urls')
    optional_named = parser_satlist.add_argument_group('Optional named arguments')
    optional_named.add_argument('--geometry',help='''Pass GeoJSON geometry file as filter''',default=None)
    parser_satlist.set_defaults(func=satlist_from_parser)

    parser_multiproc = subparsers.add_parser('multiproc',help='''Multiprocess based downloader based on satlist''')
    parser_multiproc.add_argument('--bandlist',help='Choose the earlier bandlist that you created')
    parser_multiproc.add_argument('--local',help='Local Path to save files')
    parser_multiproc.set_defaults(func=multiproc_from_parser)

    parser_satmeta = subparsers.add_parser('satmeta',help='''Filter and download Satellogic Metadata''')
    parser_satmeta.add_argument('--sensor',help='Choose micro or macro depending on multispec or hyperspectal')
    parser_satmeta.add_argument('--local',help='Local Path to save files')
    optional_named = parser_satmeta.add_argument_group('Optional named arguments')
    optional_named.add_argument('--geometry',help='''Pass GeoJSON geometry file as filter''')
    parser_satmeta.set_defaults(func=satmeta_from_parser)

    parser_metalist = subparsers.add_parser('metalist',help='''Generates Basic Metadata list per scene for Satellogic Imagery''')
    parser_metalist.add_argument('--sensor',help='Choose micro or macro depending on multispec or hyperspectal')
    parser_metalist.add_argument('--local',help='Local full Path to csv files')
    optional_named = parser_metalist.add_argument_group('Optional named arguments')
    optional_named.add_argument('--geometry',help='Pass GeoJSON geometry file as filter')
    parser_metalist.set_defaults(func=metalist_from_parser)

    parser_reproject = subparsers.add_parser('reproject',help='''Batch reproject rasters using EPSG code

        ''')
    parser_reproject.add_argument('--input',help='Input folder with raster files')
    parser_reproject.add_argument('--output',help='Output folder for reprojected files to be stored')
    parser_reproject.add_argument('--epsg',help='EPSG Code for example 4326')
    parser_reproject.set_defaults(func=reproject_from_parser)

    parser_eerefresh = subparsers.add_parser('eerefresh',help='Refreshes your personal asset list and GEE Asset list')
    parser_eerefresh.set_defaults(func=eerefresh_from_parser)

    parser_idsearch = subparsers.add_parser('idsearch',help='Does possible matches using asset name to give you asseth id/full path')
    parser_idsearch.add_argument('--name',help='Name or part of name to search for')
    parser_idsearch.set_defaults(func=idsearch_from_parser)


    parser_intersect = subparsers.add_parser('intersect',help='Exports a report of all assets(Personal & GEE) intersecting with provided geometry')
    parser_intersect.add_argument('--start',help='Start date to filter image',default=None)
    parser_intersect.add_argument('--end', help='End date to filter image', default=None)
    parser_intersect.add_argument('--aoi',help='Full path to geojson/json/kml to be used for bounds')
    parser_intersect.add_argument('--report',help='Full path where the report will be exported including type, path & number of intersects', default=None)
    optional_named = parser_intersect.add_argument_group('Optional named arguments for geometry only')
    optional_named.add_argument('--operator',help='Use bb for Bounding box incase the geometry is complex or has too many vertices', default=None)
    parser_intersect.set_defaults(func=intersect_from_parser)

    parser_imgexp = subparsers.add_parser('bandtype',help='Prints GEE bandtype and generates list to be used for export')
    parser_imgexp.add_argument('--id',help='full path for collection or image')
    parser_imgexp.set_defaults(func=imgexp_from_parser)

    parser_exp = subparsers.add_parser('export',help='Export GEE Collections based on filter')
    parser_exp.add_argument('--id',help='Full path for collection or image')
    parser_exp.add_argument('--folder', help='Drive folder path')
    parser_exp.add_argument('--type',help='Type whether image or collection')
    parser_exp.add_argument('--aoi',help='Full path to geojson/json/kml to be used for bounds')
    optional_named = parser_exp.add_argument_group('Optional named arguments for image collection only')
    optional_named.add_argument('--start',help='Start date to filter image',default=None)
    optional_named.add_argument('--end', help='End date to filter image', default=None)
    optional_named.add_argument('--bandlist',help='Bandlist we generated from bandtype export must be same bandtype', default=None)
    optional_named.add_argument('--operator',help='Use bb for Bounding box incase the geometry is complex or has too many vertices', default=None)
    parser_exp.set_defaults(func=exp_from_parser)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
