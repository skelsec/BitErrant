import global_settings
from generateTorrent import  readFileData

shattered1= readFileData('..\SHAtterFiles\shattered-1.pdf')[:global_settings.chunksize]

shattered2= readFileData('..\SHAtterFiles\shattered-2.pdf')[:global_settings.chunksize]