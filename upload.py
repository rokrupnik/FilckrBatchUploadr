import requests
from requests.packages.urllib3.exceptions import InsecurePlatformWarning, SNIMissingWarning
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

import time

import os
import sys

import flickrapi

class FileWithCallback(object):
    def __init__(self, filename, callback):
        self.file = open(filename, 'rb')
        self.callback = callback
        # the following attributes and methods are required
        self.len = os.path.getsize(filename)
        self.fileno = self.file.fileno
        self.tell = self.file.tell

    def read(self, size):
        if self.callback:
            self.callback(self.tell() * 100 // self.len)
        return self.file.read(size)


def callback(progress):
    print str(progress) + '%\r\t',

start = time.time()
checkpoint = time.time()

def print_time(checkpoint):
    end = time.time()
    s = end - start

    h = int(s / 3600)
    s = s - (h * 3600)

    m = int(s / 60)
    s = s - (m * 60)

    print 'time elapsed: %d hours, %d minutes and %d seconds' % (h, m, s), 

    s = end - checkpoint
    h = int(s / 3600)
    s = s - (h * 3600)

    m = int(s / 60)
    s = s - (m * 60)

    print ' || time for last set: %d hours, %d minutes and %d seconds' % (h, m, s), 

api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
api_secret = u'xxxxxxxxxxxxxxxx'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
flickr.authenticate_via_browser(perms='write')

walk_dir = sys.argv[1]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    # sort files by filename
    files = sorted(files)

    print('--\nroot = ' + root)

    # If at least one picture, create photoset
    if len(files) > 0:
        # TODO: check if photoset exist and then update it ALSO check if photo with same title exists
        # upload primary photo and create photoset
        filename = files[0]
        file_path = os.path.join(root, filename)

        print '\tuploading primary photo: %s (full path: %s)\n\t' % (filename, file_path),

        try:
            fileobj = FileWithCallback(file_path, callback)
            rsp = flickr.upload(title=filename, filename=filename, fileobj=fileobj, is_public=0, format='xmlnode')
            primary_photo_id = rsp.photoid[0].text
            print('\n\tuploaded primary photo with id: ' + primary_photo_id)

            print('\tcreating photoset with title ' + os.path.split(root)[1])
            rsp = flickr.photosets.create(title=os.path.split(root)[1], primary_photo_id=primary_photo_id)
            photoset_id = rsp['photoset']['id']
            print('\tcreated photoset with id ' + photoset_id)

        except Exception, e:
            print '\n\t',
            print(e)

        # upload other images
        for filename in files[1:]:
            try:
                # upload only photos and video
                if not(filename.lower().endswith(('png', 'jpg', 'gif', 'bmp', 'tiff', 'raw', 'mp4', 'mov', 'avi'))):
                    print '\twrong file type in file %s (full path: %s)\n\t' % (filename, file_path),
                    break

                file_path = os.path.join(root, filename)

                print '\tuploading file %s (full path: %s)\n\t' % (filename, file_path),

                # upload photos and add them to the photoset
                fileobj = FileWithCallback(file_path, callback)
                rsp = flickr.upload(title=filename, filename=filename, fileobj=fileobj, is_public=0, format='xmlnode')
                photo_id = rsp.photoid[0].text
                print '\n\tphoto_id: ' + photo_id,
                rsp = flickr.photosets.addPhoto(photoset_id=photoset_id, photo_id=photo_id)
                print 'status: ', rsp['stat']

            except Exception, e:
                print '\n\t',
                print(e)

    for subdir in subdirs:
        print('\t- subdirectory ' + subdir)

    print_time(checkpoint)
    checkpoint = time.time()

print('Upload completed.')