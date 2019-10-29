#include <openssl/md5.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

// rip TODO

typedef unsigned char BYTE;

void string2ByteArray(char* input, BYTE* output)
{
    int loop;
    int i;
    
    loop = 0;
    i = 0;
    
    while(input[loop] != '\0')
    {
        output[i++] = input[loop++];
    }
}

char* concat(char* a, size_t a_size,
             char* b, size_t b_size) {
    char* c = realloc(a, a_size + b_size);
    memcpy(c + a_size, b,  b_size);  // dest is after "a" data, source is b with b_size
    free(b);
    return c;
}

int main()
{
    int n;
    MD5_CTX c;
    unsigned char out[MD5_DIGEST_LENGTH];
    char preamble[] = "CPEN 442 Coin2019"

    int len = strlen(preamble);
    BYTE buf[len];

    string2ByteArray(preamble, arr);

    FILE *fileptr;
    char *id_buffer;
    long filelen;

    fileptr = fopen("public_id", "rb");  // Open the file in binary mode
    fseek(fileptr, 0, SEEK_END);          // Jump to the end of the file
    filelen = ftell(fileptr);             // Get the current byte offset in the file
    rewind(fileptr);                      // Jump back to the beginning of the file

    id_buffer = (char *)malloc((filelen+1)*sizeof(char)); // Enough memory for file + \0
    fread(id_buffer, filelen, 1, fileptr); // Read in the entire file
    fclose(fileptr); // Close the file

    char *prev_hash_buffer;

    fileptr = fopen("prev_hash", "rb");  // Open the file in binary mode
    fseek(fileptr, 0, SEEK_END);          // Jump to the end of the file
    filelen = ftell(fileptr);             // Get the current byte offset in the file
    rewind(fileptr);                      // Jump back to the beginning of the file

    prev_hash_buffer = (char *)malloc((filelen+1)*sizeof(char)); // Enough memory for file + \0
    fread(prev_hash_buffer, filelen, 1, fileptr); // Read in the entire file
    fclose(fileptr); // Close the file

    

    MD5_Init(&c);

    bytes = 

    while(bytes > 0)
    {
        MD5_Update(&c, buf, bytes);
        bytes=read(STDIN_FILENO, buf, 512);
    }

    MD5_Final(out, &c);

    for(n=0; n<MD5_DIGEST_LENGTH; n++)
        printf("%02x", out[n]);
    printf("\n");

    return(0);        
}
