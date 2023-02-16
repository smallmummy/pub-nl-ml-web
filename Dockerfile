FROM ubuntu:18.04

# 安装git、python、nginx、supervisor等，并清理缓存
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        git \
        vim \
        python3.7 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        nginx \
        curl \
        locales \
        net-tools \
        ffmpeg \
        supervisor \
        sqlite3  \
        libmysqlclient-dev && \
        locale-gen --purge "en_US.UTF-8" && \
        update-locale "LANG=en_US.UTF-8" && \
        rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install virtualenv
RUN virtualenv /cnn_venv
RUN /bin/bash -c "source /cnn_venv/bin/activate"
ENV PATH="/cnn_venv/bin:$PATH"
RUN /cnn_venv/bin/pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*
# RUN pip3 install tensorflow --upgrade --force-reinstall

# nginx、supervisor配置
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY conf_files/nginx-app.conf /etc/nginx/conf.d/
COPY conf_files/www.sst123.top_key.key /etc/nginx/cert/
COPY conf_files/www.sst123.top_chain.crt /etc/nginx/cert/
COPY conf_files/supervisor-app.conf /etc/supervisor/conf.d/

ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8

WORKDIR /cnn
COPY . /cnn/
EXPOSE 80
EXPOSE 443
EXPOSE 5000
EXPOSE 9000

CMD ["supervisord", "-n"]


