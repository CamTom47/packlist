from fastapi import APIRouter
from ..db import cur
from ..helpers.sql import serialize
from pydantic import BaseModel

class Pack(BaseModel):
    name: str
    owner: int
    notes: str
    
router = APIRouter(
    prefix='/packs',
    tags=['packs', 'packaroons']);

@router.get('/')
def find_all_packs():
    """Show all user packs"""

    query = """
            SELECT id, owner, name, notes
            FROM packs
            """
            
    cur.execute(query)
    packs = cur.fetchall()
    return packs

@router.get('/{pack_id}')
def find_a_packs(pack_id):
    """Shows the details of a user's pack"""

    query = """
            SELECT id, owner, name, notes
            FROM packs
            WHERE id = %s
            """
            
    cur.execute(query, pack_id)
    pack = cur.fetchone()
    return pack

@router.post('/')
def create_new_pack(data: Pack):
    """Create a new pack"""

    query = """
            INSERT INTO packs (owner, name, notes)
            VALUES (%s, %s, %s)
            """
            
    cur.execute(query, data["owner"], data["name"], data["notes"])
    new_pack = cur.fetchone()
    return new_pack

@router.put('/{pack_id}')
def edit_pack(pack_id, data):
    """Edit the contents of a pack"""

    data = data.model_dump()
    
    set_cols  = serialize(data)["set_cols"]
    raw_values = serialize(data)["raw_values"]
    
    query = f"""
            UPDATE packs
            SET
            {set_cols}
            WHERE id = %s
            RETURNING *
            """
    
    cur.execute(query, (*raw_values, pack_id))
    updated_pack = cur.fetchone()
    
    return updated_pack

@router.delete('/{pack_id}')
def delete_pack(pack_id):
    """Delete a user's pack"""

    query = """
            DELETE FROM packs WHERE id = %s
            """
            
    cur.execute(query, pack_id)
    
    return {"message", f"Pack {pack_id} was succesfully deleted"}