from fastapi import APIRouter, Request, BackgroundTasks
from app.services.auth_service import AuthService
from app.services.upbit_service import UpbitService
from app.services.kafka_service import KafkaService
router = APIRouter()
# 서비스 객체 생성 (실무에선 의존성 주입 도구를 쓰지만, 일단 직관적으로 작성)
kafka_svc = KafkaService()
upbit_svc = UpbitService(kafka_svc)


@router.get("/start-stream")
async def start_stream(
        codes: str,
        request: Request,
        background_tasks: BackgroundTasks
):
    # 1. 인증 서비스 호출: 쿠키에서 userId를 뽑아옴
    # staticmethod로 만들었으니 클래스에서 바로 호출 가능합니다.
    user_id = AuthService.get_user_id_from_cookie(request)

    # 2. 파라미터 준비 ("KRW-BTC,KRW-ETH" -> ["KRW-BTC", "KRW-ETH"])
    code_list = codes.split(",")

    # 3. 카프카 서비스 시작 (최초 1회)
    await kafka_svc.start()

    # 4. 백그라운드 태스크로 크롤러 실행
    # 사용자에겐 바로 응답을 주고, 서버 뒤에서 크롤링이 돕니다.
    background_tasks.add_task(upbit_svc.run_crawler, code_list, user_id)

    return {
        "status": "success",
        "user_id": user_id,
        "message": f"{code_list} 종목에 대한 실시간 수집을 시작합니다."
    }