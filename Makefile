startapp:
	docker-compose run --rm app sh -c "python manage.py startapp $(app)"

test:
	docker-compose run --rm app sh -c "python manage.py test"

lint:
	docker-compose run --rm app sh -c "flake8"

makemigrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations $(app)"