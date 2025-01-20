FROM python:3.10-slim

# Sistem bağımlılıklarını yükleyin (OpenCV için gerekli olanlar ve numpy derleme için gerekli paketler)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libglib2.0-dev \
    libsm6 \
    libxrender1 \
    libxext6 \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgl1-mesa-glx \
    gcc \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Pip'i güncelleyin
RUN pip install --upgrade pip

# Google Cloud kimlik doğrulama dosyasını kopyalayın ve çevresel değişkeni ayarlayın

# Çalışma dizinini oluşturun ve kopyalayın
WORKDIR /app

# Gereksinim dosyasını kopyalayın ve bağımlılıkları yükleyin
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamanın kaynak kodunu kopyalayın
COPY . .

# Cloud Run'ın doğru portu dinlemesi için çevresel değişkeni ayarlayın
ENV PORT=8080

# Flask uygulamanızı başlatmak için gunicorn kullanın
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
