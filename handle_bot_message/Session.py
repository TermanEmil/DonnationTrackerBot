from dataclasses import dataclass
from datetime import datetime

import pytz


@dataclass
class Session:
    chat_id: int
    form_step: str

    language: str = None
    uploads: str = ""
    upload_date: str = None
    contact: str = None
    last_updated: str = datetime.now(tz=pytz.UTC).isoformat()
