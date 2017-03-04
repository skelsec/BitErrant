import time
import bencode
from hashlib import sha1, md5

def getChunks(data, chunksize = 2**15):
	cl = list()
	for h in [data[i:i+chunksize] for i in range(0, len(data), chunksize)]:
		yield h
		
def readFileData(filename):
	data = ''
	with open(filename,'rb') as f:
		data = f.read()
	return data
	
def writeFileData(data, filename):
	with open(filename,'wb') as f:
		f.write(data)	

def generateTorrentFile(data,filename,chunksize,tracker):
	torrent = {}
	if type(tracker) != list:
		torrent["announce"] = tracker
	elif type(tracker) == list:
		torrent["announce"] = tracker[0]
		# And for some reason, each needs its own list
		torrent["announce-list"] = [[t] for t in tracker]
	torrent["creation date"] = int(time.time())
	torrent["created by"] = 'SkelSec'
	torrent["comment"] = 'Created by SkelSec, pls dont use it for evil'

	info = {}

	info["piece length"] = chunksize
	info["length"] = len(data)
	info["name"] = filename
	########## HAHAHAHAHAAA... NO! info["md5sum"] = md5(data).hexdigest()
	pieces = [ sha1(p).digest() for p in getChunks(data,chunksize) ]
	info["pieces"] = ''.join(pieces)
	torrent["info"] = info
	return bencode.bencode(torrent)
	
def verifyTorrentFile(data, torrent):
	td = bencode.bdecode(torrent)
	chunksize = td['info']['piece length']
	temp = td['info']['pieces']
	pieces_torrent = [temp[i:i+20] for i in range(0, len(temp), 20)]
	pieces_file = [ sha1(p).digest() for p in getChunks(data,chunksize) ]
	if len(pieces_torrent) != len(pieces_file):
		return False
		
	for p1, p2 in zip(pieces_file,pieces_torrent):
		if p1 != p2:
			return False
			
	return True
	