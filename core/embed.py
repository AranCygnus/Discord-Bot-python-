from __future__ import annotations

from typing import Optional, Union
from typing_extensions import Self

from discord import Colour
from discord import Embed as OriginEmbed



__all__ = (
    "Embed",
)

class Embed(OriginEmbed):
    def __init__(self, color: Optional[Union[int, Colour]] = 0xF8B500, **kwargs):
        super().__init__(color= color, **kwargs)
