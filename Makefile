PYSOURCES := $(wildcard python/*.py)
PYCR_TARGETS := $(addprefix python/., $(addsuffix .json, $(notdir $(PYSOURCES))))


TIME_FMT := /usr/bin/time -f '","real": "%E","user":"%U","sys":"%S","avemem": "%t","problem":"%C"}'
PYTHON_RESULT := python_result.json

$(PYCR_TARGETS): python/.%.py.json: python/%.py
	test -d $(dir $@) || mkdir -p $(dir $@)
	PYTHONPATH=. $(TIME_FMT) python $< 2>&1 | tr -d '\n' | sed -e 's/^/{"output":"/' -e 's#python python/\(problem\)*\([0-9]*\).py#\2#' > python/.$(notdir $<).json

pyc: $(PYCR_TARGETS)
python:pyc
	echo '{"python": [' > $(PYTHON_RESULT)
	cat $(PYCR_TARGETS) | sed 's/}{/},\n{/g' >> $(PYTHON_RESULT)
	echo "]}" >> $(PYTHON_RESULT)


clean:
	rm -vrf $(PYCR_TARGETS)

.PHONY: pyc clean
