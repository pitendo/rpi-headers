#!/usr/bin/python
import os, sys, tempfile

WorkingDirectory = os.getcwd()
HeaderFilesList = os.path.realpath('header_files.list')
GitHubBranch = 'rpi-'
GitHubKernelSourceTarballURL = 'https://github.com/raspberrypi/linux/tarball/'
KernelSourcePath = ''
LinuxHeaderPath = ''
LinuxHeaderVersion = ''
TempFile = ''
TempFolder = ''

# Execute linux terminal command and return response.
#
# @param cmd The Linux termioal command to be executed
# @return The response from the command
#
def executeCommandReturnResponse(cmd):
	filename = global TempFile
	# Execute command
	os.system(cmd + ' > ' + filename)
	
	# Open temporary file and read all lines.
	f.open(filename)
	lines = f.readlines()
	f.close()

	if len(lines) == 1:
		return lines[0].strip()
	else:
		return lines

# Join elements in the list to create a path.
#
# @param list List of elements to be joined
# @result Resulting path
#
def joinPath(list):
	str = list[0]
	list.pop(0)
	for elem in list:
		str = str + '/' + elem

	return str

# Recursive function that create folder structure and copy kernel source file to new directory.
#
# @param fullPath Full path to the source file
# @param path Minimized path
#
def moveFile(fullPath, path):
	# Split file path
	list = path.strip().split('/')

	# If the length of list is 1, then list[0] is a file.
	if len(list) == 1:
		# Move file to new folder
		os.system('mv '  + KernelSourcePath + fullPath + ' .')
	else:
		# If the dir does not exist, create it.
		if not os.path.exists(list[0]):
			os.mkdir(list[0])
		os.chdir(list[0])

		# Remove the current dir name from the list.
		list.pop(0)

		# Call collectFiles recursively with the rest of the path.
		moveFile(fullPath, joinPath(list))

# Go through the list of header files needed to create the Linux headers.
#
# @param file The file that list all needed files
#
def moveAllListedFiles(file):
	# Open the file.
	f = open(file)
	
	# Read file line by line.
	for line in f:
		# Go to base of Linux header folder.
		os.chdir(LinuxHeaderPath)
		# Build folder structure and collect file listed one the line.
		moveFile(line, line)

	# Return to working directory.
	os.chdir(WorkingDirectory)


#   __  __       _
#  |  \/  |     (_)
#  | \  / | __ _ _ _ __
#  | |\/| |/ _` | | '_ \
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|
#

# Get kernel version.
kversion = executeCommandReturnResponse('uname -r')

# Store path to Linux header folder.
lhfolder = 'linux-headers-' + kversion

# Check if Linux headers folder already exists.
if os.path.exists(lhfolder):
	# Prompt user that it already exists and exit.
	print 'The folder "' + lhfolder + '" already exists!'
	exit()

# Create folder for Linux headers.
os.mkdir(lhfolder)

# Create temporary file.
(fd, filename) = tempfile.mkstemp()
TempFile = filename.split('/')[2]

# Save oath to Linux header folder.
LinuxHeaderPath = WorkingDirectory + '/' + lhfolder + '/'

# Determine which GitHub branch to download from.
numbers = kversion.split('.')
GitHubBranch = GitHubBranch + numbers[0] + '.' + numbers[1] + '.y'

# Download Linux kernel source.
os.system('wget ' + GitHubKernelSourceTarballURL + GitHubBranch)

# Unzip Linux kernel source.
TempFolder = tempfile.mkdtemp().split('/')[2]
os.mkdir(tempfolder)
os.system('tar -xzf ' + GitHubBranch + '-C ' + TempFolder)

# Store path to base dir of kernel source.
KernelSourcePath = pwd + '/' + TempFolder + '/' + executeCommandReturnResponse('ls ' + TempFolder + '/raspberrypi-linux-*') + '/'

# Copy all files listed in the header files list.
moveAllListedFiles(HeaderFilesList)

# Compress Linux header files
os.system('tar czf ' + lhfolder + '.tar.gz ' + lhfolder)

# Remove temporary files, folders and archives.
os.remove(TempFile)
os.system('rm -r ' + TempFolder)
os.remove(GitHubBranch)


