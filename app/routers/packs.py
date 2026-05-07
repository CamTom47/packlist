from fastapi import APIRouter

router = APIRouter(
    prefix='/packs',
    tags=['packs', 'packaroons']);

@router.get('/')
def find_all_packs():
    """Show all user packs"""
    return

@router.get('/{pack_id}')
def find_a_packs(id):
    """Shows the details of a user's pack"""
    return

@router.post('/')
def create_new_pack():
    """Create a new pack"""
    return

@router.put('/{pack_id}')
def edit_pack(id):
    """Edit the contents of a pack"""
    return

@router.delete('/{pack_id}')
def delete_pack(id):
    """Delete a user's pack"""
    return    