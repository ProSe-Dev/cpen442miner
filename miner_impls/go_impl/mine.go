package main

import (
    "crypto/md5"
	"fmt"
	"flag"
	"strconv"
	"log"
	"io/ioutil"
	"strings"
)

func main() {
	flag.Parse()
	offset, _ := strconv.Atoi(flag.Args()[0])
	preamble := []byte("CPEN 442 Coin2019")
	hash_of_preceding, err := ioutil.ReadFile("prev_hash") // b has type []byte
	if err != nil {
		log.Fatal(err)
	}
	id_of_miner, err := ioutil.ReadFile("public_id") // b has type []byte
	if err != nil {
		log.Fatal(err)
	}
	coin_blob_ctr := offset
	for {
		coin_blob := []byte(strconv.Itoa(coin_blob_ctr))
		md5Data :=
		append(append(
		append(preamble, hash_of_preceding...),
		coin_blob...),
		id_of_miner...)
		sum := fmt.Sprintf("%x", md5.Sum(md5Data))
		if strings.HasPrefix(sum, "00000000") {
			fmt.Print(sum)
			return
		}
		coin_blob_ctr += 1
	}
}