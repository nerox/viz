# $Id: plugin_meta.py,v 1.1 2009/06/06 00:56:30 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: plugin_meta.py,v $
# Revision 1.1  2009/06/06 00:56:30  mjk
# *** empty log message ***
#

import os
import string
import rocks.commands.sync.viz

class Plugin(rocks.commands.sync.viz.Plugin):
	"""
	Meta Mode Plugin

	Using the viz layout in the database compute the xorg.conf file for
	all managed Tiles.  For single tile hosts this pluging call the Simple
	Mode configureHost method.  For multi-tile hosts pairs of GPUs are
	TwinView configured and then these pairs are Xinerama connect.  It is
	assumed that the orientation of TwinView and Xinerama are indentical.
	This means that you can define rows or cols of multi-tile hosts but
	cannot define a square of tiles on one host.

	Both Sage and CGLX work well in this mode for multi-tile hosts.
	Chromium does not work in this mode with multi-tile hosts.
	"""

	def provides(self):
		return 'meta'

	def configureHost(self, owner, host):
		tiles = self.getHostTiles(host)
		if len(tiles) == 1:
			return self.methods['simple'].configureHost(owner, host)

		if tiles[0]['x'] > tiles[1]['x']:
			orientation = 'LeftOf'
		elif tiles[0]['x'] < tiles[1]['x']:
			orientation = 'RightOf'
		elif tiles[0]['y'] < tiles[1]['y']:
			orientation = 'Above'
		elif tiles[0]['y'] > tiles[1]['y']:
			orientation = 'Below'
		else:
			return # bad config, skip node

		flags  = '--force-generate -a'
		flags += ' --twinview --twinview-orientation=%s' % orientation
		if len(tiles) <= 2:
			flags += ' --no-xinerama'
		else:
			flags += ' --xinerama'

		xconf = '%s-meta-%s' % (self.getXConfPath(), host)
		os.system('ssh -x %s "/opt/viz/bin/nvidia-xconfig %s"' %
		      	(host, flags))
		self.getFileFromHost(host, self.getXConfPath(), xconf)

		list = []
		fin  = open(xconf, 'r')
		display = -1
		for line in fin.readlines():
			line = line.replace('RightOf', orientation)
			if line.find('Option         "DPMS"') != -1:
				line = '\tOption\t"DPMS"\t"False"\n'
			elif line.find('Section "Screen"') != -1:
				display += 1
			elif line.find('Option         "MetaModes"') != -1:
				line = '\tOption\t"MetaModes" "%sx%s,%sx%s"\n'\
				    % (tiles[display*2]['xres'], 
				       tiles[display*2]['yres'],
				       tiles[display*2+1]['xres'],
				       tiles[display*2+1]['yres'])
			list.append(line)
		fin.close()
		fout = open(xconf, 'w')
		for line in list:
			fout.write(line)
		fout.close()

		self.sendXConf(host, 'meta')




