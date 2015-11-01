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

def imgur_export(image, drawable):
    # Temp file name.
    temp_file = gettempdir() + '/gimp-imgur.png'
    # Creating duplicate image to prevent screwing up.
    duplicate_image = image.duplicate()
    # Compressing all of the layers.
    compressed_layer = pdb.gimp_image_merge_visible_layers(duplicate_image, CLIP_TO_IMAGE)
    # Saving the file to temp directory to be processed.
    pdb.gimp_file_save(duplicate_image, compressed_layer, temp_file, '?')
    # Clearing up memory.
    pdb.gimp_image_delete(duplicate_image)
    # Post values for the API.
    values = {
      'type' : 'base64',
      'image' : b64encode(open(temp_file, 'rb').read()),
    }
    # Authentication headers.
    headers = {
      'Authorization': 'Client-ID ' + IMGUR_CLIENT_ID,
      'Accept': 'application/json'
    }
    # Send it out
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
    "Export to Imgur.com",
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