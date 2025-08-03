from app.core.interface.db_catalog_info import DBCatalogInfo
from app.di_container import DIContainer
from typing import Dict, Any
import json


class DbCatalogService:
    def __init__(self):
        self.db_catalog_repository = DIContainer.get(DBCatalogInfo)
    
    #데이터베이스 정보 조회.
    def get_database_info(self) -> Dict[str, Any]:
        return self.db_catalog_repository.database_info()
    
    #스키마 정보 조회
    def get_schema_info(self) -> Dict[str, Any]:
        return self.db_catalog_repository.schema_info()
    
    #테이블 정보 조회
    def get_table_info(self, schema_name: str) -> Dict[str, Any]:
        return self.db_catalog_repository.table_info(schema_name)
    
    #컬럼 정보 조회
    def get_column_info(self, table_name: str) -> Dict[str, Any]:
        return self.db_catalog_repository.column_info(table_name)
    
    #fk 정보 조회
    def get_fk_info(self) -> Dict[str, Any]:
        return self.db_catalog_repository.fk_info()
    
    #Sql 검증
    def get_sql_validation(self, sql: str) -> Dict[str, Any]:
        return self.db_catalog_repository.sql_validation(sql)