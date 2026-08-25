'''Base repository class that provides common CRUD operations and pagination (NFR-005, NFR-009)'''

from abc import ABC
from typing import Optional, Union, Dict, Any, List
from pymongo.collection import Collection

# repository

class BaseRepository(ABC):
    '''Provides common CRUD operations with pagination and query helpers'''
    collection: Collection = None

    def add(self, entity: Union[dict, Any]):
        '''Adds an entity to the database'''
        if isinstance(entity, dict):
            entity_dict = entity.copy()
        elif hasattr(entity, "model_dump"):
            entity_dict = entity.model_dump()
        else:
            entity_dict = dict(entity)

        if 'entity_id' in entity_dict:
            entity_dict['_id'] = entity_dict.pop('entity_id')

        return self.collection.insert_one(entity_dict)

    def get(self, entity_id: int) -> Optional[Dict[str, Any]]:
        '''Gets an entity by its integer ID from the database'''
        return self.collection.find_one({"_id": entity_id})

    def exists(self, entity_id: int) -> bool:
        '''Performs a fast index-only check whether an entity ID exists (NFR-005)'''
        return self.collection.find_one({"_id": entity_id}, {"_id": 1}) is not None

    def update(self, entity_id: int, updates: dict):
        '''Updates an entity in the database'''
        clean_updates = {k: v for k, v in updates.items() if k not in ('_id', 'entity_id')}
        return self.collection.update_one({"_id": entity_id}, {"$set": clean_updates})

    def delete(self, entity_id: int):
        '''Deletes an entity from the database'''
        return self.collection.delete_one({"_id": entity_id})

    def count(self, filter_dict: Optional[dict] = None) -> int:
        '''Counts total documents matching the filter criteria'''
        query = filter_dict or {}
        return self.collection.count_documents(query)

    def get_all(self, skip: int = 0, limit: int = 100):
        '''Gets entities with pagination to avoid unbounded memory load (NFR-006)'''
        return self.collection.find().skip(max(0, skip)).limit(max(1, min(limit, 500)))

    def find_many(self, filter_dict: dict, skip: int = 0, limit: int = 100):
        '''Queries entities matching filter with pagination'''
        return self.collection.find(filter_dict).skip(max(0, skip)).limit(max(1, min(limit, 500)))
