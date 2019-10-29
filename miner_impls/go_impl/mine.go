package main

import (
    "crypto/md5"
	"fmt"
	"flag"
	"log"
	"io/ioutil"
	"strings"
	"strconv"
	"math/big"
	b64 "encoding/base64"
)

func main() {
	flag.Parse()
	offset, _ := strconv.ParseInt(flag.Args()[0], 10, 64)
	preamble := []byte("CPEN 442 Coin2019")
	hash_of_preceding, err := ioutil.ReadFile("test_prev_hash") // b has type []byte
	if err != nil {
		log.Fatal(err)
	}
	id_of_miner, err := ioutil.ReadFile("test_public_id") // b has type []byte
	if err != nil {
		log.Fatal(err)
	}
	one := big.NewInt(1)
	coin_blob_ctr := big.NewInt(offset)
	for {
		coin_blob := coin_blob_ctr.Bytes()
		md5Data :=
		append(append(
		append(preamble, hash_of_preceding...),
		coin_blob...),
		id_of_miner...)
		sum := fmt.Sprintf("%x", md5.Sum(md5Data))
		if strings.HasPrefix(sum, "00000000") {
			sEnc := b64.StdEncoding.EncodeToString(coin_blob)
			fmt.Print(sEnc)
			return
		}
		coin_blob_ctr.Add(coin_blob_ctr, one)
	}
}