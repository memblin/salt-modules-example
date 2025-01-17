
id_to_fqdn_test_data = [
    # Defaulted domain
    ("app-1", None, "app-1.example.com"),
    # Expected domain set that matches the default
    ("app-2", "example.com", "app-2.example.com"),
    # Expected domain set that does not match the default
    ("app-3", "example.net", "app-3.example.net"),
]
