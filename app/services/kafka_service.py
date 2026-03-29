from aiokafka import AIOKafkaProducer
from app.core.config import settings
import json
from decimal import Decimal

class KafkaService:
    def __init__(self):
        self.producer = None

    async def start(self):
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
            )
        await self.producer.start()

    async def stop(self):
        if self.producer:
            await self.producer.stop()

    async def publish(self, key: str, data: dict):
        value_json = json.dumps(
            data,
            default=lambda x: float(x) if isinstance(x, Decimal) else x
        ).encode("utf-8")

        await self.producer.send_and_wait(
            settings.TOPIC_NAME,
            key=key.encode("utf-8"),
            value=value_json
        )