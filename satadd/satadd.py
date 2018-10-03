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
from batchreproject import reproject
from idsearch import idsearch
from bandtypes import imgexp
from export import exp
from exp_report import intersect
from os import linesep
import textwrap as _textwrap
from argparse import RawTextHelpFormatter
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path=os.path.dirname(os.path.realpath(__file__))

def dginit():
    subprocess.call('python autenticator.py', shell=True)
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

def refresh():
    filelist = glob.glob(os.path.join(path, "*.csv"))
    for f in filelist:
        os.remove(f)
    subprocess.call('python ee_rep.py', shell=True)
    subprocess.call('python gitcl.py', shell=True)


def refresh_from_parser(args):
    refresh()


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
    parser_dginit = subparsers.add_parser('dginit',help='Initialize GBDX')
    parser_dginit.set_defaults(func=dginit_from_parser)

    parser_satinit = subparsers.add_parser('satinit',help='Initialize Satellogic Tokens')
    parser_satinit.set_defaults(func=satinit_from_parser)

    parser_eeinit = subparsers.add_parser('eeinit',help='''Initialize Google Earth Engine''')
    parser_eeinit.set_defaults(func=eeinit_from_parser)

    parser_credrefresh = subparsers.add_parser('eeinit',help='''Refresh Satellogic & GBDX tokens

        ''')
    parser_credrefresh.set_defaults(func=credrefresh_from_parser)

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

    parser_refresh = subparsers.add_parser('refresh',help='Refreshes your personal asset list and GEE Asset list')
    parser_refresh.set_defaults(func=refresh_from_parser)
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
