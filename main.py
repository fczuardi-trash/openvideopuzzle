#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from django.utils import simplejson



class MainHandler(webapp.RequestHandler):

  def get(self):
    # *  {u'id': 1, u'width': 480, u'job_slug': u'mts-ogv30-272', u'description': u'Generates 30fps deinterlaced Theora OGV 480x272 files from 60fps mpegts files.', u'height': 272}
    # * {u'id': 2, u'width': 640, u'job_slug': u'mts-ogv30-360', u'description': u'Generates 30fps deinterlaced Theora OGV 640x360 files from 60fps mpegts files.', u'height': 360}
    # * {u'id': 3, u'width': 480, u'job_slug': u'mts-mp430-272', u'description': u'Generates 30fps deinterlaced MP4 480x272 files from 60fps mpegts files.', u'height': 272}
    # * {u'id': 4, u'width': 640, u'job_slug': u'mts-mp430-360', u'description': u'Generates 30fps deinterlaced MP4 640x360 files from 60fps mpegts files.', u'height': 360}
    # * {u'id': 5, u'width': 480, u'job_slug': u'mts-jpgbw-272', u'description': u'Generates a black and white 480x272 jpeg file from mpegts files.', u'height': 272}
    # * {u'id': 6, u'width': 640, u'job_slug': u'mts-jpgbw-360', u'description': u'Generates a black and white 640x360 jpeg file from mpegts files.', u'height': 360}
    # * {u'id': 7, u'width': 480, u'job_slug': u'mts-jpg-272', u'description': u'Generates a 480x272 jpeg file from mpegts files.', u'height': 272}
    # * {u'id': 8, u'width': 640, u'job_slug': u'mts-jpg-360', u'description': u'Generates a 640x360 jpeg file from mpegts files.', u'height': 360}
    # * {u'id': 9, u'width': 192, u'job_slug': u'mts-jpg-108', u'description': u'Generates a 192x108 jpeg file from mpegts files.', u'height': 108}
    # * {u'id': 10, u'width': 192, u'job_slug': u'mts-jpgbw-108', u'description': u'Generates a black and white 192x108 jpeg file from mpegts files.', u'height': 108}
    # * {u'id': 11, u'width': 640, u'job_slug': u'mts-dirac30-360', u'description': u'Generates 30fps deinterlaced Dirac OGV 640x360 files from 60fps mpegts files.', u'height': 360}
    # * {u'id': 12, u'width': 480, u'job_slug': u'mts-dirac30-272', u'description': u'Generates 30fps deinterlaced Dirac OGV 480x272 files from 60fps mpegts files.', u'height': 272}
    # * {u'id': 13, u'width': 480, u'job_slug': u'mts-ogv24-272', u'description': u'Generates 24fps deinterlaced Theora OGV 480x272 files from 60fps mpegts files.', u'height': 272}
    # * {u'id': 14, u'width': 640, u'job_slug': u'mts-ogv24-360', u'description': u'Generates 24fps deinterlaced Theora OGV 640x360 files from 60fps mpegts files.', u'height': 360}
    # * {u'id': 15, u'width': 480, u'job_slug': u'mts-mp424-272', u'description': u'Generates 24fps deinterlaced MP4 480x272 files from 60fps mpegts files.', u'height': 272}
    # * {u'id': 16, u'width': 640, u'job_slug': u'mts-mp424-360', u'description': u'Generates 24fps deinterlaced MP4 640x360 files from 60fps mpegts files.', u'height': 360}
    # * {u'id': 17, u'width': 640, u'job_slug': u'mts-dirac24-360', u'description': u'Generates 24fps deinterlaced Dirac OGV 640x360 files from 60fps mpegts files.', u'height': 360}
    # * {u'id': 18, u'width': 480, u'job_slug': u'mts-dirac24-272', u'description': u'Generates 24fps deinterlaced Dirac OGV 480x272 files from 60fps mpegts files.', u'height': 272}
    url = 'http://api.publicvideos.org/versions/transcoder/2/'
    result = urlfetch.fetch(url)

    if result.status_code == 200:
      # success, load the json content into a python object
      # self.response.out.write(result.content)
      # return False
      videos = []
      results = simplejson.loads(result.content)
      for result in results:
        videos.append(simplejson.loads(result))
      template_values = {
        'videos'  : videos
      }
      path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
      # self.response.headers["Content-Type"] = "text/xml"
      self.response.out.write(template.render(path, template_values))
    else:
      self.response.out.write('something went wrong:%s' % result.status_code)


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
