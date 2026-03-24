#!/bin/bash
echo "Sending test attacks..."

# Bruteforce - China
for i in 1 2 3 4 5; do
  curl -s -X POST "http://localhost:9200/honeypot-$(date +%Y.%m.%d)/_doc" \
    -H 'Content-Type: application/json' \
    -d "{\"@timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\",\"eventid\":\"cowrie.login.failed\",\"attack_type\":\"bruteforce\",\"src_ip\":\"1.180.0.$i\",\"username\":\"admin\",\"password\":\"admin\",\"geoip\":{\"country_name\":\"China\",\"city_name\":\"Beijing\",\"location\":{\"lat\":39.9042,\"lon\":116.4074}}}"
  sleep 1
done

# Credential theft - Russia
curl -s -X POST "http://localhost:9200/honeypot-$(date +%Y.%m.%d)/_doc" \
  -H 'Content-Type: application/json' \
  -d "{\"@timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\",\"eventid\":\"cowrie.login.success\",\"attack_type\":\"credential_theft\",\"src_ip\":\"5.8.0.1\",\"username\":\"root\",\"password\":\"root\",\"geoip\":{\"country_name\":\"Russia\",\"city_name\":\"Moscow\",\"location\":{\"lat\":55.7558,\"lon\":37.6173}}}"

# Command injection - USA
curl -s -X POST "http://localhost:9200/honeypot-$(date +%Y.%m.%d)/_doc" \
  -H 'Content-Type: application/json' \
  -d "{\"@timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\",\"eventid\":\"cowrie.command.input\",\"attack_type\":\"command_injection\",\"src_ip\":\"8.8.0.1\",\"username\":\"root\",\"input\":\"whoami; cat /etc/passwd\",\"geoip\":{\"country_name\":\"United States\",\"city_name\":\"New York\",\"location\":{\"lat\":40.7128,\"lon\":-74.0060}}}"

# Malware delivery - India
curl -s -X POST "http://localhost:9200/honeypot-$(date +%Y.%m.%d)/_doc" \
  -H 'Content-Type: application/json' \
  -d "{\"@timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\",\"eventid\":\"cowrie.session.file_download\",\"attack_type\":\"malware_delivery\",\"src_ip\":\"103.21.0.1\",\"username\":\"admin\",\"geoip\":{\"country_name\":\"India\",\"city_name\":\"Mumbai\",\"location\":{\"lat\":19.0760,\"lon\":72.8777}}}"

# Bruteforce - Brazil
curl -s -X POST "http://localhost:9200/honeypot-$(date +%Y.%m.%d)/_doc" \
  -H 'Content-Type: application/json' \
  -d "{\"@timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%S.000Z)\",\"eventid\":\"cowrie.login.failed\",\"attack_type\":\"bruteforce\",\"src_ip\":\"177.0.0.1\",\"username\":\"nurse\",\"password\":\"nurse\",\"geoip\":{\"country_name\":\"Brazil\",\"city_name\":\"Sao Paulo\",\"location\":{\"lat\":-23.5505,\"lon\":-46.6333}}}"

echo "Done !"
