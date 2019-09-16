.PHONY: run run-pt run-us


run:
	python3 crypto_analysis.py ./data/DemCifrado.txt

run-us:
	python3 crypto_analysis.py -l en-us ./data/20192-teste1.txt

run-pt:
	python3 crypto_analysis.py -l pt-br ./data/20192-teste2.txt