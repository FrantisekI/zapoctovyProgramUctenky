def assignByDatabase(sortedNamesJson, DatabaseObject):
    schema = {  # jen abych vedel, jak to vypada
        "type": "object",
        "required": ["items", "total", "store"],
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "total_price"],
                    "properties": {
                        "name": {"type": "string"},
                        "total_price": {"type": "string"},
                        "unit_price": {"type": ["string", "null"]}
                    }
                }
            },
            "total": {"type": ["string", "integer"]},
            "store": {"type": "string"}
        }
    }

    