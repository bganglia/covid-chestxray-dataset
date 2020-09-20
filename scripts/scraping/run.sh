source scraping_environment/bin/activate
python combined_interface.py --search "covid" --images new_covid/ --csv new_covid.csv --old ../../metadata.csv --using internal --max 10000000000000000000000 --exclude exclude.txt
