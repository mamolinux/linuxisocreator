import subprocess

for line in subprocess.check_output('dpkg-parsechangelog --format rfc822'.split(),
						 universal_newlines=True).splitlines():
	header, colon, value = line.lower().partition(':')
	if header == 'version':
		version = value.strip()
		break
else:
	raise RuntimeError('No version found in debian/changelog')

with open("src/LinuxIsoCreator/VERSION", "w") as f:
	if '~' in version:
		version = version.split('~')[0]
	f.write("%s" % version)
