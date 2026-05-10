TEST_DATA = [
    {
        "query": "We have a very large product catalog",
        "relevantDocs": [
            "SHOPcloud360",
            "VBH Holding",
            "Bürklin GmbH & Co. KG",
            "Soennecken eG"
        ],
        "expectedPrimaryDoc": "SHOPcloud360",
        "reason": "Best representative for large-scale catalog management and high-volume product infrastructure."
    },
    {
        "query": "We want to sell in many countries",
        "relevantDocs": [
            "Nice S.p.A.",
            "Quadient",
            "TECHNOLIT GmbH",
            "TEKA Industrial SA",
            "Xerox"
        ],
        "expectedPrimaryDoc": "Nice S.p.A.",
        "reason": "Strongest reference for global multi-country commerce rollout and international digital scaling."
    },
    {
        "query": "Our ordering process is too manual",
        "relevantDocs": [
            "Environmental Solutions Group",
            "Lekkerland",
            "TEKA Industrial SA"
        ],
        "expectedPrimaryDoc": "Environmental Solutions Group",
        "reason": "Most explicit focus on self-service ordering automation and reducing manual order handling."
    },
    {
        "query": "We have fragmented systems across regions",
        "relevantDocs": [
            "Quadient",
            "Fraisa",
            "Rijk Zwaan"
        ],
        "expectedPrimaryDoc": "Quadient",
        "reason": "Best example of multi-country system fragmentation and consolidation into unified architecture."
    },
    {
        "query": "We need better integration with ERP and CRM systems",
        "relevantDocs": [
            "Nice S.p.A.",
            "Fraisa",
            "SHOPcloud360",
            "Würth Group"
        ],
        "expectedPrimaryDoc": "Nice S.p.A.",
        "reason": "Strongest ERP + CRM integration case with global Microsoft ecosystem alignment."
    }
]
