import asyncio
import json
import websockets

from app.core.config import settings
from app.models.ticker import UpbitTickerDTO

class UpbitService:
    def __init__(self, kafka_service):
        self.kafka_service = kafka_service  # 의존성 주입

    async def run_crawler(self, codes: list, user_id: str):
        while True:
            try:
                async with websockets.connect(settings.UPBIT_WS_URL) as ws:
                    # 구독 요청
                    subscribe_msg = [{"ticket": "unique-id"}, {"type": "ticker", "codes": codes}]
                    await ws.send(json.dumps(subscribe_msg))

                    async for message in ws:
                        raw_data = json.loads(message)
                        # DTO로 변환하여 데이터 검증
                        ticker = UpbitTickerDTO(user_id=user_id, **raw_data)
                        # 카프카로 발행
                        await self.kafka_service.publish(ticker.code, ticker.model_dump())
            except Exception as e:
                print(f"Error: {e}. Reconnecting...")
                await asyncio.sleep(5)