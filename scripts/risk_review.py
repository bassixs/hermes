from __future__ import annotations

import argparse
import json
from pathlib import Path


def review(text: str, methodic_path: str = "methodics/risk_review.md") -> dict:
    methodic_exists = Path(methodic_path).exists()
    warnings = []
    if not methodic_exists:
        warnings.append("methodic_file_missing")

    if not text.strip():
        return {
            "risk_level": "manual_review",
            "matched_criteria": ["empty_text"],
            "reasoning_summary": "Текст поста не извлечен, нужна ручная проверка по скриншоту.",
            "confidence": 0.2,
            "recommended_action": "manual_review",
            "warnings": warnings,
        }

    # Placeholder until the real methodic is provided. Keep conservative defaults.
    return {
        "risk_level": "manual_review",
        "matched_criteria": ["methodic_not_configured"],
        "reasoning_summary": "Реальная методичка еще не подключена, результат отправлен на ручную проверку.",
        "confidence": 0.3,
        "recommended_action": "manual_review",
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run risk triage for extracted post text.")
    parser.add_argument("--text-file")
    parser.add_argument("--text")
    parser.add_argument("--methodic", default="methodics/risk_review.md")
    args = parser.parse_args()

    text = args.text or ""
    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8")

    print(json.dumps(review(text, args.methodic), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

