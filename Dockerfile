FROM python:3.11-slim

WORKDIR /mcp_server

# requirements 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY ./app /mcp_server/app

# 환경변수 설정
ENV PYTHONPATH=/mcp_server

# 포트 노출
EXPOSE 8000

CMD ["fastmcp", "run", "app/main.py", "--transport", "sse"]