CATEGORY_CLASSICAL_MEDICINE = "classical_medicine"
CATEGORY_PROPRIETARY_MEDICINE = "proprietary_or_modified_medicine"
CATEGORY_NEW_MEDICINE = "new_or_non_classical_medicine"
CATEGORY_FOOD_NUTRACEUTICAL = "food_nutraceutical"
CATEGORY_COSMETIC = "cosmetic"
CATEGORY_UNKNOWN = "unknown"

CONFIDENCE_HIGH = "high"
CONFIDENCE_MEDIUM = "medium"
CONFIDENCE_LOW = "low"


def determine_category(answers: dict) -> tuple[str, list[str]]:
    reasons = []
    intended_use = answers.get("intended_use")

    if intended_use == "food_nutraceutical":
        reasons.append("The intended use is food or nutraceutical.")
        return CATEGORY_FOOD_NUTRACEUTICAL, reasons

    if intended_use == "cosmetic":
        reasons.append("The intended use is cosmetic.")
        return CATEGORY_COSMETIC, reasons

    if intended_use == "other":
        reasons.append(
            "The intended use was described as other. "
            "Human review is required to determine the applicable regulatory and IPR category."
        )
        return CATEGORY_UNKNOWN, reasons

    if intended_use == "not_sure":
        reasons.append(
            "The intended use is unclear. "
            "Without knowing the intended use, it is not possible to identify a likely category."
        )
        return CATEGORY_UNKNOWN, reasons

    if intended_use == "medicine":
        classical_source = answers.get("classical_source", "not_sure")
        substantially_modified = answers.get("substantially_modified", "not_sure")

        if classical_source == "yes" and substantially_modified == "no":
            reasons.append(
                "The formulation is described as being based on an authoritative classical Ayurvedic source."
            )
            reasons.append("No substantial modification was reported.")
            return CATEGORY_CLASSICAL_MEDICINE, reasons

        if classical_source == "yes" and substantially_modified == "yes":
            reasons.append(
                "The formulation is based on a classical Ayurvedic source "
                "but has been substantially modified."
            )
            return CATEGORY_PROPRIETARY_MEDICINE, reasons

        if classical_source == "yes" and substantially_modified == "not_sure":
            reasons.append("The formulation is based on a classical Ayurvedic source.")
            reasons.append(
                "It is unclear whether the formulation has been substantially modified. "
                "This uncertainty affects the likely category."
            )
            return CATEGORY_PROPRIETARY_MEDICINE, reasons

        if classical_source == "no":
            reasons.append(
                "The formulation is not based on an authoritative classical Ayurvedic source."
            )
            if substantially_modified == "yes":
                reasons.append("The formulation has been substantially modified or is a new formulation.")
            return CATEGORY_NEW_MEDICINE, reasons

        if classical_source == "not_sure":
            reasons.append(
                "It is unclear whether the formulation is based on an authoritative classical Ayurvedic source."
            )
            if substantially_modified == "yes":
                reasons.append(
                    "The formulation has been substantially modified. "
                    "This suggests a new or non-classical formulation."
                )
                return CATEGORY_NEW_MEDICINE, reasons
            reasons.append(
                "There is insufficient information to confidently determine the likely category."
            )
            return CATEGORY_UNKNOWN, reasons

    reasons.append(
        "There is insufficient information to determine a likely formulation category."
    )
    return CATEGORY_UNKNOWN, reasons


def determine_confidence(answers: dict, category: str) -> str:
    if category == CATEGORY_UNKNOWN:
        return CONFIDENCE_LOW

    not_sure_count = sum(1 for v in answers.values() if v == "not_sure")

    if not_sure_count == 0:
        return CONFIDENCE_HIGH

    intended_use_uncertain = answers.get("intended_use") == "not_sure"
    classical_source_uncertain = answers.get("classical_source") == "not_sure"

    if intended_use_uncertain or classical_source_uncertain:
        return CONFIDENCE_LOW

    return CONFIDENCE_MEDIUM


def determine_human_review(answers: dict, category: str, confidence: str) -> bool:
    if category == CATEGORY_UNKNOWN:
        return True
    if confidence in (CONFIDENCE_LOW, CONFIDENCE_MEDIUM):
        return True
    if answers.get("intended_use") == "not_sure":
        return True
    if answers.get("new_process") == "not_sure":
        return True
    return False
