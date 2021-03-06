from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.users import Users
from repositories.district import DistrictRepository
from models.district import District
from .depends import get_district_repository, get_current_user

router = APIRouter()


@router.get("/get_all", response_model=List[District])
async def read_districts(
        district: DistrictRepository = Depends(get_district_repository),
        limit: int = 100,
        skip: int = 0
):
    return await district.get_all(limit=limit, skip=skip)


@router.get("/get_by_id", response_model=District)
async def read_district_by_id(
        id_district: int,
        district: DistrictRepository = Depends(get_district_repository)):
    return await district.get_by_id(id_district)


@router.get("/get_by_name", response_model=District)
async def read_district_by_name(
        district_name: str,
        district: DistrictRepository = Depends(get_district_repository)):
    return await district.get_by_name(district_name)


@router.post("/", response_model=District)
async def create_district(
        district_name: str,
        district: DistrictRepository = Depends(get_district_repository),
        current_user: Users = Depends(get_current_user)
):
    if not current_user.is_admin():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")
    return await district.create(district_name)


@router.delete("/", response_model=District)
async def delete_district(
        id_district: int,
        district: DistrictRepository = Depends(get_district_repository),
        current_user: Users = Depends(get_current_user)
):
    if not current_user.is_admin():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")
    return await district.delete(id_district)


@router.put("/", response_model=District)
async def update_district(
        id_district: int,
        district_name: str,
        district: DistrictRepository = Depends(get_district_repository),
        current_user: Users = Depends(get_current_user)
):
    if not current_user.is_admin():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access Denied")
    return await district.update(id_district, district_name)
