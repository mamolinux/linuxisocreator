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
import logging
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
LOGFILE = create_logfile()

# logger
module_logger = logging.getLogger('LinuxIsoCreator.common')

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
		(~/.config/linuxisocreator/config.cfg)
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
			module_logger.debug(_("Project Name should not be empty. Use a valid project name."))
			module_logger.debug(_("Check the log %s for details.") % LOGFILE)
			sys.exit(1)
	
	def capture_subprocess_output(self, cmd):
		with open(LOGFILE, 'a+') as logger:
			subprocess.run(cmd, stdout=logger, stderr=logger)
	
	# def prompt_sudo(self):
	# 	ret = 0
	# 	if os.geteuid() != 0:
	# 		msg = "[sudo] password for %u:"
	# 		ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
	# 	return ret

	def set_iso_env(self):
		module_logger.debug(_("Project Name: %s") % self.project_name)
		module_logger.debug(_("Version: %s") % self.project_version)
		module_logger.debug(_("Release Name: %s") % self.project_release)
		module_logger.debug(_("Release Codename: %s") % self.project_codename)
		module_logger.debug(_("Long Term Release: %s") % str(self.lts))
		module_logger.debug(_("Architecture: %s") % self.project_arch)
		
		self.project_path = os.getcwd()
		listdirs = os.listdir(self.project_path)
		for path in listdirs:
			if path.startswith(self.project_name.lower()+'_iso_') and not path.endswith('.log'):
				module_logger.debug(_("Old project exists in %s.") % path)
				ans = input(_("Use %s as the project directory? ") % path)
				if ans.lower() in 'yes':
					self.project_dir = path
					break
				else:
					ans = input(_("Delete the project directory %s? ") % path)
					if ans.lower() in 'yes':
						cmd = ['sudo', 'rm', '-rf', path]
						self.capture_subprocess_output(cmd)
		else:
			self.project_dir = self.project_name.lower()+"_iso_"+time_now
		
		self.iso = "%s-%s-desktop-%s.iso" % (self.project_name.lower(), self.project_version, self.project_arch)
		if self.lts:
			self.volid = "%s %s LTS %s" % (self.project_name, self.project_version, self.project_arch)
		else:
			self.volid = "%s %s %s" % (self.project_name, self.project_version, self.project_arch)
		
		module_logger.debug(_("Project Directory: %s") % self.project_dir)
		module_logger.debug(_("ISO Filename: %s") % self.iso)
		module_logger.debug(_("Volume ID: %s") % self.volid)
		
		self.rootfsdir = os.path.join(self.project_path, self.project_dir, "rootfs")
		self.livecddir = os.path.join(self.project_path, self.project_dir, "tree")
		os.makedirs(self.rootfsdir,exist_ok=True)
		os.makedirs(self.livecddir,exist_ok=True)
		
		self.capture_subprocess_output(['sudo', 'chown', '-R', 'root:root', self.rootfsdir])
	
	def BootstrapRelease(self):
		module_logger.debug("\n# ========================Bootstrapping Release======================== #")
		cmd = ['sudo',
			'debootstrap',
			str('--arch=' + self.project_arch),
			self.project_release,
			self.rootfsdir]
		try:
			self.capture_subprocess_output(cmd)
			module_logger.debug("# ========================Bootstrapping complete======================== #")
		except:
			module_logger.debug("Bootstrapping failed.")
			sys.exit(1)
	
	def mount_dirs(self):
		"""
		Mounts or binds directories or filesystems
		to rootfs required for logging and installation
		of anything using the package desktop-base or grub
		"""
		mountflag = "Mounting"
		
		module_logger.debug("\n# ========================Mounting directories======================== #")
		# bind /dev to rootfs/dev
		mountfs = '/dev'
		mountedpath = str(self.rootfsdir + mountfs)
		cmd = ['sudo', 'mount', '-o', 'bind', mountfs, mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountfs)
		
		# mount /dev/pts to rootfs/dev/pts
		mountfs = 'devpts'
		mountedpath = str(self.rootfsdir + '/dev/pts')
		cmd = ['sudo', 'mount', 'none', '-t', mountfs, mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountfs)
		
		# mount /proc to rootfs/proc
		mountfs = 'proc'
		mountedpath = str(self.rootfsdir + '/proc')
		cmd = ['sudo', 'mount', 'none', '-t', mountfs, mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountfs)
		
		# mount /sys to rootfs/sys
		mountfs = 'sysfs'
		mountedpath = str(self.rootfsdir + '/sys')
		cmd = ['sudo', 'mount', 'none', '-t', mountfs, mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountfs)
		module_logger.debug("# ========================Mounting successful======================== #")
	
	def unmount_dirs(self):
		"""
		Unmounts directories or filesystems from rootfs.
		"""
		mountflag = "Unmounting"
		
		module_logger.debug("\n# ========================Unounting directories======================== #")
		# Unmount rootfs/dev/pts
		mountedpath = str(self.rootfsdir + '/dev/pts')
		cmd = ['sudo', 'umount', mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountedpath)
		
		# Unmount rootfs/dev
		mountedpath = str(self.rootfsdir + '/dev')
		cmd = ['sudo', 'umount', mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountedpath)
		
		# Unmount rootfs/proc
		mountedpath = str(self.rootfsdir + '/proc')
		cmd = ['sudo', 'umount', mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountedpath)
		
		# Unmount rootfs/sys
		mountedpath = str(self.rootfsdir + '/sys')
		cmd = ['sudo', 'umount', mountedpath]
		self.run_mount_dirs(cmd, mountflag, mountedpath)
		module_logger.debug("# ========================Unounting successful======================== #")
	
	def run_mount_dirs(self, cmd, mountflag, mountfs=None):
		try:
			self.capture_subprocess_output(cmd)
		except:
			module_logger.debug("%s %s failed." % (mountflag, mountfs))
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
