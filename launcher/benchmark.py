import asyncio
import aiohttp
import csv
import time
from datetime import datetime, timezone

URL = "http://localhost:8080/api/benchmark"

TOTAL_REQUESTS = 10000
CONCURRENCY = 10000
RUN_ID = "006"
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
                data = await response.json()
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
                    "status": data.get("status"),
                    "service_instance": data.get("service_instance"),
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
    semaphore = asyncio.Semaphore(CONCURRENCY)

    async with aiohttp.ClientSession() as session:
        tasks = [
            send_request(session, semaphore, i)
            for i in range(1, TOTAL_REQUESTS + 1)
        ]

        results = await asyncio.gather(*tasks)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
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
        ])

        writer.writeheader()
        writer.writerows(results)

    print(f"Benchmark finalizado.")
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Concurrencia: {CONCURRENCY}")
    print(f"CSV generado: {CSV_FILE}")


if __name__ == "__main__":
    asyncio.run(main())