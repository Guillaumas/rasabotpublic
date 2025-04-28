FROM rasa/rasa-sdk:3.6.2

WORKDIR /app/actions

COPY . /app/actions

USER root

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "-m"]
CMD ["rasa_sdk", "--actions", "actions", "--port", "5055"]