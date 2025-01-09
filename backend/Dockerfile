FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
# gcc is needed bc some python modules apparently need to be compiled with C 
    gcc \  
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# just means fastapi runs on port 8000 (diff from prometheus on port 9090)
EXPOSE 8000

# this *actually* our fastapi service - each argument needs to be an array of strings where each string is an argument
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 