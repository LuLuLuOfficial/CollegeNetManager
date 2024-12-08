def PathCheck(Path: str):
    from pathlib import Path as _Path
    Path = _Path(Path)
    if Path.exists():
        return True
    else:
        return False
