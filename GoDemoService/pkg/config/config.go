package config

import "os"

const (
	constServiceName   = "SERVICE_NAME"
	serviceNameDefault = "godemoservice"
	constPort          = "SERVICE_PORT"
	serviceDefaultPort = `8083`

	RouGetDemo   = "demo"
	SpanDemoGet  = "demoget"
	RouPostDemo  = "demo"
	SpanDemoPost = "demopost"
)

var (
	ServiceName = setServiceName()
	DefaultPort = setServicePort()
)

func setServiceName() string {
	val, present := os.LookupEnv(constServiceName)
	if !present {
		val = serviceNameDefault
	}

	return val
}

func setServicePort() string {
	val, present := os.LookupEnv(constPort)
	if !present {
		val = serviceDefaultPort
	}
	val = ":" + val
	return val
}
