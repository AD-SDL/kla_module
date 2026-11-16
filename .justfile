# List available commands
default:
  @just --list --justfile {{justfile()}}

# initialize the project
init:
  @which pdm || echo "pdm not found, you'll need to install it: https://github.com/pdm-project/pdm"
  @pdm install -G:all
  @test -e .env || cp example.env .env
  @which pre-commit && pre-commit install && pre-commit autoupdate || true

# Build the project
build: init dcb

# Run the pre-commit checks
checks:
  @pre-commit run --all-files || { echo "Checking fixes\n" ; pre-commit run --all-files; }
check: checks

# Run automated tests
test:
  @pytest
tests: test
pytest: test

# Build docker image
dcb:
  @docker compose build

# Start the node in docker
up:
  @test -e .env || cp example.env .env
  @docker compose up
