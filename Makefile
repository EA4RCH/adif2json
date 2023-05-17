.PHONY = test coverage clean

all: coverage
	echo "Done"

# Clean up
clean:
	rm -rf htmlcov
	rm -rf .coverage

test:
	pytest -v tests/

coverage: clean test
	pytest --cov=adif2json --cov-report=html tests/
