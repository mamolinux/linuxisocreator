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
import argparse
import gettext
import locale
import sys

from LinuxIsoCreator.common import APP, LOCALE_DIR, __version__, LinuxIsoCreator


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

description =_('Creates custom Ubuntu/Debian Linux ISO from scratch.')

def start_LinISOtorCli():
	# generate password to stdout
	# using configurations from config file
	iso_creator = LinuxIsoCreator()
	iso_creator.BootstrapRelease()


if __name__ == "__main__":
	start_LinISOtorCli()
