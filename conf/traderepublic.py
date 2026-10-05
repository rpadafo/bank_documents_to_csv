import logging
import os
import csv
from decimal import Decimal

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


def process(source_path, output_path, file_name):
    """Add the calculated amount to a Trade Republic CSV."""
    base_name = os.path.splitext(file_name)[0]
    prefix = os.environ.get("PREFIX_TRADEREPUBLIC", "TR")
    csv_path = os.path.join(output_path, f"{prefix}_{base_name}.csv")

    with open(source_path, 'r', encoding='utf-8-sig', newline='') as source_file:
        reader = csv.reader(source_file)
        rows = list(reader)

    if not rows:
        raise ValueError("Trade Republic CSV is empty")

    header = rows[0]
    try:
        amount_index = header.index('amount')
        tax_index = header.index('tax')
    except ValueError as error:
        raise ValueError("Trade Republic CSV must contain 'amount' and 'tax' columns") from error

    header.append('amount_calc')
    for row in rows[1:]:
        amount = row[amount_index]
        tax = row[tax_index]
        if not amount:
            amount_calc = ''
        elif not tax:
            amount_calc = amount
        else:
            amount_calc = str(Decimal(amount) + Decimal(tax))
        row.append(amount_calc)

    with open(csv_path, 'w', encoding='utf-8', newline='') as destination_file:
        writer = csv.writer(destination_file)
        writer.writerows(rows)

    logger.info(f"[Trade Republic] CSV with calculated amount saved to: {csv_path}")