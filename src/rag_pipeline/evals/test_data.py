RETRIEVAL_TEST_DATA = [
    {
        "query": "We have a very large product catalog",
        "relevantDocs": [
            "SHOPcloud360",
            "VBH Holding",
            "Bürklin GmbH & Co. KG",
            "Soennecken eG"
        ],
        "expectedPrimaryDoc": "SHOPcloud360",
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
    },
    {
        "query": "Our ordering process is too manual",
        "relevantDocs": [
            "Environmental Solutions Group",
            "Lekkerland",
            "TEKA Industrial SA"
        ],
        "expectedPrimaryDoc": "Environmental Solutions Group",
    },
    {
        "query": "We have fragmented systems across regions",
        "relevantDocs": [
            "Quadient",
            "Fraisa",
            "Rijk Zwaan"
        ],
        "expectedPrimaryDoc": "Quadient",
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
    }
]


RESPONSE_TEST_DATA = [
    {
        "query": "We have a very large product catalog",
        "groundTruthRelevantCustomerReference": [
            "SHOPcloud360",
            "VBH Holding",
            "Bürklin GmbH & Co. KG",
            "Soennecken eG"
        ],
        "expectedPrimaryGroundTruthCustomerReference": "SHOPcloud360",
        "prediction": []
    },
    {
        "query": "We want to sell in many countries",
        "groundTruthRelevantCustomerReference": [
            "Nice S.p.A.",
            "Quadient",
            "TECHNOLIT GmbH",
            "TEKA Industrial SA",
            "Xerox"
        ],
        "expectedPrimaryGroundTruthCustomerReference": "Nice S.p.A.",
        "prediction": []
    },
    {
        "query": "Our ordering process is too manual",
        "groundTruthRelevantCustomerReference": [
            "Environmental Solutions Group",
            "Lekkerland",
            "TEKA Industrial SA"
        ],
        "expectedPrimaryGroundTruthCustomerReference": "Environmental Solutions Group",
        "prediction": []
    },
    {
        "query": "We have fragmented systems across regions",
        "groundTruthRelevantCustomerReference": [
            "Quadient",
            "Fraisa",
            "Rijk Zwaan"
        ],
        "expectedPrimaryGroundTruthCustomerReference": "Quadient",
        "prediction": []
    },
    {
        "query": "We need better integration with ERP and CRM systems",
        "groundTruthRelevantCustomerReference": [
            "Nice S.p.A.",
            "Fraisa",
            "SHOPcloud360",
            "Würth Group"
        ],
        "expectedPrimaryGroundTruthCustomerReference": "Nice S.p.A.",
        "prediction": []
    }
]
