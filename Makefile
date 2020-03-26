wipo-madrid-fees.csv: process.py ind_taxes.html
	python process.py > $@

ind_taxes.html:
	curl -o $@ https://www.wipo.int/madrid/en/fees/ind_taxes.html