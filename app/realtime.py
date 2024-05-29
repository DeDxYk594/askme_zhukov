import httpx


def notify_room(room_id):
    url = "http://localhost:8008/api"
    data = {
        "method": "publish",
        "params": {"channel": f"room:{room_id}", "data": {"message": "234"}},
    }
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "o6ss4Gl74eVM_c0U2jgeMDN8h9RKkXmZTC1u6MMRGC0",
    }
    response = httpx.post(url, json=data, headers=headers)
    response.raise_for_status()
