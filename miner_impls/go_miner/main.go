import (
	"crypto/md5"
	"net/http"
)

// TODO: don't expose secrets
func getPrivateID(idOfMiner string) []byte {
	return md5.Sum(idOfMiner)
}

func main() {
	minerId := flag.String("id", "", "Miner ID")
	flag.Parse()
	hashOfPreceding := "123"
	coinBlob := []byte("1")
	data := 
	append([]byte("CPEN 442 Coin2019"),
	 []byte(hashOfPreceding),
	 coinBlob,
	 []byte(idOfMiner)
}
