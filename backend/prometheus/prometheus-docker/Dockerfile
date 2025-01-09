   FROM alpine:latest


   RUN apk add --no-cache wget tar


   ENV PROMETHEUS_VERSION=2.41.0


   RUN wget https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz \
       && tar -xvf prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz \
       && mv prometheus-${PROMETHEUS_VERSION}.linux-amd64 /prometheus \
       && rm prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz

   
   WORKDIR /prometheus

   EXPOSE 9090

   # Run Prometheus\
   CMD ["./prometheus", "--config.file=/etc/prometheus/prometheus.yml"]