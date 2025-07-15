from pydantic import BaseModel
from typing import Optional, List

class Track(BaseModel):
    title: str
    artist: str
    url: str
    duration: int
    bpm: Optional[float] = None
    onsets: Optional[List[float]] = None 