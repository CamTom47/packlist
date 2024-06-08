from app import create_app;
from models import connect_db;
from secret import POSTGRES_KEY

app = create_app(f"postgres://postgres.cqposqomiyvuhvesjgop:{POSTGRES_KEY}@aws-0-us-west-1.pooler.supabase.com:6543/postgres")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=6543 )

connect_db(app)