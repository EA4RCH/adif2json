.PHONY = test coverage clean profile

all: coverage
	echo "Done"

# Clean up
clean:
	rm -rf htmlcov
	rm -rf .coverage

test:
	pytest -vv -s -x --log-cli-level=WARNING tests/

coverage: clean test
	pytest --cov=adif2json --cov-report=html tests/

profile:
	rm -f out/log4om*
	python -m cProfile -o profiling/monoid.prof $$(which adif2json) examples/log4om.adi out/
	snakeviz profiling/monoid.prof
