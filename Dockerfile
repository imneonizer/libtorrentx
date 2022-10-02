FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python setup.py install
ENTRYPOINT ["python", "-m", "libtorrentx"]