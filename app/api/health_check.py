from fastapi.routing import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {"Hello": "World"}
