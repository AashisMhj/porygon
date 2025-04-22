```bash
kubectl apply -f config-map.yaml
kubectl
```

```bash
docker-compose up -d
```

## setup loki and grafana

```bash
# Create a Loki config file
cat <<EOF > loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  final_sleep: 0s
  chunk_idle_period: 5m
  max_chunk_age: 1h
  chunk_retain_period: 30s
  max_transfer_retries: 0

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/boltdb-cache
  filesystem:
    directory: /loki/chunks

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h

chunk_store_config:
  max_look_back_period: 0s

table_manager:
  retention_deletes_enabled: false
  retention_period: 0s
EOF
# Run Loki
docker run -d --name=loki -p 3100:3100 -v "$(pwd)/loki-config.yaml":/etc/loki/config.yaml grafana/loki:latest  -config.file=/etc/loki/config.yaml
# Run Grafana
docker run -d --name=grafana -p 3000:3000 --link=loki  grafana/grafana-oss:latest

# change permission for docker volumes
sudo chown -R 10001:10001 ./loki
sudo chown -R 472:472 ./grafana-data/
```
