# Define variables
DOCKER_IMAGE_NAME = properties_scraper
DOCKER_CONTAINER_NAME = scraper

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Docker container with environment variables and detach it
run: build
	docker run -d \
		--name $(DOCKER_CONTAINER_NAME) \
		--env-file .env \
		$(DOCKER_IMAGE_NAME)

# Stop the running Docker container
stop:
	docker stop $(DOCKER_CONTAINER_NAME) || true

# Remove the Docker container
clean-container:
	docker rm $(DOCKER_CONTAINER_NAME) || true

# Remove the Docker image
clean: stop clean-container
	docker rmi $(DOCKER_IMAGE_NAME)

# By default, run the run target (which also builds if necessary)
.DEFAULT_GOAL := run