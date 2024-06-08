from app import create_app;
from models import connect_db;
from secret import POSTGRES_KEY

app = create_app(f"postgresql://postgres.cqposqomiyvuhvesjgop:{POSTGRES_KEY}@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
connect_db(app)