from abc import ABC, abstractmethod
## 타입 명시를 위해 import
from typing import Dict, Any

class DBCatalogInfo(ABC):
    
    #디비 카탈로그 정보 호출 - 데이터베이스 정보
    @abstractmethod
    async def database_info(self) -> Dict[str, Any]:
        pass
    
    #디비 카탈로그 정보 호출 - 스키마 정보
    @abstractmethod
    async def schema_info(self) -> Dict[str, Any]:
        pass
    
    #디비 카탈로그 정보 호출 - 테이블 정보
    @abstractmethod
    async def table_info(self, schema_name: str) -> Dict[str, Any]:
        pass
    
    #디비 카탈로그 정보 호출 - 컬럼 정보
    @abstractmethod
    async def column_info(self, table_name: str) -> Dict[str, Any]:
        pass
    
    #디비 카탈로그 정보 호출 - fk 정보
    @abstractmethod
    async def fk_info(self) -> Dict[str, Any]:
        pass
    
    #쿼리 유효성 검사
    @abstractmethod
    async def sql_validation(self, sql: str) -> Dict[str, Any]:
        pass
    