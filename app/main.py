from fastapi import FastAPI, APIRouter
from routers.user import router as user_router
from app.routers import login
from routers.mail import router as mail_router
from app.routers import chatgpt
from starlette.middleware.cors import CORSMiddleware


router = APIRouter()
router.include_router(
    user_router,
    prefix='/users',
    tags=['users']
)

router.include_router(login.router)

router.include_router(
    mail_router,
    prefix='/mail',
    tags=['mail']
)

@router.get('/health')
async def health():
    return {'status': 'ok'}

router.include_router(chatgpt.router)

app = FastAPI()
app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type"]
)
