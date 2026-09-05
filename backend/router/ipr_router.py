CATEGORY_CLASSICAL_MEDICINE = "classical_medicine"
CATEGORY_PROPRIETARY_MEDICINE = "proprietary_or_modified_medicine"
CATEGORY_NEW_MEDICINE = "new_or_non_classical_medicine"
CATEGORY_FOOD_NUTRACEUTICAL = "food_nutraceutical"
CATEGORY_COSMETIC = "cosmetic"


def route_ipr(answers: dict, classification: dict) -> dict:
    routes = []
    category = classification.get("category", "unknown")
    intended_use = answers.get("intended_use")
    classical_source = answers.get("classical_source")
    new_process = answers.get("new_process")
    substantially_modified = answers.get("substantially_modified")
    geographical_association = answers.get("geographical_association")

    if new_process == "yes":
        routes.append({
            "ipr": "patent",
            "relevance": "potentially_relevant",
            "reason": (
                "A new or novel manufacturing process was reported. "
                "Novel processes may be eligible for patent protection if they meet applicable patentability requirements."
            ),
        })
    elif new_process == "not_sure":
        routes.append({
            "ipr": "patent",
            "relevance": "unclear",
            "reason": (
                "It is unclear whether a new manufacturing process is involved. "
                "If a novel process exists, patent protection may be potentially relevant."
            ),
        })
    elif substantially_modified == "yes":
        routes.append({
            "ipr": "patent",
            "relevance": "potentially_relevant",
            "reason": (
                "The formulation has been substantially modified. "
                "If the modification constitutes a novel technical invention, patent protection may be potentially relevant."
            ),
        })

    routes.append({
        "ipr": "trademark",
        "relevance": "potentially_relevant",
        "reason": (
            "Trademark protection is potentially relevant for the product name, "
            "brand name, logo, or other source-identifying marks associated with this formulation."
        ),
    })

    routes.append({
        "ipr": "design",
        "relevance": "potentially_relevant",
        "reason": (
            "Design protection may be potentially relevant for the distinctive "
            "visual appearance of the product or its packaging."
        ),
    })

    routes.append({
        "ipr": "copyright",
        "relevance": "potentially_relevant",
        "reason": (
            "Copyright protection is potentially relevant for original written content, "
            "labels, artwork, educational materials, or documentation associated with this formulation."
        ),
    })

    routes.append({
        "ipr": "trade_secret",
        "relevance": "potentially_relevant",
        "reason": (
            "Trade secret protection may be potentially relevant for confidential "
            "formulation know-how, proprietary manufacturing knowledge, or confidential process information."
        ),
    })

    if geographical_association == "yes":
        routes.append({
            "ipr": "geographical_indication",
            "relevance": "potentially_relevant",
            "reason": (
                "A geographical association or regional reputation was reported. "
                "Geographical Indication protection may be potentially relevant."
            ),
        })
    elif geographical_association == "not_sure":
        routes.append({
            "ipr": "geographical_indication",
            "relevance": "unclear",
            "reason": (
                "It is unclear whether the product has a geographical association. "
                "If a regional connection exists, Geographical Indication protection may be relevant."
            ),
        })

    if intended_use == "medicine" or category in (
        CATEGORY_CLASSICAL_MEDICINE,
        CATEGORY_PROPRIETARY_MEDICINE,
        CATEGORY_NEW_MEDICINE,
    ):
        routes.append({
            "ipr": "plant_variety_protection",
            "relevance": "potentially_relevant",
            "reason": (
                "If this formulation involves a new plant variety, "
                "Plant Variety Protection may be potentially relevant under applicable legislation."
            ),
        })

    if intended_use == "medicine":
        routes.append({
            "ipr": "traditional_knowledge",
            "relevance": "potentially_relevant",
            "reason": (
                "The formulation is intended as medicine and may relate to traditional Ayurvedic knowledge. "
                "Traditional Knowledge documentation is potentially relevant as prior art and for defensive purposes."
            ),
        })
    elif category in (CATEGORY_FOOD_NUTRACEUTICAL, CATEGORY_COSMETIC):
        routes.append({
            "ipr": "traditional_knowledge",
            "relevance": "potentially_relevant",
            "reason": (
                "The formulation may draw on traditional knowledge associated with Ayurvedic or "
                "traditional ingredients. Traditional Knowledge documentation may be relevant as prior art."
            ),
        })

    has_unclear = any(r["relevance"] == "unclear" for r in routes)
    needs_human_review = classification.get("needs_human_review", True) or has_unclear

    return {
        "routes": routes,
        "needs_human_review": needs_human_review,
    }
