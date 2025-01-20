CREATE_TABLES = {
    "sale_order_line": """
        CREATE TABLE IF NOT EXISTS sale_order_line (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_on TEXT,                 
            sales_date TEXT,                 
            delivery_date TEXT,              
            order_reference TEXT NOT NULL,   
            sales_team TEXT,                 
            salesperson TEXT,                
            customer TEXT,                   
            state TEXT,                      
            sku TEXT NOT NULL,               
            product TEXT,                    
            collection TEXT,                
            product_template TEXT,           
            product_category TEXT,           
            fabric_sku TEXT,                
            fabric_type TEXT,                
            quantity INTEGER,                
            subtotal REAL,                   
            total_cost REAL,                 
            unit_cost REAL,                  
            unit_price REAL,                 
            order_status TEXT,               
            invoice_status TEXT,             
            delivery_status TEXT,            
            total_tax REAL,                  
            FOREIGN KEY (sku) REFERENCES master_sku (sku) -- Linking SKU to the master_sku table
        );

    """,
    "master_sku": """
        CREATE TABLE IF NOT EXISTS master_sku (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ws_ship_date TEXT,
            release_month TEXT,
            category_group TEXT,
            category TEXT,
            sub_category TEXT,
            collection TEXT,
            fabric_code TEXT,
            sku_parent TEXT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT,
            season TEXT,
            spsu25_status TEXT,
            sold_by_info TEXT,
            carded_non_carded TEXT,
            card_properties TEXT,
            properties TEXT,
            stones TEXT,
            color TEXT,
            cord_print_pattern TEXT,
            material TEXT,
            length TEXT,
            size TEXT,
            size_abbreviation TEXT,
            unit_cost REAL,
            ws_price REAL,
            ec_price REAL,
            weight_lbs REAL,
            upc TEXT,
            ws_sku BOOLEAN,
            ec_sku BOOLEAN,
            amazon_sku BOOLEAN,
            vendor TEXT,
            yards_per_unit REAL,
            labor_cost REAL,
            prefix TEXT,
            prepack_sku TEXT,
            available_sizes TEXT
        );
    """
}
