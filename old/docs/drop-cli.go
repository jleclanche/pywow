package main

import (
	"code.google.com/p/go.net/websocket"
	"fmt"
	"io"
	"io/ioutil"
	"os"
)

func main() {
	upfile, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	ws, err := websocket.Dial("ws://ws.robertnix.me:80/i", "", "http://robertnix.me")
	if err != nil {
		panic(err)
	}

	_, err = io.WriteString(ws, "nstdin")
	if err != nil {
		panic(err)
	}
	for i := 0; i < len(upfile); i += 8192 {
		n := i + 8192
		if n > len(upfile) {
			n = len(upfile)
		}
		_, err = ws.Write(append([]byte("+"), upfile[i:n]...))
		if err != nil {
			panic(err)
		}
	}
	_, err = ws.Write([]byte("="))
	if err != nil {
		panic(err)
	}
	filename := make([]byte, 10)
	_, err = ws.Read(filename)
	if err != nil {
		panic(err)
	}
	fmt.Println("http://robertnix.me/" + string(filename))
}

