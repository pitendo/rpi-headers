#!/usr/bin/python
import os, tempfile

HeaderFilesList = 'header_files.list'
KernelVersionFile = '.rpi_kernel_version'
GitHubBranch = 'rpi-'
GitHubKernelSourceTarballURL = 'https://github.com/raspberrypi/linux/tarball/'

# Execute linux terminal command and return response
def executeCommandReturnResponse(cmd):
	# Create temporary file.
	(fd, filename) = tempfile.mkstemp()

	# Execute command
	os.system(cmd + ' > ' + tempfile)
	
	# Open temporary file and read all lines.
	f.open(filename)
	lines = f.readlines()
	f.close()

	# Delete temporary file
	os.remove(filename)

	if len(lines) == 1:
		return lines[0].strip()
	else:
		return lines

# Join elements in the list to create a path
def joinPath(list):
	str = list[0]
	list.pop(0)
	for elem in list:
		str = str + '/' + elem

	return str

# Recursive function that create the folder structure and download needed files from GitHub
def collectFiles(fullPath, path):
	# Split file path
	list = path.strip().split('/')

	# If the length of list is 1, then list[0] is a file.
	if len(list) == 1:
		# Download file from GitHub.
		os.system('wget https://github.com/raspberrypi/linux/raw/' + GitHubBranch + '/' + fullPath)
	else:
		# If the dir does not exist, create it.
		if not os.path.exists(list[0]):
			os.mkdir(list[0])
		os.chdir(list[0])

		# Remove the current dir name from the list.
		list.pop(0)

		# Call collectFiles recursively with the rest of the path.
		collectFiles(fullPath, joinPath(list))


def processFilesList(file):
	# Open the file
	f = open(file)
	
	# Read file line by line
	for line in f:
		# Build folder structure and collect file listed one the line
		collectFiles(line, line)

# Get kernel version.
kversion = executeCommandReturnResponse('uname -r')

# Determine which GitHub branch to download from.
numbers = kversion.split('.')
GitHubBranch = GitHubBranch + numbers[0] + '.' + numbers[1] + '.y'


# Download Linux kernel source
os.system('wget ' + GitHubKernelSourceTarballURL + GitHubBranch)

# Unzip Linux kernel source
(fd, tempFolder) = tempfile.mkdtemp()
os.system('tar -xzf ' + GitHubBranch + ' -C ' + tempFolder)

# Create folder for Linux headers

processFilesList(HeaderFilesList)