"""
Fixed resolution buffer support, along with a primitive image analysis tool.

Author: Matthew Turk <matthewturk@gmail.com>
Affiliation: KIPAC/SLAC/Stanford
Homepage: http://yt.enzotools.org/
License:
  Copyright (C) 2008 Matthew Turk.  All Rights Reserved.

  This file is part of yt.

  yt is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from yt.raven import *

import _MPL

class FixedResolutionBuffer(object):
    def __init__(self, data_source, bounds, buff_size, antialias = True):
        """
        Accepts a 2D data object, such as a Projection or Slice, and implements
        a protocol for generating a pixelized, fixed-resolution buffer.
        *bounds* is (px_min,px_max,py_min,py_max), *buff_size* is 
        (width, height), and antialias is a boolean referring to whether or not
        the buffer should have pixel boundary antialiasing.
        """
        self.data_source = data_source
        self.bounds = bounds
        self.buff_size = buff_size
        self.antialias = antialias
        self.data = {}

    def __getitem__(self, item):
        if item in self.data: return self.data[item]
        buff = _MPL.Pixelize(self.data_source['px'],
                             self.data_source['py'],
                             self.data_source['pdx'],
                             self.data_source['pdy'],
                             self.data_source[item],
                             self.buff_size[0], self.buff_size[1],
                             self.bounds, int(self.antialias)).transpose()
        self[item] = buff
        return buff

    def __setitem__(self, item, val):
        self.data[item] = val

    def convert_to_pixel(self, coords):
        dpx = (self.bounds[1]-self.bounds[0])/self.buff_size[0]
        dpy = (self.bounds[3]-self.bounds[2])/self.buff_size[1]
        px = (coords[0] - self.bounds[0])/dpx
        py = (coords[1] - self.bounds[2])/dpy
        return (px, py)

    def convert_distance_x(self, distance):
        dpx = (self.bounds[1]-self.bounds[0])/self.buff_size[0]
        return distance/dpx
        
    def convert_distance_y(self, distance):
        dpy = (self.bounds[3]-self.bounds[2])/self.buff_size[1]
        return distance/dpy

class AnnuliProfiler(object):
    def __init__(self, fixed_buffer, center, num_bins, min_radius, max_radius):
        """
        This is a very simple class, principally used to sum up total values
        inside annuli in a fixed resolution buffer.  It accepts *fixed_buffer*,
        which should be a FixedResolutionBuffer, *center*, which is in pixel
        coordinates.  *num_bins*, *min_radius* and *max_radius* all refer to
        the binning properties for the annuli.  Note that these are all in
        pixel values.
        """
        self.fixed_buffer = fixed_buffer
        self.center = center
        self.num_bins = num_bins
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.bins = na.linspace(min_radius, max_radius, num_bins)
        self.data = {}
        self.radii = self._setup_bins()

    def _setup_bins(self):
        new_x = na.arange(self.fixed_buffer.buff_size[0]) - self.center[0]
        new_y = na.arange(self.fixed_buffer.buff_size[1]) - self.center[1]
        radii = na.sqrt((new_x**2.0)[None,:] + 
                        (new_y**2.0)[:,None])
        self.bin_indices = na.digitize(radii.ravel(), self.bins)

    def __getitem__(self, item):
        if item in self.data: return self.data[item]
        binned = na.zeros(self.num_bins, dtype='float64')
        for i in range(self.num_bins):
            binned[i] = na.sum(self.fixed_buffer[item].ravel()[self.bin_indices==i])
        self[item] = binned
        return binned

    def __setitem__(self, item, val):
        self.data[item] = val

    def sum(self, item):
        return self[item].sum()
