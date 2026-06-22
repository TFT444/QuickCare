import hashlib
import logging
import re

logger = logging.getLogger(__name__)

DISCLAIMER_EN = (
    "This information is for guidance only. "
    "Always consult your pharmacist or GP for medical advice."
)

DISCLAIMERS: dict[str, str] = {
    "en": DISCLAIMER_EN,
    "ur": "یہ معلومات صرف رہنمائی کے لیے ہے۔ ہمیشہ اپنے فارماسسٹ یا جی پی سے طبی مشورہ لیں۔",
    "bn": "এই তথ্য শুধুমাত্র নির্দেশিকার জন্য। সর্বদা আপনার ফার্মাসিস্ট বা জিপির সাথে পরামর্শ করুন।",
    "so": "Macluumaadkan waxay u tahay hanuunin keliya. Had iyo jeer la tasho farmashiistaha ama dhakhtarkaaga.",
    "pl": "Te informacje mają charakter wyłącznie informacyjny. Zawsze konsultuj się z farmaceutą lub lekarzem.",
    "ar": "هذه المعلومات للإرشاد فقط. استشر دائمًا الصيدلاني أو الطبيب للحصول على المشورة الطبية.",
    "pa": "ਇਹ ਜਾਣਕਾਰੀ ਸਿਰਫ਼ ਮਾਰਗਦਰਸ਼ਨ ਲਈ ਹੈ। ਹਮੇਸ਼ਾ ਆਪਣੇ ਫਾਰਮਾਸਿਸਟ ਜਾਂ ਜੀਪੀ ਤੋਂ ਡਾਕਟਰੀ ਸਲਾਹ ਲਓ।",
    "ta": "இந்தத் தகவல் வழிகாட்டுதலுக்காக மட்டுமே. எப்போதும் உங்கள் மருந்தாளர் அல்லது மருத்துவரிடம் ஆலோசிக்கவும்.",
    "ro": "Aceste informații sunt doar orientative. Consultați întotdeauna farmacistul sau medicul de familie.",
    "gu": "આ માહિતી ફક્ત માર્ગદર્શન માટે છે. હંમેશા તમારા ફાર્માસિસ્ટ અથવા જીપીની સલાહ લો.",
}

DIAGNOSTIC_PATTERNS = [
    r"\byou have\b",
    r"\byou are diagnosed\b",
    r"\bdiagnosis is\b",
    r"\byou should (increase|decrease|stop|change) (your )?(dose|dosage|medication)\b",
]


def validate_output(text: str) -> tuple[bool, str]:
    text_lower = text.lower()
    for pattern in DIAGNOSTIC_PATTERNS:
        if re.search(pattern, text_lower):
            logger.warning("Safety violation detected: pattern '%s'", pattern)
            return False, f"Output blocked: contains disallowed clinical claim (pattern: {pattern})"
    return True, ""


def append_disclaimer(text: str, language: str) -> str:
    disclaimer = DISCLAIMERS.get(language, DISCLAIMER_EN)
    audit_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
    logger.info("AI output audit hash: %s language: %s", audit_hash, language)
    return f"{text}\n\n---\n{disclaimer}"


def safe_output(text: str, language: str) -> str:
    ok, reason = validate_output(text)
    if not ok:
        logger.error("Blocked unsafe output: %s", reason)
        return append_disclaimer(
            "I'm unable to provide that information. Please contact your GP or pharmacist directly.",
            language,
        )
    return append_disclaimer(text, language)
