import requests
import argparse
import json
import time
import random

USER_AGENTS = [
    "curl/7.88.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "sqlmap/1.5.1#stable",
    "Wget/1.20.3 (linux-gnu)",
    "python-requests/2.31.0"
]

QUERY_PARAMS = [
    "?debug=true",
    "?id=admin",
    "?token=XYZ123",
    "?probe=1",
    "?user=guest"
]

def simulate_fake_api_hit(endpoint_url, count):
    for i in range(count):
        ua = random.choice(USER_AGENTS)
        qp = random.choice(QUERY_PARAMS)
        full_url = endpoint_url + qp

        print(f"\n[>] Request {i+1}: {full_url}")
        print(f"[>] User-Agent: {ua}")

        try:
            response = requests.get(full_url, headers={"User-Agent": ua})
            print(f"[+] Status Code: {response.status_code}")
            print("[+] Response:")
            print(json.dumps(response.json(), indent=2))
        except Exception as e:
            print(f"[!] Failed: {e}")

        # Optional: simulate delay between requests
        time.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate attacker activity against fake API honeypot.")
    parser.add_argument('--url', required=True, help="URL of the deployed fake API Gateway endpoint")
    parser.add_argument('--count', type=int, default=5, help="Number of requests to simulate")

    args = parser.parse_args()
    simulate_fake_api_hit(args.url, args.count)
