# Copyright (C) 2023 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#
# This file is part of linuxisocreator.
#
# linuxisocreator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# linuxisocreator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with linuxisocreator. If not, see <http://www.gnu.org/licenses/>
# or write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA..
#
# Author: Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#

# import the necessary modules!
import configparser
import gettext
import locale
import os
import subprocess


# i18n
APP = 'linuxisocreator'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# get version
version_file = os.path.abspath(os.path.dirname(__file__))+'/VERSION'
__version__ = open(version_file, 'r').readlines()[0]

# Constants
CONFIG_DIR = os.path.expanduser('~/.config/linuxisocreator/')
CONFIG_FILE = os.path.join(CONFIG_DIR+'config.cfg')
UI_PATH = os.path.dirname(os.path.realpath(__file__)) + "/ui/"
logfile = open(os.path.join(os.getcwd(),'log'), "w")

class LinuxIsoCreator():
	def __init__(self):
		if os.path.exists(CONFIG_DIR):
			pass
		else:
			os.makedirs(CONFIG_DIR)
		
		self.set_iso_env()
	
	def set_iso_env(self):
		self.project_name = "MamoLinux"
		self.project_dir = self.project_name.lower()+"-iso"
		self.project_arch = "amd64"
		self.project_release = "jammy"
		self.project_version = "22.04.3"
		self.project_codename = "Jammy Jellyfish"
		lts = True
		self.iso = "%s-%s-desktop-%s.iso" % (self.project_name.lower(), self.project_version, self.project_arch)
		if lts:
			self.volid = "%s %s LTS %s" % (self.project_name, self.project_version, self.project_arch)
		else:
			self.volid = "%s %s %s" % (self.project_name, self.project_version, self.project_arch)
		
		print("Project Name: "+self.project_name)
		print("Project Directory: "+self.project_dir)
		print("Version: "+self.project_version)
		print("Release Name: "+self.project_release)
		print("Release Codename: "+self.project_codename)
		print("Long Term Release: "+str(lts))
		print("Architecture: "+self.project_arch)
		print("ISO Filename: "+self.iso)
		print("Volume ID: "+self.volid)
		
		self.project_path = os.getcwd()
		self.rootfsdir = os.path.join(self.project_path, self.project_dir, "rootfs")
		self.livecddir = os.path.join(self.project_path, self.project_dir, "livecd")
		os.makedirs(self.rootfsdir,exist_ok=True)
		os.makedirs(self.livecddir,exist_ok=True)
	
	def BootstrapRelease(self):
		cmd = ['sudo',
			'debootstrap',
			'--arch={}'.format(str(self.project_arch)),
			self.project_release,
			self.rootfsdir]
		# print(cmd)
		# print(" ".join(cmd))
		subprocess.run(cmd, stdout=logfile)
