# Example webhook payloads for different installation scenarios

# Location Level App Install (Whitelabeled Company)
whitelabeled_location_install = {
    "type": "INSTALL",
    "appId": "ve9EPM428h8vShlRW1KT",
    "locationId": "otg8dTQqGLh3Q6iQI55w",
    "companyId": "otg8dTQqGLh3Q6iQI55w",
    "userId": "otg8dTQqGLh3Q6iQI55w",
    "planId": "66a0419a0dffa47fb5f8b22f",
    "trial": {
        "onTrial": True,
        "trialDuration": 10,
        "trialStartDate": "2024-07-23T23:54:51.264Z"
    },
    "isWhitelabelCompany": True,
    "whitelabelDetails": {
        "domain": "example.com",
        "logoUrl": "https://example.com/logo.png"
    },
    "companyName": "Example Company"
}

# Location Level App Install (Non-Whitelabeled Company)
non_whitelabeled_location_install = {
    "type": "INSTALL",
    "appId": "ve9EPM428h8vShlRW1KT",
    "locationId": "otg8dTQqGLh3Q6iQI55w",
    "companyId": "otg8dTQqGLh3Q6iQI55w",
    "userId": "otg8dTQqGLh3Q6iQI55w",
    "planId": "66a0419a0dffa47fb5f8b22f",
    "trial": {
        "onTrial": True,
        "trialDuration": 10,
        "trialStartDate": "2024-07-23T23:54:51.264Z"
    },
    "isWhitelabelCompany": False,
    "whitelabelDetails": {},
    "companyName": "Example Company"
}

# Agency Level App Install
agency_install = {
    "type": "INSTALL",
    "appId": "ve9EPM428h8vShlRW1KT",
    "companyId": "otg8dTQqGLh3Q6iQI55w",
    "planId": "66a0419a0dffa47fb5f8b22f",
    "trial": {
        "onTrial": True,
        "trialDuration": 10,
        "trialStartDate": "2024-07-23T23:54:51.264Z"
    }
}