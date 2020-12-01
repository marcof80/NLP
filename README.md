# LASI NLP

## Start service

1. Download `nlp.lasi`, unzip if necessary, and add to this folder.
2. Run `docker load -i nlp.lasi` to load local image.
3. Modify `docker-compose.yml` file accordingly. 
4. Run `docker-compose up` to start service.

## Test service

1. Open `lasi_nlp/entry_points.py` and modify `LASI_SERVICE` variable to the service URI.
2. Open `Demo.ipynb` notebook to test service