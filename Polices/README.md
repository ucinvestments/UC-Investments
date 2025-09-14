# UC Regents Policy PDF Scraper

This Go application downloads UC Regents policy PDFs from their website by iterating through sequential IDs.

## Features

- Concurrent downloads with 10 workers
- Automatic retry on failure (except for 404s)
- Progress tracking and final statistics
- Dockerized for easy deployment

## Usage

### Local Development

```bash
# Build and run directly
go run main.go

# Or build first
go build -o pdf-scraper
./pdf-scraper
```

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

### Configuration

Edit the constants in `main.go`:
- `startID`: Starting policy ID (default: 0)
- `endID`: Ending policy ID (default: 10000)
- `maxWorkers`: Number of concurrent downloaders (default: 10)
- `outputDir`: Directory to save PDFs (default: ./PDFs)

## Output

Downloaded PDFs are saved in the `PDFs/` directory with the naming pattern: `policy_{id}.pdf`

The script will:
- Skip files that return 404 (not found)
- Retry failed downloads up to 3 times
- Show progress every 100 files processed
- Display final statistics when complete