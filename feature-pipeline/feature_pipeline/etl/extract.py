import datetime
from json import JSONDecodeError
from pathlib import Path
from pandas.errors import EmptyDataError
from typing import Any, Dict, Tuple, Optional

import pandas as pd
import requests

from feature_pipeline import utils, settings

logger = utils.get_logger(__name__)

def _compute_extraction_window(export_end_reference_datetime: datetime.datetime, days_delay: int, days_export: int) -> Tuple[datetime.datetime, datetime.datetime]:
    """Compute the extraction window relative to 'export_end_reference_datetime' and take into consideration the maximum and minimum data points available in the dataset."""

    if export_reference_datetime is None:
        # As the dataset will expire in July 2023, we set the export end reference datetime to the last day of June 2023 + the delay.
        export_reference_datetime = datetime.datetime(
            2023, 6, 30, 0, 0
        ) + datetime.timedelta(days=days_delay)
        export_end_reference_datetime = export_end_reference_datetime.replace(
            minute=0, second=0, microsecond=0
        )

    else:
        export_end_reference_datetime = export_end_reference_datetime.replace(
            minute=0, second=0, microsecond=0
        )

    expiring_dataset_datetime = datetime.datetime(2023, 6, 30, 0, 0) + datetime.timedelta(
        days=days_delay
    )
    if export_end_reference_datetime > expiring_dataset_datetime:
        export_end_reference_datetime = expiring_dataset_datetime

        logger.warning(
            "We clapped 'export_end_reference_datetime' to 'datetime(2023, 6, 30) + datetime.timedelta(days=days_delay)' as \
        the dataset will not be updated starting from July 2023. The dataset will expire during 2023. \
        Check out the following link for more information: https://www.energidataservice.dk/tso-electricity/ConsumptionDE35Hour"
        )

        export_end = export_end_reference_datetime - datetime.timedelta(days=days_delay)
        export_start = export_end_reference_datetime - datetime.timedelta(
            days=days_delay + days_export
        )

        min_export_start = datetime.datetime(2020, 6, 30, 0, 0)
        if export_start < min_export_start:
            export_start = min_export_start
            export_end = export_start + datetime.timedelta(days=days_export)

            logger.warning(
                "We clapped 'export_start' to 'datetime(2020, 6, 30, 22, 0, 0)' and 'export_end' to 'export_start + datetime.timedelta(days=days_export)' as this is the latest window available in the dataset."
            )
        
        return export_start, export_end


def _extract_records_from_file_url(url: str, export_start: datetime.datetime, export_end: datetime.datetime, datetime_format: str, cache_dir: Optional[Path] = None) -> Optional[pd.DataFrame]:
    """Extract records from the file backup based on the given export window."""

    if cache_dir is None:
        cache_dir = settings.OUTPUT_DIR / "data"
        cache_dir.mkdir(parents=True, exist_ok=True)

    file_path = cache_dir / "ConsumptionDE35Hour.csv"
    if not file_path.exists():
        logger.info(f"Downloading data from: {url}")

        try:
            response = requests.get(url)
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"Response status = {response.status_code}. Could not dowload the file due to {e}"
            )
            return None
        
        if response.status_code != 200:
            raise ValueError(f"Response status = {response.status_code}. Could not dowload the file.")
        
        with file_path.open("w") as f:
            f.write(response.text)

        logger.info(f"Succesfully donloaded data to {file_path}")
    else:
        logger.info(f"Data already downloaded at {file_path}")
    
    try:
        data = pd.read_csv(file_path, delimiter=";")
    except EmptyDataError:
        file_path.unlink(missing_ok=True)

        raise ValueError(F"Downloaded file at {file_path} is empty. Could not load it into a DataFrame.")

    records = data[(data["HourUTC"] >= export_start.strftime(datetime_format)) & (data["HourUTC"] < export_end.strftime(datetime_format))]

    return records