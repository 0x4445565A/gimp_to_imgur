#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Plug-in:      Export to Imgur
# Version:      1.0
# Date:         11.1.2015
# Copyright:    Brandon Martinez <mbrandonweb@gmail.com>
# Tested with:  GIMP 2.8
#
# GNU General Public Licence (GPL)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gimpfu import *
from tempfile import gettempdir
from base64 import b64encode
from json import loads as json_load
from webbrowser import open_new as webbrowser_open_new
import urllib2, urllib

# Should my API key be revoked change this.
# See https://api.imgur.com for more information.
IMGUR_CLIENT_ID = "d0dd7b21288e5ee"

# Increase image quality for the upload.
# Try not to knock Imgur off the internet.
IMGUR_IMAGE_QUALITY = 0.7

def imgur_export(image, drawable) :
    temp_file = gettempdir() + '/gimp-imgur.jpg'
    # Save file to temp directory since we want to capture unsaved files
    pdb.file_jpeg_save(image, drawable, temp_file, temp_file, IMGUR_IMAGE_QUALITY, 0, 0, 0, "", 0, 0, 0, 0)
    values = {
      'type' : 'base64',
      'image' : b64encode(open(temp_file, 'rb').read()),
    }
    headers = {
      'Authorization': 'Client-ID ' + IMGUR_CLIENT_ID,
      'Accept': 'application/json'
    }
    data = urllib.urlencode(values)
    req = urllib2.Request('https://api.imgur.com/3/image', data, headers)
    try:
        response = urllib2.urlopen(req)
        response_data = json_load(str(response.read()))
        if (response_data['status'] == 200):
            webbrowser_open_new(response_data['data']['link'])
        else:
            pdb.gimp_message(str(response_data))
    except Exception, e: 
        pdb.gimp_message(str(e) + "\nPlease check Client-ID") 



register(
    "python_fu_imgur_export",
    "Export",
    "Export to Imgur",
    "tehbmar",
    "tehbmar",
    "2015",
    "Export to Imgur",
    "RGB*, GRAY*",
    [
      (PF_IMAGE, 'image', '', PF_IMAGE),
      (PF_DRAWABLE, 'drawable', '', PF_DRAWABLE),
    ],
    [],
    imgur_export, menu="<Image>/File/Export")

main()