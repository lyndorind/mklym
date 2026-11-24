from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from repository_lab.database import get_session
from repository_lab.models import Item
from repository_lab.schemas import ItemCreate, ItemRead

router = APIRouter(prefix="/items", tags=["items"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, session: SessionDep) -> Item:
    item = Item(**payload.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("", response_model=list[ItemRead])
def list_items(session: SessionDep) -> list[Item]:
    return list(session.scalars(select(Item).order_by(Item.id)))


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, session: SessionDep) -> Item:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, session: SessionDep) -> None:
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
