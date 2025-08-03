from typing import Dict, Any
from app.config.catalog import catalog_quries
from app.infra.database.postgres_db import PostgresManager
from app.core.interface.db_catalog_info import DBCatalogInfo
from sqlalchemy import text
from app.config.catalog import catalog_quries


class PostgreSQLCatalogRepository(DBCatalogInfo):
    
    #디비 접속 정보 입력 받기.
    def __init__(self):
        self.connection_manager = PostgresManager()
    
    
    #디비 카탈로그 정보 호출 - 데이터베이스 정보
    async def database_info(self) -> Dict[str, Any]:
        with self.connection_manager.engine.connect() as connection:
            
            database_info_json = {}
        
            ##데이터 베이스명 조회.
            database_info = connection.execute(text(catalog_quries['database_info'])).fetchone()
            
            ## json에 데이터베이스 정보 담기.
            database_info_json['database_name'] = database_info.database
            database_info_json['description'] = database_info.comment
            
        print(f"데이터베이스 호출 확인 => {database_info_json}")
        return database_info_json
    
    #디비 카탈로그 정보 호출 - 스키마 정보
    async def schema_info(self) -> Dict[str, Any]:
        
        with self.connection_manager.engine.connect() as connection:
            
            database_catalog_json = {}
            
            ##스키마 조회
            schema_info = connection.execute(text(catalog_quries['schema_info'])).fetchall()
            
            schemas = []
            for temp_schema in schema_info:
                
                if not temp_schema: return database_catalog_json
                
                ##스키마 명 넣기.
                schema_dict = {
                    'schema_name' : temp_schema.schema_name,
                    'description' : temp_schema.comment
                }
                
                schemas.append(schema_dict)
            
            database_catalog_json['schemas'] = schemas
            
        print(f"스키마 호출 확인 => {database_catalog_json}")
        return database_catalog_json
    
    #디비 카탈로그 정보 호출 - 테이블 정보
    async def table_info(self, schema_name: str) -> Dict[str, Any]:
        with self.connection_manager.engine.connect() as connection:
            
            database_catalog_json = {}
            
            ##테이블 정보
            table_info_list = []
        
            ##테이블 정보 조회.
            table_info = connection.execute(text(catalog_quries['table_info']), {'schema_name': schema_name}).fetchall()
            
            
            for temp_table in table_info:
                
                table_dict = {
                    'table_name' : temp_table.table_name,
                    'description' : temp_table.table_comment,
                    'table_type' : temp_table.table_type,
                }
                
                table_info_list.append(table_dict)
                    
            database_catalog_json['tables'] = table_info_list
        
        print(f"테이블 호출 확인 => {database_catalog_json}")
        return database_catalog_json
    
    #디비 카탈로그 정보 호출 - 컬럼 정보
    async def column_info(self, table_name: str) -> Dict[str, Any]:
        with self.connection_manager.engine.connect() as connection:
            
            database_catalog_json = {}
            
            ##컬럼 정보 담기
            column_info_list = []
            
            ##컬럼 정보 조회.
            column_info = connection.execute(text(catalog_quries['column_info']),{'table_name': table_name}).fetchall()
            
            for temp_column in column_info:
                
                column_dict = {
                    'column_name': temp_column.column_name,
                    'data_type' : temp_column.data_type,
                    'is_nullable' : temp_column.is_nullable,
                    'is_primary_key' : temp_column.is_primary_key,
                    'description' : temp_column.column_comment,
                    'column_default' : temp_column.column_default,
                    'character_maximum_length' : temp_column.character_maximum_length,
                    'numeric_precision' : temp_column.numeric_precision
                }
                
                column_info_list.append(column_dict)
                
            database_catalog_json['columns'] = column_info_list
        
        print(f"컬럼 호출 확인 => {database_catalog_json}")
        return database_catalog_json
    
    #디비 카탈로그 정보 호출 - fk 정보
    async def fk_info(self) -> Dict[str, Any]:
        with self.connection_manager.engine.connect() as connection:
            
            database_catalog_json = {}
            
            fk_info = connection.execute(text(catalog_quries['fk_info'])).fetchall()
            
            database_catalog_json['table_schema'] = fk_info.table_schema
            database_catalog_json['table_name'] = fk_info.table_name
            database_catalog_json['foreign_table_schema'] = fk_info.foreign_table_schema
            database_catalog_json['foreign_table_name'] = fk_info.foreign_table_name
            database_catalog_json['foreign_column_name'] = fk_info.foreign_column_name
        
        print("fk 호출 확인")
        return database_catalog_json
    
    #쿼리 유효성 검사 - 실행계획을 json으로 출력.
    async def sql_validation(self, sql: str) -> Dict[str, Any]:
        
        try: 
            with self.connection_manager.engine.connect() as connection:
                
                valid_info = connection.execute(text(f"EXPLAIN (FORMAT JSON) {sql}")).fetchone()
                
                print("유효성 호출 확인")
                return {
                    "is_valid" : True,
                    "execution_plan" : valid_info[0] if valid_info else None,
                    "error" : None
                }
        except Exception as e:
            return {
                "is_valid" : False,
                "error" : str(e)
            }
            
