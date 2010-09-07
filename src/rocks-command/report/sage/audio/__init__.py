# $Id: __init__.py,v 1.5 2010/09/07 23:53:29 bruno Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.5  2010/09/07 23:53:29  bruno
# star power for gb
#
# Revision 1.4  2009/06/03 01:23:23  mjk
# - Now using the idea of modes for the wall (e.g. simple, sage, cglx)
# - Simple (chromium) and Sage modes work
# - Requires root to do a "rocks sync viz mode=??" to switch
# - "rocks enable/disable hidebezels" is chromium specific
#   The command line needs to change to reflect this fact
# - Tile-banner tell you the resolution and mode node
# - Sage works (surprised)
# - Removed autoselect of video mode on first boot, started to crash nodes
#
# Revision 1.3  2009/05/01 19:07:31  mjk
# chimi con queso
#
# Revision 1.2  2008/10/18 00:56:21  mjk
# copyright 5.1
#
# Revision 1.1  2008/05/31 02:57:37  mjk
# - SAGE is back and works (mostly)
# - DMX building from source (in progress)
# - Updated nvidia driver
#

import rocks.commands

class Command(rocks.commands.report.command):
	"""
	Reports the configuration for the SAGE Audio streams to go the
	the master node
	
	<example cmd='report sage audio'>
	</example>
	"""

    
	def run(self, params, args):
		
		privAddr = self.db.getHostAttr('localhost',
			'Kickstart_PrivateAddress')

		self.addText('AudioTileDisplay\n')
		self.addText('\tDeviceID -1\n')
		self.addText('\tSampleFormat Float32\n')
		self.addText('\tSamplingRate 44100\n')
		self.addText('\tChannels 2\n')
		self.addText('\tFramePerBuffer 2048\n')
		self.addText('\tMachines 1\n')
		self.addText('\n')
		self.addText('AudioNode\n')
		self.addText('\tName local\n')
		self.addText('\tIP %s\n' % privAddr)

