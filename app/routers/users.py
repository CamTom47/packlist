from fastapi import APIRouter
from ..db import cur
from pydantic import BaseModel

class User(BaseModel):
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    password: str | None = None


router = APIRouter(
    prefix="/users",
        tags=["users"]
    )



@router.get('/')
def find_all_users():
    """Return a list of items in the database"""
    cur.execute('SELECT id, first_name, last_name, username FROM users;')
    
    users = cur.fetchall()

    return users

@router.get('/{user_id}')
def find_a_user(user_id):
    """Return a list of items in the database"""
    cur.execute("""SELECT
                        id,
                        first_name,
                        last_name,
                        username 
                    FROM 
                        users
                    WHERE id = %s;""", user_id)
    
    user = cur.fetchone()

    return user

@router.put('/{user_id}')
def update_user(user_id, data: User):
    """ Update an existing user """
    first_name, last_name, username, password = data['firstName'], data['lastName'], data['username'], data['password']
    
    
    # DO SOMETHING SEPARATE FOR PW UPDATE
    
    cur.execute("""
                    UPDATE users
                    SET first_name = %s,
                        last_name = %s,
                        username = %s,
                        password = %s)
                    WHERE id = %s
                    RETRUNING first_name AS "firstName", last_name AS "lastName", username
                    """, (first_name, last_name, username, user_id))
    
    updated_user = cur.fetchone()
    return updated_user

@router.delete('/{user_id}')
def delete_user(user_id):
    cur.execute( 'DELETE FROM users WHERE id = %s', user_id)        
    
    return {"message": 'user successfully deleted'}
