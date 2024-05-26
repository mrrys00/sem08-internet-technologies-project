#ARG port=8081
ARG app=cmd/service

FROM golang as builder
ARG app
WORKDIR /app

COPY GoDemoService/go.mod .
COPY GoDemoService/go.sum .

RUN go mod download

COPY GoDemoService/cmd/ cmd
COPY GoDemoService/lib/ lib
COPY GoDemoService/pkg/ pkg

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /out/${app} ./${app}

# final stage
FROM scratch
ARG app
#ARG port
COPY --from=builder /out/${app} /app/

#EXPOSE ${port}
ENTRYPOINT ["/app/service"]
