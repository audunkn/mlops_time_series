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