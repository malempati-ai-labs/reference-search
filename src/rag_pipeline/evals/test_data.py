RETRIEVAL_TEST_DATA = [
    {
        "query": "We want to roll out ecommerce in many countries",
        "relevantCompanies": [
            "TECHNOLIT GmbH",
            "Quadient",
            "Xerox",
            "Nice S.p.A.",
            "TEKA Industrial SA",
        ]
    },
    {
        "query": "We have a very large product catalog",
        "relevantCompanies": [
            "SHOPcloud360",
            "VBH Holding",
            "Bürklin GmbH & Co. KG",
            "Soennecken eG"
        ]
    },
    {
        "query": "Our ordering process is still manual",
        "relevantCompanies": [
            "Environmental Solutions Group",
            "Lekkerland",
            "TEKA Industrial SA"
        ]
    },
    {
        "query": "We need better self-service capabilities for customers",
        "relevantCompanies": [
            "Environmental Solutions Group",
            "TEKA Industrial SA",
            "Lekkerland"
        ]
    },
    {
        "query": "We need to centralize multiple ecommerce systems",
        "relevantCompanies": [
            "Quadient",
            "Soennecken eG",
            "Block Group"
        ]
    },
    {
        "query": "We need a scalable B2B ecommerce platform",
        "relevantCompanies": [
            "VBH Holding",
            "KION North America",
            "SHOPcloud360",
            "Nice S.p.A."
        ]
    },
    {
        "query": "We need better product search and findability",
        "relevantCompanies": [
            "SHOPcloud360",
            "Rijk Zwaan",
            "Bürklin GmbH & Co. KG",
            "Fraisa"
        ]
    },
    {
        "query": "We want to improve customer experience across channels",
        "relevantCompanies": [
            "Bookspot",
            "Quadient",
            "Fraisa"
        ]
    },
    {
        "query": "We need ERP and CRM integration",
        "relevantCompanies": [
            "Nice S.p.A.",
            "Fraisa",
            "SHOPcloud360"
        ]
    },
    {
        "query": "We need a future-proof ecommerce architecture",
        "relevantCompanies": [
            "Fraisa",
            "VBH Holding",
            "Bürklin GmbH & Co. KG"
        ]
    },
    {
        "query": "We need to support multiple brands on one platform",
        "relevantCompanies": [
            "Nice S.p.A.",
            "Block Group",
            "Quadient"
        ]
    },
    {
        "query": "We want to digitize traditional sales processes",
        "relevantCompanies": [
            "VBH Holding",
            "Block Group",
            "desivero Srl"
        ]
    },
    {
        "query": "We need high scalability due to business growth",
        "relevantCompanies": [
            "KION North America",
            "SHOPcloud360",
            "Nice S.p.A."
        ]
    },
    {
        "query": "We need a unified customer experience globally",
        "relevantCompanies": [
            "Quadient",
            "Fraisa",
            "Rijk Zwaan"
        ]
    },
    {
        "query": "We need to integrate distributors and partners",
        "relevantCompanies": [
            "TECHNOLIT GmbH",
            "Soennecken eG"
        ]
    },
    {
        "query": "We need to reduce operational and maintenance costs",
        "relevantCompanies": [
            "Quadient",
            "Environmental Solutions Group",
            "Fraisa"
        ]
    },
    {
        "query": "We need better customer segmentation",
        "relevantCompanies": [
            "VBH Holding"
        ]
    },
    {
        "query": "We need centralized management of online stores",
        "relevantCompanies": [
            "Block Group",
            "SHOPcloud360",
            "Bookspot"
        ]
    },
    {
        "query": "We need ecommerce migration without downtime",
        "relevantCompanies": [
            "Dynapac Compaction Equipment AB",
            "KION North America"
        ]
    },
    {
        "query": "We need customer-specific pricing and personalization",
        "relevantCompanies": [
            "Würth Group",
            "VBH Holding"
        ]
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
