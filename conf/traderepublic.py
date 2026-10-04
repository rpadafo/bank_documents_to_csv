import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


def process(source_path, output_path, file_name):
    """Copy a Trade Republic CSV unchanged, adding the configured prefix."""
    base_name = os.path.splitext(file_name)[0]
    prefix = os.environ.get("PREFIX_TRADEREPUBLIC", "TR")
    csv_path = os.path.join(output_path, f"{prefix}_{base_name}.csv")

    with open(source_path, 'rb') as source_file:
        content = source_file.read()

    with open(csv_path, 'wb') as destination_file:
        destination_file.write(content)

    logger.info(f"[Trade Republic] CSV copied unchanged to: {csv_path}")