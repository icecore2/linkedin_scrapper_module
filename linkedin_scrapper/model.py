import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BaseJobData:
    title: str
    company: str
    location: str
    job_link: str
    created_at: Optional[str] = None
    description: Optional[str] = None
    closing_date: Optional[str] = None
    category: Optional[str] = None
    remote: Optional[bool] = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())
