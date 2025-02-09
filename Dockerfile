# Base image
FROM apache/airflow:2.6.2-python3.9


# Set working directory
WORKDIR /opt/airflow

# Copy Airflow DAGs and pipeline scripts
COPY airflow/dags/ dags/
COPY src/ src/

# Copy dependencies
COPY requirements.txt .
# Set the PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/src"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint for Airflow
ENTRYPOINT ["airflow"]
