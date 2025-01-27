FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR .
RUN pip install poetry==1.8.4
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
 && poetry install

# Creating folders, and files for a project:
COPY . .
EXPOSE 8081