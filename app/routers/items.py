from fastapi import APIRouter
from app.models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"]
    )

def get_categories(items):
    """Return an Set of categories that the items belong to"""
    categories = set()
    for item in items:
        categories.add(item.category)
        
    return categories
    
@router.get('/')
def find_all_items():
    """Return a list of items in the database"""
    
    items = Item.query.filter((Item.created_by == 1) | (Item.created_by == g.user.id)).all()

    categories = get_categories(items)

    return {items, categories}

@router.get('/{item_id}')
def find_a_item(item_id):
    """Return a list of items in the database"""
    return

@router.post('/')
def create_new_item():
    
    new_item = {}
    
    return new_item

@router.put('/{item_id}')
def edit_item(item_id):
    """Render edit item content and handle form submission"""
    
    new_item = {}
    
    
    return new_item
    
@router.delete('/{item_id}')
def delete_item(item_id):
    """Deletes an item from the databse if was created by the user"""
    
    
    # item = Item.query.get(item_id)
    
    return {"message" : f"Item with the id of {item_id} was successfully deleted."}
