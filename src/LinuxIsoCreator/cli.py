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
import gettext
import locale
import logging
import os

from LinuxIsoCreator.common import APP, LOCALE_DIR, LOGFILE, LinuxIsoCreator


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# logger
module_logger = logging.getLogger('LinuxIsoCreator.cli')

def start_LinISOtorCli():
	iso_creator = LinuxIsoCreator()
	
	ans = input(_("Bootstrap %s? ") % iso_creator.project_release)
	if ans.lower() in 'yes':
		iso_creator.BootstrapRelease()
	
	ans = input(_("Delete log file %s? ") % LOGFILE)
	if ans.lower() in 'yes':
		os.system("rm -f %s" % LOGFILE)
