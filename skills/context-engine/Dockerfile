# Build Stage
FROM golang:1.24.13-alpine AS builder

# Set working directory inside the builder container
WORKDIR /app

# Initialize Go module and download dependencies
COPY server/go.mod server/go.sum* ./
RUN go mod download || true

# Copy the entire source code
COPY server/ .

# Generate go.sum and resolve all dependencies
RUN go mod tidy

# Build the Go application statically
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o context-engine-server ./cmd/server

# Final lightweight Stage
FROM scratch

# Copy the static binary from the builder stage
COPY --from=builder /app/context-engine-server /context-engine-server

# Set the entrypoint to the compiled binary
ENTRYPOINT ["/context-engine-server"]
