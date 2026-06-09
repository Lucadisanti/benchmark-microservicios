from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

INSTANCE_NAME = os.getenv("INSTANCE_NAME", "api-local")

def get_connection():
    return mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="",
        database="benchmark_microservicios"
    )

@app.route("/")
def inicio():
    return "Microservicio funcionando"

@app.route("/api/benchmark", methods=["POST"])
def benchmark():
    try:
        data = request.get_json()

        test_id = data["test_id"]
        request_id = data["request_id"]
        value = data["value"]
        description = data["description"]
        sent_at = data["sent_at"]

        service_instance = INSTANCE_NAME

        conn = get_connection()
        cursor = conn.cursor()

        cursor.callproc("insert_benchmark_record", [
            test_id,
            request_id,
            value,
            description,
            sent_at,
            service_instance
        ])

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "status": "ok",
            "test_id": test_id,
            "request_id": request_id,
            "value": value,
            "description": description,
            "sent_at": sent_at,
            "service_instance": service_instance
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)