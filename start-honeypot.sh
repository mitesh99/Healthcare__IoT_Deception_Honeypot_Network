#!/bin/bash
cd ~/healthcare-iot-honeypot

echo "Starting Healthcare IoT Honeypot..."

docker rm -f attack_dashboard 2>/dev/null
docker compose up -d

echo "Waiting 30 seconds for Logstash..."
sleep 30

LOGSTASH_IP=$(docker inspect logstash | grep '"IPAddress"' | grep '192' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -1)
echo "Logstash IP: $LOGSTASH_IP"

sudo tee /home/mitesh/healthcare-iot-honeypot/logging/filebeat/filebeat.yml > /dev/null << FBEOF
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/honeypot/cowrie/*.json
    json.keys_under_root: true
    json.overwrite_keys: true
    tags: ["cowrie"]

output.logstash:
  hosts: ["${LOGSTASH_IP}:5044"]
FBEOF

sudo chown root:root /home/mitesh/healthcare-iot-honeypot/logging/filebeat/filebeat.yml
sudo chmod go-w /home/mitesh/healthcare-iot-honeypot/logging/filebeat/filebeat.yml
docker compose restart filebeat

sleep 15
ES_IP=$(docker inspect elasticsearch | grep '"IPAddress"' | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | tail -1)
echo "Elasticsearch IP: $ES_IP"

docker rm -f attack_dashboard 2>/dev/null
docker run -d \
  --name attack_dashboard \
  --network healthcare-iot-honeypot_monitoring_net \
  -p 5000:5000 \
  -e ELASTICSEARCH_HOST=http://${ES_IP}:9200 \
  -e SECRET_KEY=change-me \
  -v /home/mitesh/healthcare-iot-honeypot/data/processed:/app/data/processed \
  healthcare-iot-honeypot-dashboard

echo ""
echo "All Done! Project is LIVE!"
echo "Dashboard : http://localhost:5000"
echo "Kibana    : http://localhost:5601"
echo "Grafana   : http://localhost:3000"
docker compose ps
