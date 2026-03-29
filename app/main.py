import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router import router
from app.services.kafka_service import KafkaService
from app.services.upbit_service import UpbitService

kafka_svc = KafkaService()
upbit_svc = UpbitService(kafka_service=kafka_svc)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await kafka_svc.start()

    asyncio.create_task(upbit_svc.run_crawler(["KRW-BTC", "KRW-ETH"]))
    yield

    await kafka_svc.stop()
app = FastAPI(lifespan=lifespan)

app.include_router(router)