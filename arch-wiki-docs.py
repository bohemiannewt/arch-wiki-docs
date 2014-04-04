#! /usr/bin/env python

import datetime
import argparse

from ArchWiki import ArchWiki
from ArchWikiOptimizer import ArchWikiOptimizer
from ArchWikiDownloader import ArchWikiDownloader
    
if __name__ == "__main__":
    aparser = argparse.ArgumentParser(description="Download pages from Arch Wiki and optimize them for offline browsing")
    aparser.add_argument("--output-directory", type=str, required=True, help="Path where the downloaded pages should be stored.")
    aparser.add_argument("--force", action="store_true", help="Ignore timestamp, always download the page from the wiki.")
    aparser.add_argument("--clean", action="store_true", help="Clean the output directory after downloading, useful for removing pages deleted/moved on the wiki. Warning: any unknown files found in the output directory will be deleted!")

    args = aparser.parse_args()
    if args.force:
        epoch = datetime.datetime.utcnow()
    else:
        # this should be the date of the latest incompatible change
        epoch = datetime.datetime(2014, 4, 4)

    aw = ArchWiki()
    optimizer = ArchWikiOptimizer(aw, args.output_directory)

    downloader = ArchWikiDownloader(aw, args.output_directory, epoch, cb_download=optimizer.optimize)
    aw.print_namespaces()
    for ns in ["0", "4", "12", "14"]:
        downloader.process_namespace(ns)

    downloader.download_images()
    downloader.download_css()

    if args.clean:
        downloader.clean_output_directory()
