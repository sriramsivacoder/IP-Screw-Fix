ALL_QUESTIONS = [
    {
        "id": "intended_use",
        "text": "What is the intended use of this formulation?",
        "options": [
            {"value": "medicine", "label": "Medicine"},
            {"value": "food_nutraceutical", "label": "Food or Nutraceutical"},
            {"value": "cosmetic", "label": "Cosmetic"},
            {"value": "other", "label": "Other"},
            {"value": "not_sure", "label": "Not sure"},
        ],
        "show_if": None,
    },
    {
        "id": "classical_source",
        "text": (
            "Is this medicine based on an authoritative classical Ayurvedic text "
            "or formulary (such as the Ayurvedic Pharmacopoeia of India or "
            "Ayurvedic Formulary of India)?"
        ),
        "options": [
            {"value": "yes", "label": "Yes"},
            {"value": "no", "label": "No"},
            {"value": "not_sure", "label": "Not sure"},
        ],
        "show_if": {"field": "intended_use", "value": "medicine"},
    },
    {
        "id": "substantially_modified",
        "text": (
            "Has the formulation been substantially modified or is it a "
            "new formulation not found in classical Ayurvedic texts?"
        ),
        "options": [
            {"value": "yes", "label": "Yes"},
            {"value": "no", "label": "No"},
            {"value": "not_sure", "label": "Not sure"},
        ],
        "show_if": None,
    },
    {
        "id": "new_process",
        "text": "Is there a new or novel manufacturing process involved in producing this formulation?",
        "options": [
            {"value": "yes", "label": "Yes"},
            {"value": "no", "label": "No"},
            {"value": "not_sure", "label": "Not sure"},
        ],
        "show_if": None,
    },
    {
        "id": "geographical_association",
        "text": (
            "Does the product have a geographical association or a reputation "
            "linked to a specific region or geographical area?"
        ),
        "options": [
            {"value": "yes", "label": "Yes"},
            {"value": "no", "label": "No"},
            {"value": "not_sure", "label": "Not sure"},
        ],
        "show_if": None,
    },
    {
        "id": "biological_resources_from_india",
        "text": "Were the biological resources used in this formulation obtained from India?",
        "options": [
            {"value": "yes", "label": "Yes"},
            {"value": "no", "label": "No"},
            {"value": "not_sure", "label": "Not sure"},
        ],
        "show_if": None,
    },
]


def get_active_questions(answers: dict) -> list:
    active = []
    for question in ALL_QUESTIONS:
        condition = question["show_if"]
        if condition is None:
            active.append(question)
        else:
            field_value = answers.get(condition["field"])
            if field_value == condition["value"]:
                active.append(question)
    return active
