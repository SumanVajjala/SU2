#!/usr/bin/env python 

## \file mesh_deformation.py
#  \brief Python script for doing the parallel deformation using SU2_DEF.
#  \author F. Palacios
#  \version 3.2.5 "eagle"
#
# Copyright (C) 2012-2014 SU2 <https://github.com/su2code>.
#
# SU2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# SU2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with SU2. If not, see <http://www.gnu.org/licenses/>.

import os, sys, shutil, copy
from optparse import OptionParser
sys.path.append(os.environ['SU2_RUN'])
import SU2

# -------------------------------------------------------------------
#  Main 
# -------------------------------------------------------------------

def main():
    
    # Command Line Options
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="read config from FILE", metavar="FILE")
    parser.add_option("-n", "--partitions", dest="partitions", default=2,
                      help="number of PARTITIONS", metavar="PARTITIONS")
    parser.add_option("-p", "--oldpartitions", dest="oldpartitions", default="oldpartitions",
                      help="old number of PARTITIONS (use -n instead)", metavar="OLDPARTITIONS")
    parser.add_option("-d", "--divide_grid", dest="divide_grid", default="True",
                      help="DIVIDE_GRID the numerical grid", metavar="DIVIDE_GRID")

    (options, args)=parser.parse_args()
    options.partitions = int( options.partitions )
    options.divide_grid = options.divide_grid.upper() == 'TRUE'
    
    if options.oldpartitions != "oldpartitions":
        print ("\n IMPORTANT: -p is no longer available in SU2 v3.2.4, use -n flag instead \n")
        sys.exit()
    
    # Run Parallel Comutation
    mesh_deformation ( options.filename    ,
                       options.partitions  , 
                       options.divide_grid  )
#: def main()

  
# -------------------------------------------------------------------
#  Parallel Computation Function
# -------------------------------------------------------------------

def mesh_deformation( filename           ,
                      partitions  = 2    , 
                      divide_grid = True  ):
    
    # Config
    config = SU2.io.Config(filename)
    config.NUMBER_PART = partitions
    config.DECOMPOSED  = not divide_grid
    config.DV_VALUE_NEW = config.DV_VALUE
    
    # State
    state = SU2.io.State()
    
    # Decomposition
    info = SU2.run.decompose(config)

    state.FILES.MESH = config.MESH_FILENAME

    # Deformation
    info = SU2.run.DEF(config)
    state.update(info)
    
    return state

#: mesh_deformation()


# -------------------------------------------------------------------
#  Run Main Program
# -------------------------------------------------------------------

# this is only accessed if running from command prompt
if __name__ == '__main__':
    main()
    
    
