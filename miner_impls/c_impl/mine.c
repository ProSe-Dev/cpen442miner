#include <sys/types.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <openssl/md5.h>
#include <openssl/pem.h>

char *base64encode (const void *b64_encode_this, int encode_this_many_bytes){
    BIO *b64_bio, *mem_bio;
    BUF_MEM *mem_bio_mem_ptr;
    b64_bio = BIO_new(BIO_f_base64());
    mem_bio = BIO_new(BIO_s_mem());
    BIO_push(b64_bio, mem_bio);
    BIO_set_flags(b64_bio, BIO_FLAGS_BASE64_NO_NL);
    BIO_write(b64_bio, b64_encode_this, encode_this_many_bytes);
    BIO_flush(b64_bio);
    BIO_get_mem_ptr(mem_bio, &mem_bio_mem_ptr);
    BIO_set_close(mem_bio, BIO_NOCLOSE);
    BIO_free_all(b64_bio);
    BUF_MEM_grow(mem_bio_mem_ptr, (*mem_bio_mem_ptr).length + 1);
    (*mem_bio_mem_ptr).data[(*mem_bio_mem_ptr).length] = '\0';
    return (*mem_bio_mem_ptr).data;
}

unsigned char result[MD5_DIGEST_LENGTH];
unsigned char *hexresult;

unsigned char * bin_to_strhex(const unsigned char *bin, unsigned int binsz,
                                  unsigned char **result)
{
  unsigned char     hex_str[]= "0123456789abcdef";
  unsigned int      i;

  if (!(*result = (unsigned char *)malloc(binsz * 2 + 1)))
    return (NULL);

  (*result)[binsz * 2] = 0;

  if (!binsz)
    return (NULL);

  for (i = 0; i < binsz; i++)
    {
      (*result)[i * 2 + 0] = hex_str[(bin[i] >> 4) & 0x0F];
      (*result)[i * 2 + 1] = hex_str[(bin[i]     ) & 0x0F];
    }
  return (*result);
}

// Get the size of the file by its file descriptor
unsigned long get_size_by_fd(int fd) {
    struct stat statbuf;
    if(fstat(fd, &statbuf) < 0) exit(-1);
    return statbuf.st_size;
}

int startsWith(const char *pre, const char *str)
{
    size_t lenpre = strlen(pre),
           lenstr = strlen(str);
    return lenstr < lenpre ? 0 : memcmp(pre, str, lenpre) == 0;
}

char* str_reverse_malloc(char *str, int len)
{
    char *reverse = malloc(len+1);
    if ( ! reverse) return NULL;
    int i;
    for (i = len-1 ; i >= 0 ; --i) {
        reverse[i] = str[len-i-1];
    }
    reverse[len] = 0;
    return reverse;
}

int main(int argc, char *argv[]) {
    int id_file_descript;
    int prev_hash_file_descript;
    unsigned long id_file_size;
    unsigned long prev_hash_file_size;
    unsigned long coin_blob_size;
    char* id_buffer;
    char* prev_hash_buffer;
    char* full_buffer;
    char* coin_blob;
    unsigned long coin_blob_counter;

    if(argc != 2) { 
        exit(-1);
    }

    sscanf(argv[1], "%lu", &coin_blob_counter);
    char* preamble = "CPEN 442 Coin2019";
    unsigned long preamble_size = strlen(preamble);

    id_file_descript = open("public_id", O_RDONLY);
    if(id_file_descript < 0) exit(-1);

    id_file_size = get_size_by_fd(id_file_descript);

    id_buffer = mmap(0, id_file_size, PROT_READ, MAP_SHARED, id_file_descript, 0);

    prev_hash_file_descript = open("prev_hash", O_RDONLY);
    if(prev_hash_file_descript < 0) exit(-1);

    prev_hash_file_size = get_size_by_fd(prev_hash_file_descript);
    prev_hash_buffer = mmap(0, prev_hash_file_size, PROT_READ, MAP_SHARED, prev_hash_file_descript, 0);

    unsigned long full_size_default = preamble_size + id_file_size + prev_hash_file_size;

    full_buffer = malloc((full_size_default + 8) * sizeof(char));
    memcpy(full_buffer, preamble, preamble_size);
    memcpy(full_buffer + preamble_size, prev_hash_buffer, prev_hash_file_size);

    while (1) {
        coin_blob = (unsigned char*) &coin_blob_counter;
        coin_blob = str_reverse_malloc(coin_blob, strlen(coin_blob));
        coin_blob_size = strlen(coin_blob);
        memcpy(full_buffer + preamble_size + prev_hash_file_size, coin_blob, coin_blob_size);
        memcpy(full_buffer + preamble_size + prev_hash_file_size + coin_blob_size, id_buffer, id_file_size);
        MD5((unsigned char*) full_buffer, full_size_default + coin_blob_size, result);
        bin_to_strhex(result, MD5_DIGEST_LENGTH, &hexresult);
        if (startsWith("00000000", hexresult)) {
            char *base64_encoded = base64encode((char *) coin_blob, coin_blob_size);
            printf("%s", base64_encoded);
            free(base64_encoded);
            return 0;
        }
        coin_blob_counter++;
        free(coin_blob);
    }

    munmap(prev_hash_buffer, prev_hash_file_size);
    munmap(id_buffer, id_file_size);
    free(full_buffer);
    return 0;
}
