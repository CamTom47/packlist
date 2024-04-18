
from flask import Flask, render_template, request, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Item, Pack, User, UserTrip, Trip, TripPack, PackItem
from forms import AddUserForm, LoginForm, AddTripForm, AddPackForm, EditPackForm, EditTripForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///packlist'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'secret secret'

app.debug = True
toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = 'curr_user'

connect_db(app)

def serialize_item(item):
    """Serialize an SQLAlchemy obj to dictionary"""

    return {
        "id": item.id,
        "name": item.name,
        "category": item.category,
        "essential": item.essential,
        "rain_precautionary": item.rain_precautionary,
        "cold_precautionary": item.cold_precautionary,
        "heat_precautionary": item.heat_precautionary,
        "emergency_precautionary": item.emergency_precautionary,
        "removable": item.removable
    }

@app.before_request
def add_user_to_g():
    """See if user is logged in, add current user to Flask global"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
         g.user = None

def do_login(user):
    """Log in a user"""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Log out a user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def homepage():
    """Render landing page content"""
    return render_template('homepage.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    """Register a user"""
    
    form = AddUserForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.register(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        do_login(user)



        return redirect('/')
    
    else:
        return render_template('create_user_form.html', form = form )

@app.route('/login', methods=['GET','POST'])
def login():
    """Render login form on GET request and Authenticate a user on POST request"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        print(session)
        do_login(user)

        return redirect('/')

    else: 
        return render_template('/login_form.html', form=form)

@app.route('/logout')
def logout():
    """Handle logout of user"""
    do_logout()
    return redirect('/')


#--------------------- Routing for trips ---------------------#
@app.route('/trips')
def show_trips():
    """Show all trips"""
    trips = Trip.query.all()

    return render_template('/trips/trips.html', trips = trips)


@app.route('/trips/new', methods=['GET','POST'])
def create_trip():
    """Creata a new trip"""

    form = AddTripForm()

    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        mileage = form.mileage.data
        notes = form.notes.data

        trip = Trip(
            
            name = name, 
            location = location,
            start_date = start_date,
            end_date = end_date,
            mileage = mileage,
            notes = notes
        )

        db.session.add(trip)
        db.session.commit()

        return redirect('/trips')

    return render_template('trips/create_trip_form.html', form=form)

@app.route('/trips/<int:id>')
def show_trip_details(id):
    """Show the details of a trip"""
    trip = Trip.query.get(id)
    
    trip_packs = TripPack.query.join(Trip, TripPack.trip_id == Trip.id).filter(TripPack.trip_id == trip.id).all()

    packs = Pack.query.all()

    return render_template('trips/trip_details.html', trip = trip, trip_packs=trip_packs, packs=packs)

@app.route('/trips/<int:id>/edit', methods=['GET','POST'])
def edit_trip(id):
    """Handle edit trip form"""

    trip = Trip.query.get_or_404(id)

    form = EditTripForm()

    if form.validate_on_submit():
        trip.name = form.name.data
        trip.location = form.location.data
        trip.start_date = form.start_date.data
        trip.end_date = form.end_date.data
        trip.mileage = form.mileage.data
        trip.notes = form.notes.data

        db.session.commit()

        return redirect(f'/trips/{id}')
    
    return render_template('trips/edit_trip_form.html', form=form, trip=trip)

@app.route('/trips/<int:id>/delete', methods=['POST'])
def delete_trip(id):
    """Delete trip"""
    trip = Trip.query.get(id)
    db.session.delete(trip)
    db.session.commit()

    return redirect('/trips')


# --------------------- Routing for packs  ---------------------#

@app.route('/packs')
def show_packs():
    """Show all user packs"""

    packs = Pack.query.all()
    
    return render_template('packs/packs.html', packs = packs)

@app.route('/packs/<int:id>')
def show_pack_details(id):
    """Shows the details of a user's pack"""
    pack = Pack.query.get_or_404(id)

    items = Item.query.join(PackItem, Item.id == PackItem.item_id).filter(PackItem.pack_id == pack.id)

    return render_template('packs/pack_details.html', pack=pack, items=items)


@app.route('/packs/new', methods =['GET','POST'])
def create_new_pack():
    form = AddPackForm()

    if form.validate_on_submit():
        name = form.name.data
        notes = form.notes.data

        pack = Pack(name=name,notes=notes)

        items = request.form.getlist('pack-items')

        db.session.add(pack)
        db.session.commit()

        for item in items:
            item = Item.query.filter(Item.name == item).first()

            pack_item = PackItem(pack_id = pack.id, item_id=item.id)

            db.session.add(pack_item)
            db.session.commit()


        return redirect(f'/packs/{pack.id}')
    
    return render_template('/packs/create_pack_form.html', form=form)

@app.route('/packs/<int:id>/edit', methods=['GET','POST'])
def edit_pack(id):
    """Edit the contents of a pack"""
    pack = Pack.query.get_or_404(id)
    existing_items = pack.items

    form = EditPackForm()
    
    if form.validate_on_submit():
        pack.name = form.name.data
        pack.notes = form.notes.data

        db.session.commit()

        new_items = request.form.getlist('pack-items')

        if existing_items:
            for existing_item in existing_items:
                """If an item was removed from the pack"""
                if existing_item not in new_items:
                    print(existing_item.id)

                    pack_item = PackItem.query.filter(PackItem.item_id == existing_item.id and PackItem.pack_id == pack.id).first()
                    db.session.delete(pack_item)
                    db.session.commit()

        if new_items:
            for new_item in new_items:
                """Add items that were not originally in the pack"""
                item = Item.query.filter(Item.name == new_item).first()

                pack_item = PackItem(pack_id = pack.id, item_id=item.id)

                db.session.add(pack_item)
                db.session.commit()

        return redirect(f'/packs/{pack.id}')
    
    
    return render_template('packs/edit_pack_form.html', form=form, pack = pack, items = existing_items)
    
@app.route('/packs/<int:id>/delete', methods=['POST'])
def delete_pack(id):
    """Delete a user's pack"""
    pack = Pack.query.get_or_404(id)

    db.session.delete(pack)
    db.session.commit()

    return redirect('/packs')

@app.route('/trips/<int:trip_id>/<int:pack_id>', methods=['POST'])
def add_pack_to_trip(trip_id,pack_id):
    """Add a pack to a trip"""

    trip_pack = TripPack(trip_id=trip_id, pack_id=pack_id)
    db.session.add(trip_pack)
    db.session.commit()

    return redirect(f'/trips/{trip_id}')


# -------------------- Routing for Items ------------------------#
@app.route('/items')
def get_items():
    items = Item.query.all()
    serialized = [serialize_item(item) for item in items]

    return jsonify(items = serialized)