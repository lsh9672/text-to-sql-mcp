import asyncio
import json
from typing import List, Dict, Optional
from contextlib import asynccontextmanager
from mcp.server.fastmcp import FastMCP
import os
from app.core.service.db_catalog_service import DbCatalogService
from app.di_container import DIContainer
from pathlib import Path
import sys
from starlette.requests import Request
from starlette.responses import PlainTextResponse, JSONResponse

# @asynccontextmanager
async def lifespan_manager():
    # 🚀 애플리케이션 시작 시 실행
    print("애플리케이션 시작 - 의존성 주입 설정")
    setup_dependencies()
    yield
    # 🔒 애플리케이션 종료 시 실행  
    print("애플리케이션 종료 - 리소스 정리")
    cleanup_resources()

def setup_dependencies():
    
    from app.infra.repository.postgres_catalog_repository_impl import PostgreSQLCatalogRepository
    from app.core.interface.db_catalog_info import DBCatalogInfo
    
    
    print("di 동작 테스트")
    DIContainer.register(DBCatalogInfo, PostgreSQLCatalogRepository())
    DIContainer.register(DbCatalogService, DbCatalogService())


setup_dependencies()
mcp = FastMCP(
    "text-to-sql-mcp", 
    host="0.0.0.0", 
    port=8001
    )

    
def cleanup_resources():
    ## TODO : 디비 정리등 리소스 정리를 만들어야 함.
    pass


# 간단한 헬스체크 엔드포인트
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> PlainTextResponse:
    """간단한 헬스체크 - HTTP 200 OK 반환"""
    return PlainTextResponse("OK")

## TODO : main에 모든 정보가 다 있는 것은 좋지 않을 듯, 툴과 리소스 별개의 파일로 만들어서 관리하는 것이 좋을 듯.
#툴 목록

#디비 카탈로그 정보 호출 - 데이터베이스 정보
@mcp.tool()
async def database_info() -> str:
    
    dbCatalogService = DIContainer.get(DbCatalogService)
    
    return json.dumps(
        await dbCatalogService.get_database_info(),
        ensure_ascii=False,
        indent=2
        )

#디비 카탈로그 정보 호출 - 스키마 정보
@mcp.tool()
async def schema_info() -> str:
    dbCatalogService = DIContainer.get(DbCatalogService)
    return json.dumps(
        await dbCatalogService.get_schema_info(),
        ensure_ascii=False,
        indent=2
        )

#디비 카탈로그 정보 호출 - 테이블 정보
@mcp.tool()
async def tables_info(schema_name: str) -> str:
    dbCatalogService = DIContainer.get(DbCatalogService)
    
    return json.dumps(
        await dbCatalogService.get_table_info(schema_name),
        ensure_ascii=False,
        indent=2
        )

#디비 카탈로그 정보 호출 - 컬럼 정보
@mcp.tool()
async def column_info(table_name: str) -> str:
    
    dbCatalogService = DIContainer.get(DbCatalogService)
    return json.dumps(
        await dbCatalogService.get_column_info(table_name),
        ensure_ascii=False,
        indent=2
        )

#디비 카탈로그 정보 호출 - fk 정보
@mcp.tool()
async def column_fk() -> str:

    dbCatalogService = DIContainer.get(DbCatalogService)
    return json.dumps(
        await dbCatalogService.get_fk_info(),
        ensure_ascii=False,
        indent=2
        )
    

#sql 검증 및 실행계획 반환
@mcp.tool()
async def sql_validation(sql: str) -> str:
    
    dbCatalogService = DIContainer.get(DbCatalogService)
    
    return json.dumps(
        await dbCatalogService.get_sql_validation(sql),
        ensure_ascii=False,
        indent=2
        )
    
def main():
    """서버 실행"""
    print("애플리케이션 시작 - 의존성 주입 설정")
    # setup_dependencies()
    print("🎯 MCP 서버 HTTP 모드로 실행 중... (포트: 8001)")
    # mcp.run(transport="http", port=8001)
    # mcp.run(transport="sse", port=8001)
    # mcp.run(transport="sse")
    mcp.run(transport="streamable-http", port=8000)
    
    
if __name__ == "__main__":
    main()