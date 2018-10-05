#!/usr/bin/env python

import multiprocessing
import os
import csv
import requests

########################################################################
class MultiProcDownloader(object):
    """
    Downloads urls with Python's multiprocessing module
    """

    #----------------------------------------------------------------------
    def __init__(self, urls):
        """ Initialize class with list of urls """
        self.urls = urls

    #----------------------------------------------------------------------
    def run(self):
        """
        Download the urls and waits for the processes to finish
        """
        jobs = []
        for url in self.urls:
            process = multiprocessing.Process(target=self.worker, args=(url,))
            jobs.append(process)
            process.start()
        for job in jobs:
            job.join()

    #----------------------------------------------------------------------
    def worker(self, url):
        """
        The target method that the process uses tp download the specified url
        """
        try:
            basefolder=url.split('-')[0]
            fname = url.split('-')[1].split('rasters/')[1].split('/download')[0] #Filename this is critical change for general use
            foldname=url.split('-')[1].split('scenes/')[1].split('/rasters')[0]
            msg = "Starting download of %s" % fname
            if not os.path.exists(os.path.join(basefolder,foldname)):
                os.makedirs(os.path.join(basefolder,foldname))
            os.chdir(os.path.join(basefolder,foldname))
            url=url.split('-')[1]
            if not os.path.isfile(os.path.join(basefolder,foldname,fname)):
                print msg, multiprocessing.current_process().name
                r = requests.get(url)
                with open(os.path.join(basefolder,foldname,fname), "wb") as f:
                    f.write(r.content)
            else:
                print("File already exists skipping "+str(fname))
        except Exception as e:
            print(e)
            print('Issues with file: '+str(fname))

def funct(local,final):
    if not os.path.exists(final):
        os.makedirs(final)
    os.chdir(final)
    urls=[]
    with open(local) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(str(final)+'-'+row['download_url'])
    downloader = MultiProcDownloader(urls)
    downloader.run()

#----------------------------------------------------------------------
if __name__ == "__main__":
    funct(local,final)
    # downloader = MultiProcDownloader(urls)
    # downloader.run()
