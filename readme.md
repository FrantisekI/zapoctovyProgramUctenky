
erDiagram
    DATES {
        date date_purchased (date, add_price)
    }

    SHOPS {
        name name
    }

    "PRODUCT CLASSES" {
        int INT
        name name (custom, affordable, brand) 
    }

    "CUSTOM PRODUCT NAMES" {
        name name (feature, cost, wid, ceo)
    }

    DATES ||--o{ "PRODUCT CLASSES" : "refers to"
    SHOPS ||--o{ "PRODUCT CLASSES" : "refers to"
    "PRODUCT CLASSES" ||--o{ "CUSTOM PRODUCT NAMES" : "refers to"
    "BOUGHT ITEMS" }o--|| "PRODUCT CLASSES" : "belongs to"
    "BOUGHT ITEMS" }o--|| DATES : "belongs to"
    "BOUGHT ITEMS" }o--|| SHOPS : "belongs to"
