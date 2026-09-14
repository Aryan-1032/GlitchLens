TEST_DATA = {
    "product": {
        "name": "Apple Juice",
        "slug": "apple-juice",
        "category": "Juices",
    },

    "search": {
        "valid_query": "Apple",
        "no_results_query": "zzzx-no-match-92741",
    },

    "invalid_product": {
        "slug": "does-not-exist-92741",
    },

    "guest_checkout": {
        "email": "guest.test@example.com",
        "country": "India",
        "first_name": "Test",
        "last_name": "User",
        "street": "123 Test Street",
        "city": "Pune",
        "postal_code": "411001",
        "state": "Maharashtra",
    },

    "invalid_login": {
        "email": "invalid@example.com",
        "password": "invalid-password",
    },
}