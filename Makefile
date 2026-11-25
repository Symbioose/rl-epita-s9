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
	python presentation/build.py
pdf:
	python scripts/export_pdf.py
	python scripts/export_pdf.py --source presentation/annexes.html --output presentation/annexes.pdf
package:
	python scripts/package_results.py
