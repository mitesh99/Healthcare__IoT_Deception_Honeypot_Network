#!/usr/bin/env python3
import os, json
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY","dev-secret")
socketio = SocketIO(app, cors_allowed_origins="*")
es = Elasticsearch([os.getenv("ELASTICSEARCH_HOST","http://localhost:9200")])
RANGE_MAP = {"1h":"now-1h","24h":"now-24h","7d":"now-7d","30d":"now-30d"}

@app.route("/")
def index(): return render_template("dashboard.html")

@app.route("/api/stats")
def get_stats():
    tr = RANGE_MAP.get(request.args.get("range","24h"),"now-24h")
    query = {
        "query":{"range":{"@timestamp":{"gte":tr}}},
        "aggs":{
            "total":{"value_count":{"field":"src_ip.keyword"}},
            "unique":{"cardinality":{"field":"src_ip.keyword"}},
            "attack_types":{"terms":{"field":"attack_type.keyword","size":10}},
            "timeline":{"date_histogram":{"field":"@timestamp","fixed_interval":"1h"}},
            "top_ips":{"terms":{"field":"src_ip.keyword","size":20}},
            "top_usernames":{"terms":{"field":"username.keyword","size":10}},
            "countries": {"cardinality": {"field": "geoip.country_name.keyword"}},
        },
        "size":0
    }
    try:
        r = es.search(index="honeypot-*",body=query); a = r["aggregations"]
        return jsonify({
            "total_attacks":a["total"]["value"],
            "unique_attackers":a["unique"]["value"],
            "attack_types":[{"name":b["key"],"count":b["doc_count"]} for b in a["attack_types"]["buckets"]],
            "timeline":[{"timestamp":b["key_as_string"],"count":b["doc_count"]} for b in a["timeline"]["buckets"]],
            "top_ips":[{"ip":b["key"],"count":b["doc_count"]} for b in a["top_ips"]["buckets"]],
            "top_usernames":[{"username":b["key"],"count":b["doc_count"]} for b in a["top_usernames"]["buckets"]],
            "countries": a["countries"]["value"],

        })
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route("/api/recent_attacks")
def get_recent_attacks():
    query = {"query":{"range":{"@timestamp":{"gte":"now-1h"}}},"sort":[{"@timestamp":{"order":"desc"}}],"_source":["src_ip","username","password","attack_type","geoip.country_name","@timestamp"],"size":50}
    try:
        r = es.search(index="honeypot-*",body=query)
        return jsonify([{"timestamp":s.get("@timestamp",""),"src_ip":s.get("src_ip","Unknown"),"country":s.get("geoip",{}).get("country_name","Unknown"),"username":s.get("username",""),"password":s.get("password",""),"attack_type":s.get("attack_type","unknown")} for hit in r["hits"]["hits"] for s in [hit["_source"]]])
    except Exception as e: return jsonify({"error":str(e)}),500

@app.route("/api/health")
def health(): return jsonify({"status":"healthy","timestamp":datetime.now().isoformat(),"elasticsearch":es.ping()})

@socketio.on("connect")
def on_connect(): emit("connected",{"data":"Connected!"})

if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port=5000,debug=True)
