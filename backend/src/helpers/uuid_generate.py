import uuid


def generate_uuid() -> str:
    id = str(uuid.uuid4())
    return id
