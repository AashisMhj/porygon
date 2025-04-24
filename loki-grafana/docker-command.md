## setup loki and grafana
```bash
sudo docker network create -d bridge loki-grafana

# Run Loki
sudo docker run -d --name=loki --network loki-grafana -p 3100:3100 -v "$(pwd)/loki-config.yaml":/etc/loki/config.yaml -v ./loki:/loki  grafana/loki:latest  -config.file=/etc/loki/config.yaml

# Run Grafana
sudo docker run -d --name=grafana --network loki-grafana -v ./grafana-data:/var/lib/grafana -p 3000:3000 --link=loki  grafana/grafana-oss:latest

# change permission for docker volumes
sudo chown -R 10001:10001 ./loki
sudo chown -R 472:472 ./grafana-data/
```
