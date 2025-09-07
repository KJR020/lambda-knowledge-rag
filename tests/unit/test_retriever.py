from src.core.clients import KnowledgeClient


def test_knowledgeclient_find():
    # Pass a dummy s3_client to avoid reading AWS_REGION from environment
    class DummyS3:
        pass

    c = KnowledgeClient(s3_client=DummyS3())
    res = c.find("test")
    assert isinstance(res, dict)
    assert res.get("id") == "stub-1"
    assert "test" in res.get("text")
