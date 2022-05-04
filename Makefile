startapp:
	docker-compose run app sh -c "python manage.py startapp $(app)"

test:
	docker-compose run app sh -c "python manage.py test"

makemigrations:
	docker-compose run app sh -c "python manage.py makemigrations $(app)"