from typing import Tuple
from prompts.loader import promprt_loader

def get_prompt_text(name: str) -> str:
    return promprt_loader(name)

def split_system_human(raw: str) -> Tuple[str, str]:
    parts = raw.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return raw.strip(), ""

__all__ = ["get_prompt_text", "split_system_human"]
