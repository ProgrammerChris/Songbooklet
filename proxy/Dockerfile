FROM nginx:1.15.8

RUN rm /etc/nginx/conf.d/default.conf
COPY app.conf /etc/nginx/conf.d/

RUN mkdir -p /data/nginx/cache