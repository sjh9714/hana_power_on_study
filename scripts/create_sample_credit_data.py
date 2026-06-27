"""Create a small synthetic credit-card transaction sample.

The generated data is intentionally fake. It is meant for portfolio
documentation and lightweight notebook reproduction only.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROWS = [
    ("TX-0001", "CUST-001", "2026-01-03 09:12:00", 18400, "convenience_store", "Seoul", "false"),
    ("TX-0002", "CUST-002", "2026-01-03 12:45:00", 125000, "electronics", "Busan", "false"),
    ("TX-0003", "CUST-003", "2026-01-03 23:51:00", 890000, "travel", "Seoul", "true"),
    ("TX-0004", "CUST-001", "2026-01-04 08:05:00", 6200, "coffee", "Seoul", "false"),
    ("TX-0005", "CUST-004", "2026-01-04 19:22:00", 231000, "online_market", "Incheon", "false"),
    ("TX-0006", "CUST-002", "2026-01-05 01:18:00", 760000, "gaming", "Daegu", "true"),
    ("TX-0007", "CUST-005", "2026-01-05 14:07:00", 45000, "restaurant", "Gwangju", "false"),
    ("TX-0008", "CUST-003", "2026-01-06 10:31:00", 13200, "transport", "Seoul", "false"),
    ("TX-0009", "CUST-006", "2026-01-06 22:48:00", 510000, "luxury_goods", "Busan", "true"),
    ("TX-0010", "CUST-004", "2026-01-07 16:11:00", 98000, "grocery", "Incheon", "false"),
    ("TX-0011", "CUST-007", "2026-01-07 18:30:00", 21000, "pharmacy", "Daejeon", "false"),
    ("TX-0012", "CUST-005", "2026-01-08 02:05:00", 670000, "online_market", "Gwangju", "true"),
]


HEADER = [
    "transaction_id",
    "customer_id",
    "transaction_time",
    "amount",
    "merchant_category",
    "city",
    "is_fraud_candidate",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create synthetic credit-card transaction sample data.")
    parser.add_argument(
        "--output",
        default="sample_data/credit-card-transactions-sample.csv",
        help="Output CSV path. Defaults to sample_data/credit-card-transactions-sample.csv.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(HEADER)
        writer.writerows(ROWS)

    print(f"Wrote {len(ROWS)} synthetic rows to {output_path}")


if __name__ == "__main__":
    main()
