# FlickrBatchUploadr
Simple python script that recursively iterates given folder and for every directory that contains photos creates a Flickr photoset, uploads contained photos and adds them to the created photoset.

# Requirements
* python 2.7
* [`flickrapi` library](https://stuvel.eu/flickrapi)
* [Flickr API key and secret](https://www.flickr.com/services/apps/create/apply/)

# Usage
1. Insert your API key and secret to the appropriate place in the script  
2. In terminal, run: `python upload.py root_folder_with_photos`
    * For logging redirect standard output to a file e.g.: `python upload.py root_folder_with_photos > log.txt`