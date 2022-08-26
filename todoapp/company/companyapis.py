from fastapi import APIRouter

router  = APIRouter()

@router.get("/")
async def get_company_name():
    return {"CompanyName" : "Example Company"}

@router.get("/employees")
async def get_employees():
    return 162