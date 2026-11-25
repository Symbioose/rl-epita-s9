.PHONY: test prepare train validation evaluate report slides
test:
	python -m unittest discover -s tests -v
prepare:
	python scripts/run_experiments.py --phase prepare
train:
	python scripts/run_experiments.py --phase train
validation:
	python scripts/run_experiments.py --phase validation
evaluate:
	python scripts/run_experiments.py --phase test
report:
	python scripts/report.py
slides:
	python presentation/build.py
