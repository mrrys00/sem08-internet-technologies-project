package utils

import (
	"log"
	"math/rand"
	"time"
)

type DbObject struct {
	StringField string `json:"stringField"`
	IntField    int    `json:"intField"`
	BoolField   bool   `json:"boolField"`
}

func RandomSleep() {
	n := rand.Intn(1024)
	time.Sleep(time.Duration(n) * time.Millisecond)
	log.Printf("Response delayed for %d milliseconds\n", n)
}
