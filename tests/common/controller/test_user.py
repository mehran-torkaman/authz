import pytest, json

@pytest.mark.parametrize(
    ("headers", "data", "status", "code"),
    [
        ({}, {}, 415, 101),
        ({"Content-Type": "application/json"}, {}, 400, 104)
    ]
)
def test_create_user(client, headers, data, status, code):
    result = client.post(
        "/api/v1/users",
        data = json.dumps(data),
        headers = headers
    )
    assert result.status_code == status
