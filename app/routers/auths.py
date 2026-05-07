from fastapi import APIRouter

router = APIRouter(
        prefix='/auth',
        tags=['auth']
)

@router.post('/register')
def signup():
    """Register a user"""
    
    return 

@router.post('/login')
def login():
    """Render login form on GET request and Authenticate a user on POST request"""
    
    return 