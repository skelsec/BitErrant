Prereq:
1. visual studio
2. python bencode
3. python crypto
4. the SHAtter pdf files (https://shattered.io/)

STEPS:
	1. put your shellcode in the "shellcode" variable in shellcode.py.
		the script will generate the encrypted shellcode and print out parameters "shellcodeEnc" and "shellcodeSize"
	2. open the VS project file, and in TwoFace.cpp replace the parameters you generated.
		(optional) put something useful in the "good" function
		compile the project
	3. place the exe file you've just compiled in the "CodeGeneration\CompiledFile" folder
	4. execute "makeErrant.py" in the "CodeGeneration" folder
		the results will be written in the "output" folder
	5. now you have a file that executes the "good" function, one file that executes the "evil" function and a torrent file, that is valid for BOTH files :)
	6. use it for education purposes only
	
		