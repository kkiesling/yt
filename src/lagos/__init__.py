"""
Lagos
=====

    Lagos defines a set of class structures for Enzo data handling.

G{packagetree}

@author: U{Matthew Turk<http://www.stanford.edu/~mturk/>}
@organization: U{KIPAC<http://www-group.slac.stanford.edu/KIPAC/>}
@contact: U{mturk@slac.stanford.edu<mailto:mturk@slac.stanford.edu>}
@license:
  Copyright (C) 2007 Matthew Turk.  All Rights Reserved.

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

from yt.logger import lagosLogger as mylog
from yt.config import ytcfg

try:
    from pyhdf_np import SD          # NumPy
    import pyhdf_np.error  # NumPy
except:
    mylog.warning("No HDF4 support")
import warnings, tables
warnings.simplefilter("ignore", tables.NaturalNameWarning)

from yt.arraytypes import *
import weakref
from new import classobj
from string import strip, rstrip
from math import ceil, floor, log10, pi
import os, os.path, types, exceptions, re
from stat import ST_CTIME

#import RavenCombine, fields, chemistry
import time

try:
    from yt.enki import EnzoInterface
except:
    pass

try:
    import EnzoFortranRoutines
except:
    pass
    #mylog.warning("EnzoFortranRoutines import failed; all fortran calls will fail!")

# Now we import all the subfiles

import PointCombine
from EnzoDefs import *
from DerivedFields import fieldInfo, log_fields, colormap_dict
from DerivedQuantities import quantityInfo
from EnzoFortranWrapper import cosmologyGetUnits
from DataReadingFuncs import *
from BaseGridType import *
from ClusterFiles import *
from BaseDataTypes import *
from EnzoRateData import *
from HierarchyType import *
from OutputTypes import *
from EnzoRunType import *
from DataCube import *
