from fastapi import APIRouter
from ..db import cur


router = APIRouter(
    prefix="/users",
    tags=["users"]
    )



@router.get('/')
def get_users():
    """Return a list of items in the database"""
    cur.execute('SELECT * FROM users;')
    
    users = cur.fetchall()

    return users

@router.post('/')
def create_user():
    return

@router.put('/{user_id}')
def update_user():
    return

@router.delete('/{user_id}')
def delete_user():
    return
