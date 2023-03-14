check_defined = \
$(strip $(foreach 1,$1, \
$(call __check_defined,$1,$(strip $(value 2)))))

__check_defined = \
$(if $(value $1),, \
$(error Undefined $1$(if $2, ($2))))

builddocker:
	@:$(call check_defined, tag)
	docker build -t registry.simco.fr/simco/pokedex-back:$(tag) .

migrate:
	python manage.py migrate
