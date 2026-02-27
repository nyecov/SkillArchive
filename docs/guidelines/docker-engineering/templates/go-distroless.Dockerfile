# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /main
# Immutable: Owned by root, executed by non-root
USER 65532:65532
ENTRYPOINT ["/main"]
