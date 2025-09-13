.PHONY: build run unify clean docker-build docker-run help

# Default target
help:
	@echo "BDS Data Unification - Available commands:"
	@echo "  make run          - Run the unification script locally"
	@echo "  make docker-build - Build the Docker image"
	@echo "  make docker-run   - Run unification in Docker container"
	@echo "  make compose-up   - Run with docker-compose"
	@echo "  make clean        - Remove unified output files"
	@echo "  make test         - Test the unification with current data"

# Run the unification script locally
run:
	python3 unify_bds_data.py --path . --output unified_bds_data.json

# Build Docker image
docker-build:
	docker build -t bds-unifier .

# Run Docker container
docker-run: docker-build
	docker run -v $$(pwd)/boycott.thewitness/output:/app/boycott.thewitness/output:ro \
	           -v $$(pwd)/dontbuyintooccupation.org/output:/app/dontbuyintooccupation.org/output:ro \
	           -v $$(pwd)/investigate.afsc.org:/app/investigate.afsc.org:ro \
	           -v $$(pwd)/unified_output:/app/data \
	           bds-unifier

# Run with docker-compose
compose-up:
	docker-compose up --build

# Run in background with docker-compose
compose-up-d:
	docker-compose up -d --build

# Stop docker-compose
compose-down:
	docker-compose down

# Test the unification
test:
	@echo "Testing BDS data unification..."
	@python3 unify_bds_data.py --path . --output test_unified_data.json
	@echo "Test output saved to test_unified_data.json"

# Clean up generated files
clean:
	rm -f unified_bds_data.json unified_bds_data_compact.json unified_bds_data_summary.csv
	rm -f test_unified_data.json test_unified_data_compact.json test_unified_data_summary.csv
	rm -rf unified_output/

# View statistics from the unified data
stats:
	@if [ -f unified_bds_data.json ]; then \
		python3 -c "import json; \
		with open('unified_bds_data.json') as f: data = json.load(f); \
		print('Total entities:', data['metadata']['total_entities']); \
		print('\nStatistics:'); \
		for k, v in data['metadata']['statistics'].items(): \
			if isinstance(v, dict): \
				print(f'  {k}:'); \
				for k2, v2 in v.items(): print(f'    - {k2}: {v2}'); \
			else: print(f'  {k}: {v}')"; \
	else \
		echo "No unified data found. Run 'make run' first."; \
	fi