FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN groupadd -r simadm; \
	useradd -r -m -g simadm simadm; \
	mkdir /app; \
	chown simadm /app; \
	apt-get update; \
	apt-get install -y locales postgresql-client locales-all python3-dev

ENV GOSU_VERSION 1.12
RUN apt-get update; \
        apt-get installation -y --no-install-recommends ca-certificates wget; \
        dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
        wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
        wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
        gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
        gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
        rm -rf /usr/local/bin/gosu.asc; \
        chmod +x /usr/local/bin/gosu; \
        gosu --version; \
        gosu nobody true

WORKDIR /app
ENV PATH /home/simadm/.local/bin:/home/simadm/.poetry/bin:$PATH
RUN gosu simadm bash -c "curl -sSL https://install.python-poetry.org | python - --version 1.1.15"
COPY poetry.lock pyproject.toml /app/
RUN gosu simadm bash -c "poetry config virtualenvs.create false && poetry install --no-dev && export LC_ALL=fr_FR.UTF-8 && export LANG=fr_FR.UTF-8 && locale-gen fr_FR.UTF-8"
COPY . /app
RUN cp /app/pokedex-back/settings_docker_example.py /app/pokedex-back/settings_docker.py
RUN chown -R simadm:simadm /app
ENTRYPOINT ["./entrypoint.sh"]
EXPOSE 8030
