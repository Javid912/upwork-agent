# fetcher_cli.py
import argparse
import json
from fetcher.playwright_fetcher import fetch_jobs_sync

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--pages", type=int, default=1)
    parser.add_argument("--auth", help="path to storage_state (auth.json)", default=None)
    parser.add_argument("--headful", action="store_true", help="run browser visible")
    parser.add_argument("--out", default="jobs.json")
    args = parser.parse_args()

    jobs = fetch_jobs_sync(args.query, pages=args.pages, storage_state=args.auth, headless=(not args.headful))
    print(f"fetched {len(jobs)} jobs")
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(jobs, f, default=str, ensure_ascii=False, indent=2)
    print("wrote", args.out)

if __name__ == "__main__":
    main()
