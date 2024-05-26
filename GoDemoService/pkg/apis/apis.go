package apis

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/mrrys00/sem08-cloud-shared-services-project/pkg/config"
	"github.com/mrrys00/sem08-cloud-shared-services-project/pkg/utils"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/trace"
	"net/http"
	"strconv"
)

var database []utils.DbObject

func RouGetDemoMiddleware(ctx context.Context, tracer trace.Tracer) gin.HandlerFunc {
	handleHello := func(c *gin.Context) {
		_, span := tracer.Start(c.Request.Context(), config.SpanDemoGet)
		defer span.End()

		propagator := propagation.TraceContext{}
		propagator.Inject(ctx, propagation.HeaderCarrier(c.Request.Header))

		utils.RandomSleep()

		if database == nil {
			c.JSON(http.StatusNotFound, gin.H{"database": "Database is empty"})
			return
		}

		limitStr := c.DefaultQuery("limit", "10")
		limit, err := strconv.Atoi(limitStr)
		if limit < 0 || err != nil {
			c.JSON(http.StatusUnprocessableEntity, gin.H{"error": fmt.Sprintf("Invalid limit: %s. The limit must be positive integer.", limitStr)})
			span.AddEvent("Invalid limit provided")
			return
		}

		if limit > len(database) {
			limit = len(database)
		}

		span.AddEvent(fmt.Sprintf("Return database with limit %d", limit))

		c.JSON(http.StatusOK, gin.H{"database": database[:limit]})
	}

	return gin.HandlerFunc(handleHello)
}

func RouPostDemoMiddleware(ctx context.Context, tracer trace.Tracer) gin.HandlerFunc {
	handleAlert := func(c *gin.Context) {
		_, span := tracer.Start(c.Request.Context(), config.SpanDemoPost)
		defer span.End()

		propagator := propagation.TraceContext{}
		propagator.Inject(ctx, propagation.HeaderCarrier(c.Request.Header))

		utils.RandomSleep()

		var dbObject utils.DbObject
		if err := c.BindJSON(&dbObject); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			span.AddEvent("Cannot bind data")
			return
		}

		if len(dbObject.StringField) == 0 {
			c.JSON(http.StatusUnprocessableEntity, gin.H{"error": "StringField is required and cannot be empty"})
			span.AddEvent("Missing StringField")
			return
		}

		database = append(database, dbObject)
		span.AddEvent("Object saved")

		c.JSON(http.StatusCreated, gin.H{"message": "DbObject saved successfully"})
	}

	return gin.HandlerFunc(handleAlert)
}
