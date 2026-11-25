.PHONY: test prepare train validation evaluate report slides figures pdf package
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
figures:
	python scripts/plot_results.py
slides:
	python presentation/build.py --figure results/figures/reussite.png
pdf:
	python scripts/export_pdf.py
package:
	python scripts/package_results.py
