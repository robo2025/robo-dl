FROM robo2025/docker-deep-learn:release-1.0.1
ENV PYTHONUNBUFFERED 1


COPY . /project/dl_api

WORKDIR /project/dl_api

RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple && \
#    pip3 install --no-cache-dir uWSGI && \
    mkdir -p /project/dl_api/logs && \
    mkdir -p /project/dl_api/images && \
    rm -rf /tmp/*

# 暂时没有找到问题所在
# CMD ["uwsgi", "/project/dl_api/robo_dl_api/wsgi/uwsgi.ini"]
CMD python3 manage.py runserver 0.0.0.0:8001