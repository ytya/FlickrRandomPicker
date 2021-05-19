from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Config:
    # Flickr API Key
    api_key: str = ""
    api_secret: str = ""

    # wait time[sec] per api query (Flickr API Limit of 3600 queries per hour)
    wait_time: float = 1.2

    retry_error_num: int = 10

    # license names (https://www.flickr.com/creativecommons/)
    target_licenses: Tuple[str] = (
        "Attribution License",
        "United States Government Work",
        "Public Domain Dedication (CC0)",
        "Public Domain Mark",
    )

    # search options (https://www.flickr.com/services/api/flickr.photos.search.html)
    # don't set the following options (min_upload_date, max_upload_date)
    search_extras: Dict[str, str] = field(
        default_factory=lambda: {
            "content_type": "1",  # photos only
            "media": "photos",
            "dimension_search_mode": "min",
            "width": 2000,
            "height": 2000,
        }
    )
