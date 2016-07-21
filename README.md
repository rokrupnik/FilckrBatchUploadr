# FlickrBatchUploadr
Simple python script that recursively iterates given folder and for every directory that contains photos creates a Flickr photoset, uploads contained photos and adds them to the created photoset.

# Requirements
* python 2.7
* [`flickrapi` library](https://stuvel.eu/flickrapi)
* [Flickr API key and secret](https://www.flickr.com/services/apps/create/apply/)

# Usage
`python upload.py root_folder_with_photos`
