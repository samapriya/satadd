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
# def refresh():
#     filelist = glob.glob(os.path.join(path, "*.csv"))
#     for f in filelist:
#         os.remove(f)
#     subprocess.call('python ee_rep.py', shell=True)
#     subprocess.call('python gitcl.py', shell=True)



# def refresh_from_parser(args):
#     refresh()


# def idsearch_from_parser(args):
#     idsearch(mname=args.name)

# def intersect_from_parser(args):
#     intersect(start=args.start,
#               end=args.end,
#               geojson=args.aoi,
#               operator=args.operator,
#               output=args.report)

# def imgexp_from_parser(args):
#     imgexp(collection=args.id)


# def exp_from_parser(args):
#     exp(
#         collection=args.id,
#         folderpath=args.folder,
#         typ=args.type,
#         start=args.start,
#         end=args.end,
#         bandnames=args.bandlist,
#         geojson=args.aoi,
#         operator=args.operator,
#         )
spacing = '                               '

def main(args=None):
    parser = argparse.ArgumentParser(description='Simple CLI for piping Planet, Satellogic & GBDX Assets')

    subparsers = parser.add_subparsers()
    parser_dginit = subparsers.add_parser('dginit',help='Initialize GBDX')
    parser_dginit.set_defaults(func=dginit_from_parser)

    parser_satinit = subparsers.add_parser('satinit',help='Initialize Satellogic Tokens')
    parser_satinit.set_defaults(func=satinit_from_parser)

    parser_info = subparsers.add_parser('info',help='Prints account info for GBDX')
    parser_info.set_defaults(func=info_from_parser)

    parser_simple_search = subparsers.add_parser('simple_search',help='Simple search to look for DG assets that intersect your AOI handles KML/SHP/GEOJSON')
    parser_simple_search.add_argument('--local',help='full path for folder or file with SHP/KML/GEOJSON')
    parser_simple_search.add_argument('--start',help='start date YYYY-MM-DD')
    parser_simple_search.add_argument('--end',help='end date YYYY-MM-DD')
    parser_simple_search.add_argument('--limit',help='Limit the number of items to search')
    parser_simple_search.set_defaults(func=simple_search_from_parser)

    parser_metadata = subparsers.add_parser('metadata',help='Exports metadata for simple search into constitudent folders as JSON files')
    parser_metadata.add_argument('--local',help='full path for folder or file with SHP/KML/GEOJSON')
    parser_metadata.add_argument('--start',help='start date YYYY-MM-DD')
    parser_metadata.add_argument('--end',help='end date YYYY-MM-DD')
    parser_metadata.add_argument('--limit',help='Limit the number of items to search')
    parser_metadata.set_defaults(func=metadata_from_parser)

    parser_footprint = subparsers.add_parser('footprint',help='Exports footprint for metadata files extracted earlier and converts them to indidual geometries (GeoJSON) and combined geomtry (GeoJSON) file')
    parser_footprint.add_argument('--local',help='full path for folder with metadata JSON files')
    parser_footprint.add_argument('--dirc',help='directory to store individual geometries')
    parser_footprint.add_argument('--output',help='path to combined footprint geometry geojson')
    parser_footprint.set_defaults(func=footprint_from_parser)

    parser_satraster = subparsers.add_parser('satraster',help='Filter and download Satellogic Imagery')
    parser_satraster.add_argument('--sensor',help='Choose micro or macro depending on multispec or hyperspectal')
    parser_satraster.add_argument('--local',help='Local Path to save files')
    optional_named = parser_satraster.add_argument_group('Optional named arguments')
    optional_named.add_argument('--geometry',help='Pass GeoJSON geometry file as filter')
    parser_satraster.set_defaults(func=satraster_from_parser)
    args = parser.parse_args()

    args.func(args)


if __name__ == '__main__':
    main()
