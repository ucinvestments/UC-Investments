# Build stage
FROM golang:1.21-alpine AS builder

# Install dependencies for building
RUN apk add --no-cache git

# Set working directory
WORKDIR /app

# Copy go mod files (create them if they don't exist)
COPY go.* ./

# Initialize go module if not exists and download dependencies
RUN if [ ! -f go.mod ]; then go mod init pdf-scraper; fi && \
    go mod tidy

# Copy source code
COPY main.go .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o pdf-scraper .

# Final stage
FROM alpine:latest

# Install ca-certificates for HTTPS requests
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy the binary from builder
COPY --from=builder /app/pdf-scraper .

# Create PDFs directory
RUN mkdir -p /app/PDFs

# Run the application
CMD ["./pdf-scraper"]