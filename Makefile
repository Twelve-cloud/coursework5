test:
	cd stocktrader && poetry run pytest
	cd stocktrader && flake8 .

start: docker-compose.yaml
	sudo docker compose build
	sudo docker compose up
