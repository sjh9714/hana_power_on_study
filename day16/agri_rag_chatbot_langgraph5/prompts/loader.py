from pathlib import Path


def promprt_loader(name: str) -> str:
    """Load a prompt text file from the prompts/ directory.

    Example: promprt_loader('router_prompt') -> reads prompts/router_prompt.txt
    """
    return Path(f"prompts/{name}.txt").read_text(encoding="utf-8")
