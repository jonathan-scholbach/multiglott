def slug_from_title(title: str) -> str:
    return "-".join(title.split()).lower()
