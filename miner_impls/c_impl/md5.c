#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/md5.h>

unsigned char result[MD5_DIGEST_LENGTH];

char* get_md5_sum(unsigned char* md, char *buf) {
    int i;
    char* buf2 = buf;
    char* endofbuf = buf + sizeof(buf);
    for (i = 0; i < x; i++)
    {
        /* i use 5 here since we are going to add at most 
        3 chars, need a space for the end '\n' and need
        a null terminator */
        if (buf + 5 < endofbuf)
        {
            if (i > 0)
            {
                buf += sprintf(buf, ":");
            }
            buf += sprintf(buf, "%02X", md[i]);
        }
    }
    buf += sprintf(buf, "\n");
}

// Get the size of the file by its file descriptor
unsigned long get_size_by_fd(int fd) {
    struct stat statbuf;
    if(fstat(fd, &statbuf) < 0) exit(-1);
    return statbuf.st_size;
}

bool startsWith(const char *pre, const char *str)
{
    size_t lenpre = strlen(pre),
           lenstr = strlen(str);
    return lenstr < lenpre ? false : memcmp(pre, str, lenpre) == 0;
}

int main(int argc, char *argv[]) {
    int file_descript;
    unsigned long id_file_size;
    unsigned long prev_hash_file_size;
    char* id_buffer;
    char* prev_hash_buffer;
    unsigned long offset;
    unsigned char* result;
    unsigned char* hexresult;
    char* full_buffer;

    if(argc != 2) { 
        exit(-1);
    }

    char *p;
    long coin_blob_counter = strtol(argv[1], &p, 10);

    file_descript = open("public_id", O_RDONLY);
    if(file_descript < 0) exit(-1);

    id_file_size = get_size_by_fd(file_descript);
    id_buffer = mmap(0, file_size, PROT_READ, MAP_SHARED, file_descript, 0);

    file_descript = open("prev_hash", O_RDONLY);
    if(file_descript < 0) exit(-1);

    prev_hash_file_size = get_size_by_fd(file_descript);
    prev_hash_buffer = mmap(0, file_size, PROT_READ, MAP_SHARED, file_descript, 0);

    full_buffer = malloc((id_file_size + prev_hash_file_size) * sizeof(char));

    while (true) {
        MD5((unsigned char*) file_buffer, file_size, result);
        get_md5_sum(result, hexresult);
        if (startsWith("00000000", hexresult)) {
            printf(hexresult)
            return 0;
        }
        coin_blob_counter++;
    }

    munmap(prev_hash_buffer, prev_hash_file_size);
    munmap(id_buffer, id_file_size); 

    return 0;
}
