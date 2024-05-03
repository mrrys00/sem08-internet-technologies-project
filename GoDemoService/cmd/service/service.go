package main

import (
	"context"
	"github.com/gin-gonic/gin"
	"github.com/mrrys00/sem08-cloud-shared-services-project/lib/tracing"
	"github.com/mrrys00/sem08-cloud-shared-services-project/pkg/apis"
	"github.com/mrrys00/sem08-cloud-shared-services-project/pkg/config"
	"log"
)

func main() {
	// Create a new Gin router and Jaeger tracer
	r := gin.Default()
	ctx := context.Background()
	tracer := tracing.Init(ctx, config.ServiceName)

	// Routes
	r.GET(config.RouGetDemo, apis.RouGetDemoMiddleware(ctx, tracer))
	r.POST(config.RouPostDemo, apis.RouPostDemoMiddleware(ctx, tracer))

	// Run server
	if err := r.Run(config.DefaultPort); err != nil {
		log.Fatalf("Unable to run server: %v", err)
	} else {
		log.Printf("Server %s started properly", config.ServiceName)
	}

}
