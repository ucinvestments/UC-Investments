package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"
)

const (
	startID      = 0
	endID        = 10000
	maxWorkers   = 10
	retryAttempts = 3
	retryDelay    = 2 * time.Second
	outputDir     = "./PDFs"
)

type downloadJob struct {
	id  int
	url string
}

type downloadResult struct {
	id      int
	success bool
	message string
}

func main() {
	fmt.Printf("Starting UC Regents Policy PDF downloader...\n")
	fmt.Printf("Downloading PDFs from ID %d to %d\n", startID, endID)

	// Create output directory if it doesn't exist
	if err := os.MkdirAll(outputDir, 0755); err != nil {
		fmt.Printf("Error creating output directory: %v\n", err)
		return
	}

	// Create channels for job distribution
	jobs := make(chan downloadJob, 100)
	results := make(chan downloadResult, 100)

	// Start worker goroutines
	var wg sync.WaitGroup
	for w := 0; w < maxWorkers; w++ {
		wg.Add(1)
		go worker(w, jobs, results, &wg)
	}

	// Start result processor
	done := make(chan bool)
	go processResults(results, done)

	// Generate and send jobs
	go func() {
		for id := startID; id <= endID; id++ {
			url := fmt.Sprintf("https://regents.universityofcalifornia.edu/policies/%d.pdf", id)
			jobs <- downloadJob{id: id, url: url}
		}
		close(jobs)
	}()

	// Wait for all workers to complete
	wg.Wait()
	close(results)

	// Wait for result processor to finish
	<-done

	fmt.Println("\nDownload complete!")
}

func worker(id int, jobs <-chan downloadJob, results chan<- downloadResult, wg *sync.WaitGroup) {
	defer wg.Done()

	client := &http.Client{
		Timeout: 30 * time.Second,
	}

	for job := range jobs {
		success := false
		message := ""

		for attempt := 1; attempt <= retryAttempts; attempt++ {
			err := downloadPDF(client, job.url, job.id)
			if err == nil {
				success = true
				message = fmt.Sprintf("Downloaded successfully")
				break
			}

			// Check if it's a 404 error
			if err.Error() == "file not found" {
				message = "File not found (404)"
				break // Don't retry for 404 errors
			}

			// Retry for other errors
			if attempt < retryAttempts {
				time.Sleep(retryDelay)
			} else {
				message = fmt.Sprintf("Failed after %d attempts: %v", retryAttempts, err)
			}
		}

		results <- downloadResult{
			id:      job.id,
			success: success,
			message: message,
		}
	}
}

func downloadPDF(client *http.Client, url string, id int) error {
	// Make the request
	resp, err := client.Get(url)
	if err != nil {
		return fmt.Errorf("request failed: %v", err)
	}
	defer resp.Body.Close()

	// Check response status
	if resp.StatusCode == 404 {
		return fmt.Errorf("file not found")
	}
	if resp.StatusCode != 200 {
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	// Check content type
	contentType := resp.Header.Get("Content-Type")
	if contentType != "application/pdf" && contentType != "application/octet-stream" {
		// Sometimes PDFs are served with different content types
		if len(contentType) > 0 && contentType != "text/html" {
			fmt.Printf("Warning: Unexpected content type for ID %d: %s\n", id, contentType)
		} else {
			return fmt.Errorf("not a PDF file (content-type: %s)", contentType)
		}
	}

	// Create the output file
	filename := filepath.Join(outputDir, fmt.Sprintf("policy_%d.pdf", id))
	out, err := os.Create(filename)
	if err != nil {
		return fmt.Errorf("failed to create file: %v", err)
	}
	defer out.Close()

	// Download the file
	written, err := io.Copy(out, resp.Body)
	if err != nil {
		os.Remove(filename) // Clean up partial file
		return fmt.Errorf("failed to save file: %v", err)
	}

	// Verify file size
	if written == 0 {
		os.Remove(filename) // Clean up empty file
		return fmt.Errorf("downloaded file is empty")
	}

	return nil
}

func processResults(results <-chan downloadResult, done chan<- bool) {
	successCount := 0
	failCount := 0
	notFoundCount := 0

	for result := range results {
		if result.success {
			successCount++
			fmt.Printf(" ID %d: %s\n", result.id, result.message)
		} else if result.message == "File not found (404)" {
			notFoundCount++
			// Don't print for each 404 to reduce noise
			if notFoundCount%100 == 0 {
				fmt.Printf("... %d files not found so far ...\n", notFoundCount)
			}
		} else {
			failCount++
			fmt.Printf(" ID %d: %s\n", result.id, result.message)
		}

		// Print progress every 100 files
		total := successCount + failCount + notFoundCount
		if total%100 == 0 {
			fmt.Printf("\n=== Progress: %d processed | %d downloaded | %d not found | %d failed ===\n\n",
				total, successCount, notFoundCount, failCount)
		}
	}

	fmt.Printf("\n=== Final Results ===\n")
	fmt.Printf("Total processed: %d\n", successCount+failCount+notFoundCount)
	fmt.Printf("Successfully downloaded: %d\n", successCount)
	fmt.Printf("Files not found (404): %d\n", notFoundCount)
	fmt.Printf("Failed downloads: %d\n", failCount)

	done <- true
}