FROM golang:alpine AS builder

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux

WORKDIR /usr/local/go/src/vkstock/stock_worker

# Copy and download dependency using go mod
#COPY go.mod .
#COPY go.sum .
#RUN go mod download

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

COPY --from=builder /dist/app /


ENTRYPOINT ["/app"]
