'''Unit and integration tests for Database Layer, Configuration, Connection Pooling, and Health endpoints'''

import pytest
from unittest.mock import MagicMock
from config import Settings, get_settings
from database import Database, get_db
from repository.base_repo import BaseRepository
from repository.indexes import init_db_indexes

def test_settings_loading_and_defaults():
    '''Test application settings loaded with correct types and defaults (NFR-009)'''
    settings = get_settings()
    assert settings.APP_NAME == "ProjecTrack"
    assert isinstance(settings.MIN_POOL_SIZE, int)
    assert isinstance(settings.MAX_POOL_SIZE, int)
    assert settings.MIN_POOL_SIZE <= settings.MAX_POOL_SIZE
    assert isinstance(settings.SERVER_SELECTION_TIMEOUT_MS, int)
    assert settings.MONGO_DB_NAME is not None

def test_database_singleton_instance():
    '''Test Database class maintains a singleton instance and provides get_db()'''
    db1 = Database()
    db2 = Database()
    assert db1 is db2
    assert get_db() is not None

def test_database_ping_format():
    '''Test Database.ping() returns expected structured health dict (NFR-005)'''
    ping_res = Database.ping()
    assert isinstance(ping_res, dict)
    assert "status" in ping_res
    assert "database" in ping_res
    assert "latency_ms" in ping_res
    if ping_res["status"] == "healthy":
        assert isinstance(ping_res["latency_ms"], (int, float))

def test_init_db_indexes():
    '''Test declarative index creation across domain collections (NFR-005, NFR-006)'''
    db = get_db()
    res = init_db_indexes(db)
    assert isinstance(res, dict)
    assert res["status"] in ("success", "partial_error", "skipped")

def test_base_repository_crud_logic_with_mock():
    '''Test BaseRepository add, get, exists, update, count, and get_all pagination logic'''
    class MockCursor:
        def __init__(self, data):
            self.data = list(data)
            self._skip = 0
            self._limit = len(self.data)

        def skip(self, n):
            self._skip = n
            return self

        def limit(self, n):
            self._limit = n
            return self

        def __iter__(self):
            return iter(self.data[self._skip : self._skip + self._limit])

    class MockCollection:
        def __init__(self):
            self.docs = {}

        def insert_one(self, doc):
            self.docs[doc["_id"]] = doc.copy()
            return MagicMock(inserted_id=doc["_id"])

        def find_one(self, filter_dict, projection=None):
            doc = self.docs.get(filter_dict.get("_id"))
            if doc is None:
                return None
            if projection and list(projection.keys()) == ["_id"]:
                return {"_id": doc["_id"]}
            return doc.copy()

        def update_one(self, filter_dict, update_dict):
            target_id = filter_dict.get("_id")
            if target_id in self.docs:
                self.docs[target_id].update(update_dict.get("$set", {}))
                return MagicMock(modified_count=1)
            return MagicMock(modified_count=0)

        def delete_one(self, filter_dict):
            target_id = filter_dict.get("_id")
            if target_id in self.docs:
                del self.docs[target_id]
                return MagicMock(deleted_count=1)
            return MagicMock(deleted_count=0)

        def count_documents(self, filter_dict):
            if not filter_dict:
                return len(self.docs)
            return sum(1 for d in self.docs.values() if all(d.get(k) == v for k, v in filter_dict.items()))

        def find(self, filter_dict=None):
            if not filter_dict:
                items = list(self.docs.values())
            else:
                items = [d for d in self.docs.values() if all(d.get(k) == v for k, v in filter_dict.items())]
            return MockCursor(items)

    class DummyRepo(BaseRepository):
        def __init__(self):
            self.collection = MockCollection()

    repo = DummyRepo()

    # 1. Add item
    item1 = {"entity_id": 1001, "name": "Item One", "category": "A"}
    item2 = {"entity_id": 1002, "name": "Item Two", "category": "B"}
    repo.add(item1)
    repo.add(item2)

    # 2. Exists check (NFR-005)
    assert repo.exists(1001) is True
    assert repo.exists(9999) is False

    # 3. Get item
    fetched = repo.get(1001)
    assert fetched is not None
    assert fetched["_id"] == 1001
    assert fetched["name"] == "Item One"

    # 4. Count items
    assert repo.count() == 2
    assert repo.count({"category": "A"}) == 1

    # 5. Update item
    repo.update(1001, {"name": "Item One Updated"})
    updated = repo.get(1001)
    assert updated["name"] == "Item One Updated"

    # 6. Pagination check (NFR-006)
    all_items = list(repo.get_all(skip=0, limit=1))
    assert len(all_items) == 1

    # 7. Delete item
    repo.delete(1001)
    repo.delete(1002)
    assert repo.exists(1001) is False
    assert repo.count() == 0

@pytest.mark.asyncio
async def test_health_routes():
    '''Test health check router responses (NFR-005, NFR-009)'''
    from routes.health_router import health_check, database_health
    from fastapi import Response

    res1 = await health_check()
    assert res1["status"] == "healthy"
    assert "version" in res1

    resp = Response()
    res2 = await database_health(resp)
    assert "database" in res2
    assert "status" in res2["database"]
