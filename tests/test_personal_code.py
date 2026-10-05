"""CR-1: personas koda pārbaude iesniegumā."""

import pytest


def _post(client, payload, personal_code):
    payload["personalCode"] = personal_code
    return client.post("/submissions", json=payload)


def _assert_personal_code_error(response, issue):
    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"] == [{"field": "personalCode", "issue": issue}]


@pytest.mark.parametrize(
    "personal_code, stored",
    [
        ("32000000001", "32000000001"),  # K1
        ("320000-00001", "32000000001"),  # K2
        (" 320000 00001 ", "32000000001"),  # K3
        ("010190-10001", "01019010001"),  # K8
        ("39999999999", "39999999999"),  # K12
        ("010105-20005", "01010520005"),  # K16: gadsimta cipars 2
    ],
)
def test_valid_personal_code_is_stored_normalized(
    client, valid_payload, personal_code, stored
):
    response = _post(client, valid_payload, personal_code)
    assert response.status_code == 201
    saved = client.get(f"/submissions/{response.json()['id']}").json()
    assert saved["personalCode"] == stored


@pytest.mark.parametrize(
    "personal_code",
    [
        "3200000000",  # K4: 10 cipari
        "320000000011",  # K5: 12 cipari
        "32OOOOOOOO1",  # K6: burts O
        "3200-0000001",  # K9: defise nav pēc 6. cipara
        "010190-10002",  # K10: nepareizs kontrolcipars
        "310290-10006",  # K11: neeksistējošs datums
        "30000000001",  # K13: vecais formāts, mēnesis 00
        "010105-30000",  # K17: nederīgs gadsimta cipars, kontrolcipars pareizs
        "   ",  # K14: tikai atstarpes
        "-",  # K14: tikai defise
    ],
)
def test_invalid_personal_code_returns_invalid_format(
    client, valid_payload, personal_code
):
    response = _post(client, valid_payload, personal_code)
    _assert_personal_code_error(response, "INVALID_FORMAT")


def test_empty_personal_code_returns_required(client, valid_payload):
    # K7: neaizpildīts
    response = _post(client, valid_payload, "")
    _assert_personal_code_error(response, "REQUIRED")


def test_missing_personal_code_returns_required(client, valid_payload):
    # K7: lauka nav
    del valid_payload["personalCode"]
    response = client.post("/submissions", json=valid_payload)
    _assert_personal_code_error(response, "REQUIRED")


def test_omd_receives_normalized_code(client, valid_payload, fake_omd):
    # K15
    response = _post(client, valid_payload, "320000-00001")
    assert response.status_code == 201
    assert fake_omd.calls == ["32000000001"]
    assert response.json()["replyChannel"] == "E_ADDRESS"
