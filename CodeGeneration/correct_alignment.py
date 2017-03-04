import sys
from shatteredData import shattered1, shattered2

def roundTochunksize(x, base = 10):
	return int(base * round(float(x)/base)) 

def rebaseCollisionData(data, chunksize):
	marker = data.find(shattered1[:0x0F])
	if marker == -1:
		print '[-] Marker not found! Exiting!'
		sys.exit()

	print '[+] Found marker at pos: %s' % (hex(marker),)
	newpos = roundTochunksize(marker, chunksize)
	print '[+] Rebasing data to: %s' % (hex(newpos),)
	if newpos > marker+chunksize or newpos < marker-chunksize:
		print 'Fuckup :('
		sys.exit()
		
	sectionend   = marker+chunksize+chunksize
	sectionstart = marker-chunksize
	
	if newpos > marker:
		goodfile = data[:sectionstart] +'\x00'*(newpos-sectionstart)+ shattered1 + '\x00'*((2*chunksize)-(newpos-sectionstart)) + data[sectionend:] 
		badfile = data[:sectionstart] +'\x00'*(newpos-sectionstart)+ shattered2 + '\x00'*((2*chunksize)-(newpos-sectionstart)) + data[sectionend:] 
	elif newpos < marker:
		goodfile = data[:newpos] + shattered1 + '\x00' * (marker - newpos) +data[sectionend:] 
		badfile = data[:newpos] + shattered2 + '\x00' * (marker - newpos) +data[sectionend:] 
	else:
		goodfile = data[:marker] + shattered1 + data[sectionend-chunksize:]
		badfile = data[:marker] + shattered2 + data[sectionend-chunksize:]
		print '[+] Anint you the lucky one!'
		
	return (goodfile, badfile)