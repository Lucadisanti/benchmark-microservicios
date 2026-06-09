import asyncio
import aiohttp
import csv
import time
from datetime import datetime, timezone


URL = "http://localhost:8080/api/benchmark"

TOTAL_REQUESTS = 10000
CONCURRENCY = 5
RUN_ID = "011"

TEST_ID = f"benchmark-api4-{TOTAL_REQUESTS}-c{CONCURRENCY}-{RUN_ID}"
CSV_FILE = f"launcher/benchmark_results-{TEST_ID}.csv"


def now_iso():
    return datetime.now(timezone.utc).isoformat()


async def send_request(session, semaphore, i):
    async with semaphore:
        request_id = f"{RUN_ID}-REQ-{i:06d}"
        sent_at = now_iso()

        payload = {
            "test_id": TEST_ID,
            "request_id": request_id,
            "value": i,
            "description": "registro de prueba",
            "sent_at": sent_at
        }

        start = time.perf_counter()

        try:
            async with session.post(URL, json=payload) as response:
                try:
                    data = await response.json()
                except Exception:
                    data = {
                        "status": "error",
                        "error": "La respuesta no fue JSON válido"
                    }

                end = time.perf_counter()

                return {
                    "test_id": TEST_ID,
                    "request_id": request_id,
                    "value": i,
                    "description": "registro de prueba",
                    "sent_at": sent_at,
                    "received_at": now_iso(),
                    "client_elapsed_ms": round((end - start) * 1000, 2),
                    "status_code": response.status,
                    "status": data.get("status", "error"),
                    "service_instance": data.get("service_instance", ""),
                    "error": data.get("error", "")
                }

        except Exception as e:
            end = time.perf_counter()

            return {
                "test_id": TEST_ID,
                "request_id": request_id,
                "value": i,
                "description": "registro de prueba",
                "sent_at": sent_at,
                "received_at": now_iso(),
                "client_elapsed_ms": round((end - start) * 1000, 2),
                "status_code": 0,
                "status": "error",
                "service_instance": "",
                "error": str(e)
            }


async def main():
    inicio_total = time.perf_counter()

    semaphore = asyncio.Semaphore(CONCURRENCY)

    connector = aiohttp.TCPConnector(limit=CONCURRENCY)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [
            send_request(session, semaphore, i)
            for i in range(1, TOTAL_REQUESTS + 1)
        ]

        results = await asyncio.gather(*tasks)

    fin_total = time.perf_counter()
    duracion_total = round(fin_total - inicio_total, 2)

    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "test_id",
                "request_id",
                "value",
                "description",
                "sent_at",
                "received_at",
                "client_elapsed_ms",
                "status_code",
                "status",
                "service_instance",
                "error"
            ],
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(results)

    exitosos = [r for r in results if r["status_code"] == 200 and r["status"] == "ok"]
    errores = [r for r in results if r["status_code"] != 200 or r["status"] != "ok"]

    tiempos_ok = [r["client_elapsed_ms"] for r in exitosos]

    print("Benchmark finalizado.")
    print(f"Test ID: {TEST_ID}")
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Concurrencia: {CONCURRENCY}")
    print(f"Duracion total: {duracion_total} segundos")
    print(f"Requests exitosos: {len(exitosos)}")
    print(f"Requests con error: {len(errores)}")

    if tiempos_ok:
        print(f"Tiempo promedio por request: {round(sum(tiempos_ok) / len(tiempos_ok), 2)} ms")
        print(f"Tiempo minimo: {min(tiempos_ok)} ms")
        print(f"Tiempo maximo: {max(tiempos_ok)} ms")

    print(f"CSV generado: {CSV_FILE}")

    if errores:
        print("Primeros errores encontrados:")
        for error in errores[:5]:
            print(f"- {error['request_id']} | status_code={error['status_code']} | error={error['error']}")


if __name__ == "__main__":
    asyncio.run(main())