from fastapi import APIRouter, HTTPException , status
from app.models.Rawr import Rawr
from sqlmodel import Session, select

router = APIRouter(prefix="/Rawr", tags=["Rawr"])
from ..database import engine

@router.get("/", summary="Get all Rawr")
async def get_all():
    with Session(engine) as session:
        statement = select(Rawr)
        results = session.exec(statement).all()
        return results



@router.post("/", summary="Create a new Rawr", status_code=status.HTTP_201_CREATED)
async def create_item(_Rawr : Rawr):
    with Session(engine) as session:
        session.add(_Rawr)
        session.commit()
        session.refresh(_Rawr)
        return _Rawr


@router.get("/{item_id}", summary="Get Rawr by ID")
async def get_item(item_id: int):
    with Session(engine) as session:
        item = session.get(Rawr, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rawr not found")
        return item



@router.put("/{item_id}", summary="Update Rawr")
async def update_item(_Rawr : Rawr , item_id: int):
    with Session(engine) as session:

        item = session.get(Rawr, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rawr not found")

        for key, value in _Rawr.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@router.delete("/{item_id}", summary="Delete Rawr" ,status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):

    with Session(engine) as session:
        item = session.get(Rawr, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Rawr not found")

        session.delete(item)
        session.commit()
        return None
