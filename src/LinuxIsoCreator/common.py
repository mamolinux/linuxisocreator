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
import datetime
import gettext
import locale
import os
import subprocess
import sys

from random import choice


# i18n
APP = 'linuxisocreator'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

## Setup logfile
def create_logfile():
	logpath = os.getcwd()
	logfilename = 'isobuild_' + time_now + '.log'
	logfile = os.path.join(logpath, logfilename)
	
	return logfile

# Set the log filename
time_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
logfile = create_logfile()
LOGFILE = open(logfile, "w")

# get version
version_file = os.path.abspath(os.path.dirname(__file__))+'/VERSION'
__version__ = open(version_file, 'r').readlines()[0]

# Constants
CONFIG_DIR = os.path.expanduser('~/.config/linuxisocreator/')
CONFIG_FILE = os.path.join(CONFIG_DIR+'config.cfg')
UI_PATH = os.path.dirname(os.path.realpath(__file__)) + "/ui/"


# This is the backend.
# It contains utility functions to build iso
class LinuxIsoCreator():
	def __init__(self):
		if os.path.exists(CONFIG_DIR):
			pass
		else:
			os.makedirs(CONFIG_DIR)
		
		self.config = configparser.ConfigParser()
		self.save_config()
		self.load_config()
		self.set_iso_env()
	
	def save_config(self):
		"""Saves configurations to config file.
		
		Saves user-defined configurations to config file.
		If the config file does not exist, it creates a new config file
		(~/.config/simple-pwgen/config.cfg)
		in user's home directory.
		"""
		if os.path.exists(CONFIG_FILE):
			pass
		else:
			self.config['default'] = {
				'project-name': "MamoLinux",
				'project-arch': "amd64",
				'project-release': "jammy",
				'project-version': "22.04.3",
				'project-codename': "Jammy Jellyfish",
				'lts': True,
			}
			with open(CONFIG_FILE, 'w') as f:
				self.config.write(f)
	
	def load_config(self):
		"""Loads configurations from config file.
		
		Tries to read and parse from config file.
		If the config file is missing or not readable,
		then it triggers default configurations.
		"""
		self.config.read(CONFIG_FILE)
		try:
			self.project_name = self.config['default']['project-name']
			self.project_arch = self.config['default']['project-arch']
			self.project_release = self.config['default']['project-release']
			self.project_version = self.config['default']['project-version']
			self.project_codename = self.config['default']['project-codename']
			self.lts = self.config['default'].getboolean('lts')
		except:
			self.project_name = "MamoLinux"
			self.project_arch = "amd64"
			self.project_release = "jammy"
			self.project_version = "22.04.3"
			self.project_codename = "Jammy Jellyfish"
			self.lts = True
		
		if not self.project_name:
			LOGFILE.write(_("Project Name should not be empty. Use a valid project name."))
			print(_("Check the log %s for details.") % logfile)
			sys.exit(1)
	
	def set_iso_env(self):
		LOGFILE.write(_("Project Name: %s\n") % self.project_name)
		LOGFILE.write(_("Version: %s\n") % self.project_version)
		LOGFILE.write(_("Release Name: %s\n") % self.project_release)
		LOGFILE.write(_("Release Codename: %s\n") % self.project_codename)
		LOGFILE.write(_("Long Term Release: %s\n") % str(self.lts))
		LOGFILE.write(_("Architecture: %s\n") % self.project_arch)
		
		self.project_path = os.getcwd()
		listdirs = os.listdir(self.project_path)
		for path in listdirs:
			if path.startswith(self.project_name.lower()) and not path.endswith('.log'):
				print(_("Old project exists in %s.") % path)
				ans = input(_("Use %s as the project directory? ") % path)
				if ans.lower() in 'yes':
					self.project_dir = path
					break
				else:
					ans = input(_("Delete the project directory %s? ") % path)
					if ans.lower() in 'yes':
						cmd = ['sudo', 'rm', '-rf', path]
						subprocess.run(cmd, stdout=LOGFILE)
		else:
			self.project_dir = self.project_name.lower()+"_iso_"+time_now
		
		self.iso = "%s-%s-desktop-%s.iso" % (self.project_name.lower(), self.project_version, self.project_arch)
		if self.lts:
			self.volid = "%s %s LTS %s" % (self.project_name, self.project_version, self.project_arch)
		else:
			self.volid = "%s %s %s" % (self.project_name, self.project_version, self.project_arch)
		
		LOGFILE.write(_("Project Directory: %s\n") % self.project_dir)
		LOGFILE.write(_("ISO Filename: %s\n") % self.iso)
		LOGFILE.write(_("Volume ID: %s\n") % self.volid)
		
		self.rootfsdir = os.path.join(self.project_path, self.project_dir, "rootfs")
		self.livecddir = os.path.join(self.project_path, self.project_dir, "tree")
		os.makedirs(self.rootfsdir,exist_ok=True)
		os.makedirs(self.livecddir,exist_ok=True)
	
	def BootstrapRelease(self):
		LOGFILE.write("# ========================Bootstrapping Release======================== #\n")
		cmd = ['sudo',
			'debootstrap',
			str('--arch=' + self.project_arch),
			self.project_release,
			self.rootfsdir]
		try:
			subprocess.run(cmd, stdout=LOGFILE)
			LOGFILE.write("# ========================Bootstrapping complete======================== #\n")
		except:
			LOGFILE.write("Bootstrapping failed.")
			sys.exit(1)
	
	def setuprootfs(self):
		LOGFILE.write("# ========================Setting up rootfs======================== #\n")
		cmd = ['sudo', 'mount', '-o', 'bind', '/dev', str(self.rootfsdir+'/dev')]
		print(cmd)
		# try:
		# 	subprocess.run(cmd, stdout=LOGFILE)
		# 	LOGFILE.write("# ========================Bootstrapping complete======================== #")
		# except:
		# 	LOGFILE.write("Bootstrapping failed.")
		# 	sys.exit(1)
