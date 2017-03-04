import global_settings
from shellcodeEncryptor import byte2carray, byte2intarray
from generateTorrent import generateTorrentFile, readFileData, writeFileData, verifyTorrentFile



chunksize = global_setting.chunksize
data = ''
with open('shattered-1.pdf','rb') as f:
	data = f.read(chunksize)

#print byte2carray(data) 	
data = '\x00'*chunksize + data + '\x00'*chunksize
writeFileData(byte2intarray(data), "shatter1.carr.txt")


with open('shattered-2.pdf','rb') as f:
	data = f.read(chunksize)
	
#print byte2carray(data)
data = '\x00'*chunksize + data + '\x00'*chunksize
#print byte2carray(data)

	
