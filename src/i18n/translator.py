import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_TRANSLATIONS_DIR = Path(__file__).parent / "translations"
_cache: dict[str, dict] = {}


def _load(lang: str) -> dict:
    if lang not in _cache:
        path = _TRANSLATIONS_DIR / f"{lang}.json"
        if not path.exists():
            logger.warning("No translation file for '%s', falling back to 'en'", lang)
            path = _TRANSLATIONS_DIR / "en.json"
        with open(path, encoding="utf-8") as f:
            _cache[lang] = json.load(f)
    return _cache[lang]


def t(key: str, lang: str = "en", **kwargs) -> str:
    translations = _load(lang)
    template = translations.get(key) or _load("en").get(key, key)
    try:
        return template.format(**kwargs) if kwargs else template
    except KeyError:
        return template
