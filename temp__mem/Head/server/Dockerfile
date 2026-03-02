# Build Stage
FROM golang:1.23-alpine AS builder

# Set working directory inside the builder container
WORKDIR /app

# Initialize Go module (if not already done) and download dependencies
# Copying go.mod and go.sum first leverages Docker layer caching
COPY go.mod go.sum* ./
RUN go mod download || true

# Copy the entire source code
COPY . .

# Generate go.sum and resolve all dependencies inside the container
RUN go mod tidy

# Build the Go application statically
# CGO_ENABLED=0 ensures a fully static binary that can run on scratch
# -ldflags="-s -w" strips debug information to further reduce binary size
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-s -w" -o context-engine-server ./cmd/server

# Final lightweight Stage
FROM scratch

# Copy the static binary from the builder stage
COPY --from=builder /app/context-engine-server /context-engine-server

# Set the entrypoint to the compiled binary
ENTRYPOINT ["/context-engine-server"]
