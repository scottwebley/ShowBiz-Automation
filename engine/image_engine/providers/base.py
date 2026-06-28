"""
===========================================
ShowBiz Image Engine
providers/base.py
Version 2.0
===========================================

Base classes used by every image provider.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ImageResult:
    """
    Represents a single candidate image.
    """

    title: str
    image_url: str
    page_url: str

    width: int = 0
    height: int = 0

    source: str = ""
    license: str = ""

    score: float = 0.0


class ImageProvider:
    """
    Base class for all providers.
    """

    provider_name = "Unknown"

    def search(self, query: str) -> List[ImageResult]:
        raise NotImplementedError(
            f"{self.provider_name} must implement search()."
        )