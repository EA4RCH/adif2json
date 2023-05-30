.PHONY = test coverage clean profile

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

profile:
	rm -f out/log4om*
	python -m cProfile -o profiling/direct.prof $$(which adif2json) examples/log4om.adi out/
	snakeviz profiling/direct.prof
