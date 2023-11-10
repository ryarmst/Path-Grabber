#!/usr/bin/env python

# A simple Python 3 script to prepare a list of paths to fuzz from a file of URLs
# Usage: python3 compileDirs.py <URL file> > outputURLs.txt
# Note: will need to install furl: pip3 install furl


# Step 1:python3 pathGrabber.py <URL export from Burp> > known_dirs.txt

# Step 2: host=<hostname>;ffuf -w '/home/dbg/known_dirs.txt:KNOWN' -w '/home/dbg/AppSecVM-Tools/Web App Payloads/Directories/Main/common.txt:FUZZ' -u "https://${host}KNOWN/FUZZ" -od /home/dbg/scans -o "ffuf - $host - Directories (Unauthenticated).csv" -of csv -c

from furl import furl
import os
import sys
import argparse

__version__ = 0.02

def main(arguments):

	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
	
	args = parser.parse_args(arguments)
	
	# Declaration of lists
	directories = []
	
	for url in args.infile:
		urlPath = str(furl(url).path) # Extract just the path component from URLs
		
		# Process incoming path
		urlPath = ProcessURL(urlPath)
					
		# If the path terminates with a '/' add it to our list
		lastIndex = len(urlPath) - 1
		if (urlPath.rfind('/') == lastIndex):
			directories.append(urlPath[0:lastIndex])
		
		# Now iterate up through path segments
		for i in range(len(furl(url).path.segments)):
			urlPath = pathTraverse(urlPath);
			directories.append(urlPath)
			
	# Sort lists and remove duplicates
	directories = sorted(list(dict.fromkeys(directories)))
	
	# Print results 
	for x in directories:
		print(x)

## Returns the path having moved up to the next parent (equivalent to ../, trimming the the rightmost segment)
def pathTraverse(path):
	strLength = len(path)
	lastIndex = strLength - 1
	
	if (path.rfind('/') == lastIndex):
		index = str(path).rfind('/', 0, lastIndex)
	else:
		index = str(path).rfind('/')
	path = path[0:index]
	return path

# Function to clean up paths
def ProcessURL(path):
	path = path.strip('%0A')
	path = path.strip('%22')
	
	# Remove double '/'
	path = path.replace('//','/')
	
	return path
						
							
if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))