#!/usr/bin/env python

import multiprocessing
import os
import sys
import time
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
            basefolder=url.split('=')[0]
            foldname=url.split('=')[1]
            filename=url.split('=')[2].split('[')[0]
            msg = "Starting download of %s" % os.path.join(foldname,filename)
            if not os.path.exists(os.path.join(basefolder,foldname)):
                os.makedirs(os.path.join(basefolder,foldname))
            os.chdir(os.path.join(basefolder,foldname))
            url=url.split('[')[1]
            #print(os.path.join(basefolder,foldname,filename))
            if not os.path.isfile(os.path.join(basefolder,foldname,filename)):
                r = requests.get(url, stream=True)
                time.sleep(1)
                if r.status_code==200:
                    print msg, multiprocessing.current_process().name
                    with open(os.path.join(basefolder,foldname,filename), 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024 * 1024):
                            if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
            else:
                print("File already exists skipping "+str(filename))
        except Exception as e:
            print(e)
            # print('Issues with file: '+str(filename))

def funct(local,final):
    if not os.path.exists(final):
        os.makedirs(final)
    os.chdir(final)
    urls=[]
    with open(local) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            urls.append(str(final)+'='+str(row['scene_id'])+'='+str(row['filename'])+'['+row['download_url'])
    downloader = MultiProcDownloader(urls)
    downloader.run()

#----------------------------------------------------------------------
if __name__ == "__main__":
    funct(local=os.path.normpath(sys.argv[1]),final=os.path.normpath(sys.argv[2]))
    # downloader = MultiProcDownloader(urls)
    # downloader.run()
