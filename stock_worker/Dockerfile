FROM golang:alpine AS builder

ENV GO111MODULE=off \
    CGO_ENABLED=0 \
    GOOS=linux

RUN apk --no-cache add ca-certificates
RUN apk add git

WORKDIR /usr/local/go/src/vkstock/stock_worker

# Copy and download dependency using go mod
#COPY go.mod .
#COPY go.sum .
#RUN go mod download

RUN go get -u -v gopkg.in/ahmdrz/goinsta.v2

# Copy the code into the container
COPY . .

# Build the application
RUN go build -o app -i ./main/main.go

# Move to /dist directory as the place for resulting binary folder
WORKDIR /dist

# Copy binary from build to main folder
RUN cp /usr/local/go/src/vkstock/stock_worker/app .


# Build a small image
FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /dist/app /


ENTRYPOINT ["/app"]
