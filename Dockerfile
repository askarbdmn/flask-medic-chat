# Gunakan base image Python
FROM python:3.9

# Set direktori kerja di dalam container
WORKDIR /app

# Salin semua file ke container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Jalankan aplikasi Flask
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
