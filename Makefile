.PHONY: compose-up seed smoke api test

compose-up:
	docker compose up --build

seed:
	docker compose exec api python -m app.seed.seed_acme

smoke:
	docker compose exec api python -m app.scripts.smoke_test

api:
	cd backend && uvicorn app.main:app --reload

test:
	cd backend && python -m pytest -q
