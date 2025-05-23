FROM python:3.11-bookworm
ARG UID=15371
ARG GID=15371

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            curl \
            build-essential \
            gettext \
            git \
            less \
            libffi-dev \
            libjpeg-dev \
            libmemcached-dev \
            libpq-dev \
            libssl-dev \
            libxml2-dev \
            libxslt1-dev \
            locales \
            nginx \
            python3-virtualenv \
            python3-dev \
            sudo \
            supervisor \
            zlib1g-dev \
            npm && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && \
    apt-get install -y nodejs && \
    wget https://github.com/helix-editor/helix/releases/download/25.01.1/helix_25.1.1-1_amd64.deb && \
    apt-get install -y ./helix_25.1.1-1_amd64.deb && \
    rm -f helix_25.1.1-1_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    dpkg-reconfigure locales && \
	locale-gen C.UTF-8 && \
	/usr/sbin/update-locale LANG=C.UTF-8 && \
    mkdir /etc/pretix && \
    mkdir /data && \
    groupadd -o -g $GID pretixuser && \
    useradd -ms /bin/bash -d /pretix -u $UID -g pretixuser pretixuser && \
    echo 'pretixuser ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    mkdir /static && \
    mkdir /etc/supervisord

ENV LC_ALL=C.UTF-8 \
    DJANGO_SETTINGS_MODULE=production_settings
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=$GITHUB_TOKEN

COPY deployment/docker/pretix.bash /usr/local/bin/pretix
COPY deployment/docker/supervisord /etc/supervisord
COPY deployment/docker/supervisord.all.conf /etc/supervisord.all.conf
COPY deployment/docker/supervisord.web.conf /etc/supervisord.web.conf
COPY deployment/docker/nginx.conf /etc/nginx/nginx.conf
# We are mounting pretix into the dev container, so the following
# will be actually overwritten.
# This is fixed in docker-compose-dev.yaml by also mounting the
# production_settings.py file independently into the src directory.
COPY deployment/docker/production_settings.py /pretix/src/production_settings.py
COPY pyproject.toml /pretix/pyproject.toml
COPY src /pretix/src

ENV DJANGO_SETTINGS_MODULE=
RUN pip3 install -U \
        pip \
        setuptools \
        toml \
        wheel && \
    cd /pretix && \
    python src/set_github_token.py && \
    PRETIX_DOCKER_BUILD=TRUE pip3 install \
        -e ".[memcached]" \
        gunicorn django-extensions ipython && \
    rm -rf ~/.cache/pip
ENV DJANGO_SETTINGS_MODULE=production_settings

RUN chmod +x /usr/local/bin/pretix && \
    rm /etc/nginx/sites-enabled/default && \
    cd /pretix/src && \
    rm -f pretix.cfg && \
	mkdir -p data && \
    chown -R pretixuser:pretixuser /pretix /data data && \
	sudo -u pretixuser make production

USER pretixuser
VOLUME ["/etc/pretix", "/data"]
EXPOSE 80
ENTRYPOINT ["pretix"]
CMD ["all"]
