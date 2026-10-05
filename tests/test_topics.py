"""CR-0: tēma PARKS un tēmu saraksts GET /topics."""

EXPECTED_TOPICS = [
    {"code": "ROADS", "name": "Ceļi un ielas"},
    {"code": "WASTE", "name": "Atkritumi"},
    {"code": "PLANNING", "name": "Teritorijas plānošana"},
    {"code": "PARKS", "name": "Parki un skvēri"},
    {"code": "OTHER", "name": "Cits"},
]


def test_list_topics(client):
    # K1, K4: precīzs saraksts, secība nemainās, OTHER beigās
    response = client.get("/topics")
    assert response.status_code == 200
    assert response.json() == EXPECTED_TOPICS


def test_create_submission_with_parks_topic(client, valid_payload):
    # K2
    valid_payload["topic"] = "PARKS"
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 201
    stored = client.get(f"/submissions/{response.json()['id']}").json()
    assert stored["topic"] == "PARKS"


def test_unknown_topic_returns_validation_error(client, valid_payload):
    # K3
    valid_payload["topic"] = "ZOO"
    response = client.post("/submissions", json=valid_payload)
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert any(d["field"] == "topic" for d in error["details"])
