import os 
from flask import Flask, render_template, request, redirect, session, g, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Item, Pack, User, UserTrip, Trip, TripPack, PackItem, TripStatus
from forms import AddUserForm, EditUserForm, LoginForm, AddTripForm, AddPackForm, EditPackForm, EditTripForm, AddItemForm, EditItemForm
from secret import G_API_KEY
from weather import get_weather_information, get_weather_highs_lows
from dashboard import count_trips_completed, count_upcoming_trips, average_trip_mileage, total_mileage_completed, total_days_backpacking
from sqlalchemy import exc, and_, or_


CURR_USER_KEY = 'curr_user'

def add_user_to_g():
        """See if user is logged in, add current user to Flask global"""

        if CURR_USER_KEY in session:
            g.user = User.query.get(session[CURR_USER_KEY])

        else:
            g.user = None
            
def create_app(database_name, testing=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "secret secrets"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    if testing:
        app.config["WTF_CSRF_ENABLED"] = False

    debug = DebugToolbarExtension(app)


    def get_categories(items):
        """Return an Set of categories that the items belong to"""
        categories = set()
        for item in items:
            categories.add(item.category)
            
        return categories

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
    def add_user():
        add_user_to_g()
            
            
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

    ###############################################################################################################
    #  User routes:

    @app.route('/signup', methods=['GET','POST'])
    def signup():
        """Register a user"""
        
        form = AddUserForm()
        
        if form.validate_on_submit():
            try:
            
                user = User.register(first_name = form.first_name.data,
                                last_name = form.last_name.data,
                                username = form.username.data,
                                password = form.password.data)
            
                db.session.add(user)
                db.session.commit()
            
            except exc.IntegrityError:
                flash("username already taken", "danger")
                return render_template('users/create_user_form.html', form = form )

            do_login(user)
            flash(f"Hello, {user.username}", "success")

            return redirect(f'/users/{user.id}/dashboard')
        
        return render_template('users/create_user_form.html', form = form )

    @app.route('/login', methods=['GET','POST'])
    def login():
        """Render login form on GET request and Authenticate a user on POST request"""
        form = LoginForm()

        if form.validate_on_submit():
            
            username = form.username.data
            password = form.password.data
            
            user = User.authenticate(username, password)
        
            if user:
                do_login(user)
                flash(f"Hello, {user.username}", "success")
                return redirect(f'/users/{user.id}/dashboard')
            
            else:
                flash("Invalid credentials, please try again.", "danger")
                return render_template('/login_form.html', form=form)

            

        return render_template('/login_form.html', form=form)

    @app.route('/logout')
    def logout():
        """Handle logout of user"""
        do_logout()
        return redirect('/')

    @app.route('/users/<int:id>')
    def show_user_information(id):
        """Show a user's account information"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        user = User.query.get_or_404(id)
        
        
        
        return render_template('/users/show_user_information.html', user=user)
        
    @app.route('/users/<int:id>/edit', methods=["GET","POST"])
    def handle_user_information(id):
        """Render user edit for and handle information upon valid submission"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        form = EditUserForm()
        
        if form.validate_on_submit():
            user = User.auth_update(first_name= form.first_name.data,
                                last_name = form.last_name.data,
                                username=form.username.data,
                                password=form.password.data)
            
            db.session.commit()
            return redirect(f'/')
            
        return render_template('users/edit_user_form.html', form = form)

    @app.route('/users/<int:id>/dashboard')
    def show_user_dashboard(id):
        """Show the details of a user"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        user = User.query.get(id)
        trips = user.trips
        packs = Pack.query.filter(Pack.owner == user.id).all()
        
        total_trips = count_trips_completed(trips)
        upcoming_trip_count = count_upcoming_trips(trips)
        avg_mileage = average_trip_mileage(trips)
        trip_mileage = total_mileage_completed(trips)
        days_backpacking = total_days_backpacking(trips)
        

        
        
        return render_template("/users/user_dashboard.html", user=user, trips=trips, packs=packs,
                                total_trips = total_trips,
                                upcoming_trip_count = upcoming_trip_count,
                                avg_mileage = avg_mileage,
                                trip_mileage = trip_mileage,
                                days_backpacking = days_backpacking)
        
    @app.route('/users/<int:id>/delete', methods=['POST'])
    def user_delete(id):
        """Delete a users account and content"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')    
        
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        
        return redirect('/login')
        
            


    ###############################################################################################################
    #  Trip routes:

    @app.route('/trips')
    def show_trips():
        """Show all trips"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        user = User.query.get(g.user.id)
        trips = user.trips

        return render_template('/trips/trips.html', trips = trips)


    @app.route('/trips/new', methods=['GET','POST'])
    def create_trip():
        """Creata a new trip"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')


        form = AddTripForm()

        if form.validate_on_submit():
            try:
                name = form.name.data
                location = request.form['location']
                start_date = form.start_date.data
                end_date = form.end_date.data
                mileage = form.mileage.data
                notes = form.notes.data
                lat = request.form['lat']
                lng = request.form['lng']
                trip_status = request.form['trip-status']
                
                

                status = TripStatus.query.filter(TripStatus.status == trip_status).first()
                
                
                
                trip = Trip(
                    name = name, 
                    location = location,
                    start_date = start_date,
                    end_date = end_date,
                    mileage = mileage,
                    notes = notes,
                    lat = lat,
                    lng = lng,
                    status = status.id
                )

                db.session.add(trip)
                db.session.commit()
            
                user_trip = UserTrip(user_id = g.user.id, trip_id=trip.id)
                db.session.add(user_trip)
                db.session.commit()
                
            except KeyError:
                flash('Please select a valid location', 'danger')
                return redirect('/trips/new')

                

            return redirect('/trips')

        return render_template('trips/create_trip_form.html', form=form)

    @app.route('/trips/<int:id>')
    def show_trip_details(id):
        """Show the details of a trip"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        
        user = User.query.get(g.user.id)
        trip = Trip.query.get(id)
        trips = user.trips

        
        if trip.users[0].id != g.user.id:
            flash("You do not have permissions to view this trip")
            return redirect('/trips')
        
        key = G_API_KEY
        
        trip_packs = TripPack.query.join(Trip, TripPack.trip_id == Trip.id).filter(TripPack.trip_id == trip.id).all()

        packs = Pack.query.filter(Pack.owner == g.user.id).all()
        
        daily_weather = get_weather_information(trip.lat, trip.lng)
        
        return render_template('trips/trip_details.html', trips=trips, trip = trip, trip_packs=trip_packs, packs=packs, key=key, daily_weather=daily_weather)

    @app.route('/trips/<int:id>/edit', methods=['GET','POST'])
    def edit_trip(id):
        """Handle edit trip form"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')

        trip = Trip.query.get_or_404(id)
        
        if trip.users[0].id != g.user.id:
            flash("You do not have permissions to edit this trip")
            return redirect('/trips')

        form = EditTripForm()

        if form.validate_on_submit():
            try:
                trip.name = form.name.data
                trip.location = form.location.data
                trip.start_date = form.start_date.data
                trip.end_date = form.end_date.data
                trip.mileage = form.mileage.data
                trip.notes = form.notes.data

                db.session.commit()

                return redirect(f'/trips/{id}')
            
            except KeyError:
                flash('Please select a valid location', 'danger')
                return redirect('/trips/<int:id>/edit')
        
        return render_template('trips/edit_trip_form.html', form=form, trip=trip)

    @app.route('/trips/<int:id>/status', methods=["POST"])
    def trip_status_update(id):
        """Updated that completion status of a trip"""
        
        trip = Trip.query.get(id)
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        if trip.status == 1:
            trip.status = 2
            db.session.commit()
            
        else:
            trip.status = 1
            db.session.commit()
        
        return redirect('/trips')

    @app.route('/trips/<int:id>/delete', methods=['POST'])
    def delete_trip(id):
        """Delete trip"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        trip = Trip.query.get(id)
        
        if trip.users[0].id != g.user.id:
            flash("You do not have permissions to delete this trip")
            return redirect('/trips')
        
        db.session.delete(trip)
        db.session.commit()

        return redirect('/trips')


    @app.route('/trips/<int:trip_id>/<int:pack_id>', methods=['POST'])
    def add_pack_to_trip(trip_id,pack_id):
        """Add a pack to a trip"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')

        trip_pack = TripPack(trip_id=trip_id, pack_id=pack_id)
        db.session.add(trip_pack)
        db.session.commit()

        return redirect(f'/trips/{trip_id}')

    @app.route('/trips/<int:trip_id>/<int:pack_id>/delete', methods=['POST'])
    def remove_pack_from_trip(trip_id,pack_id):
        """Remove a pack from a trip"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')

        trip_pack = TripPack.query.filter((TripPack.trip_id == trip_id) & (TripPack.pack_id == pack_id)).first()
        db.session.delete(trip_pack)
        db.session.commit()

        return redirect(f'/trips/{trip_id}')

    @app.route('/trips/<int:trip_id>/<int:pack_id>/check')
    def evaluate_pack_for_trip(trip_id, pack_id):
        """Check the contents of a users pack against forecasted weather conditions"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        trip = Trip.query.get(trip_id)
        pack = Pack.query.get(pack_id)
        pack_items = pack.items
        pack_item_names = [];
        
        for item in pack_items:
            pack_item_names.append(item.name)
        
        categories = get_categories(pack_items)
        
        weather_information = get_weather_highs_lows(trip.lat, trip.lng)
        
        if weather_information["temp_high"] >= 80:
            heat_items = Item.query.filter(
                    and_(Item.heat_precautionary == True,
                        Item.essential == False,
                        or_(Item.created_by == 1,
                            Item.created_by == g.user.id))).all() 
        else: 
            heat_items = []
            
            
        if weather_information["temp_low"] <= 45:
            cold_items = Item.query.filter(
                    and_(Item.cold_precautionary == True,
                        Item.essential == False,
                        or_(Item.created_by == 1,
                            Item.created_by == g.user.id))).all()    
        else: 
            cold_items = []
            
            
        if weather_information["chance_of_rain"] <= 25:
            rain_items = Item.query.filter(
                    and_(Item.rain_precautionary == True,
                        Item.essential == False,
                        or_(Item.created_by == 1,
                            Item.created_by == g.user.id))).all()    
        else: 
            rain_items = []
            
            
        essential_items = Item.query.filter(
            and_(Item.essential == True, 
                or_(Item.created_by == 1, Item.created_by == g.user.id)))
        
        emergency_items = Item.query.filter(
            and_(Item.emergency_precautionary == True,
                Item.essential == False,
                or_(Item.created_by == 1,
                    Item.created_by == g.user.id))).all()
        
        
        
        return render_template('packs/check_pack.html', pack_items=pack_items,
                            categories=categories,
                            trip = trip,
                            pack = pack,
                            weather_information = weather_information,
                            heat_items = heat_items,
                            cold_items = cold_items,
                            rain_items = rain_items,
                            essential_items = essential_items,
                            emergency_items = emergency_items,
                            pack_item_names=pack_item_names)
        
    @app.route('/trips/<int:trip_id>/<int:pack_id>/check/edit', methods=['POST'])
    def add_packcheck_items(trip_id, pack_id):
        """Check the contents of the selected pack against the weather conditions of trip duration and provide suggested items to add"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        pack = Pack.query.get(pack_id)
        trip = Trip.query.get(trip_id)
            
        new_items = request.form.getlist('pack-items')

        if new_items:
            for new_item in new_items:
                """Add items that were not originally in the pack"""
                item = Item.query.filter(Item.name == new_item).first()

                pack_item = PackItem(pack_id = pack.id, item_id=item.id)

                db.session.add(pack_item)
                db.session.commit()
                
        return redirect(f'/trips/{trip_id}')


    ###############################################################################################################
    #  Pack routes:

    @app.route('/packs')
    def show_packs():
        """Show all user packs"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')

        user = User.query.get(g.user.id)
        
        packs = Pack.query.filter(Pack.owner == user.id)
        
        
        
        return render_template('packs/packs.html', packs = packs)

    @app.route('/packs/<int:id>')
    def show_pack_details(id):
        """Shows the details of a user's pack"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        user = User.query.get(g.user.id)
        
        pack = Pack.query.get_or_404(id)
        packs = Pack.query.filter(Pack.owner == user.id)

        items = Item.query.join(PackItem, Item.id == PackItem.item_id).filter(PackItem.pack_id == pack.id)
        categories = get_categories(items)

        return render_template('packs/pack_details.html', packs=packs, pack=pack, categories=categories, items=items)


    @app.route('/packs/new', methods =['GET','POST'])
    def create_new_pack():
        """Create a new pack"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        form = AddPackForm()
        
        all_items = Item.query.all()
        
        categories = get_categories(all_items)

        if form.validate_on_submit():
            owner = g.user.id
            name = form.name.data
            notes = form.notes.data

            pack = Pack(owner=owner, 
                        name=name, 
                        notes=notes)

            items = request.form.getlist('pack-items')

            db.session.add(pack)
            db.session.commit()

            for item in items:
                item = Item.query.filter(Item.name == item).first()

                pack_item = PackItem(pack_id = pack.id,
                                    item_id=item.id)

                db.session.add(pack_item)
                db.session.commit()


            return redirect(f'/packs/{pack.id}')
        
        return render_template('/packs/create_pack_form.html', form=form, categories = categories)

    @app.route('/packs/<int:id>/edit', methods=['GET','POST'])
    def edit_pack(id):
        """Edit the contents of a pack"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        
        
        pack = Pack.query.get_or_404(id)
        existing_items = pack.items
        categories = get_categories(existing_items)

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
        
        
        return render_template('packs/edit_pack_form.html', form=form, pack = pack, items = existing_items, categories = categories)
        
    @app.route('/packs/<int:id>/delete', methods=['POST'])
    def delete_pack(id):
        """Delete a user's pack"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        pack = Pack.query.get_or_404(id)

        db.session.delete(pack)
        db.session.commit()

        return redirect('/packs')

    
        
        
        
    ###############################################################################################################
    #  Item routes:
    @app.route('/api/items')
    def get_json_items():
        """Return json dict of items in the database"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        items = Item.query.all()
        serialized = [serialize_item(item) for item in items]

        return jsonify(items = serialized)

    @app.route('/items')
    def get_items():
        """Return a list of items in the database"""
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        items = Item.query.filter((Item.created_by == 1) | (Item.created_by == g.user.id)).all()

        categories = get_categories(items)

        return render_template('/items/items.html', items=items, categories=categories)

    @app.route('/items/new', methods=["GET","POST"])
    def create_new_item():
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        form = AddItemForm()
        
        if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            essential = bool(form.essential.data)
            rain_precautionary = bool(form.rain_precautionary.data)
            cold_precautionary = bool(form.cold_precautionary.data)
            heat_precautionary = bool(form.heat_precautionary.data)
            emergency_precautionary = bool(form.emergency_precautionary.data)
            removable = bool(request.form['removable'])
            
            item = Item(name = name,
                        category = category,
                        essential = essential ,
                        rain_precautionary = rain_precautionary ,
                        cold_precautionary = cold_precautionary ,
                        heat_precautionary = heat_precautionary ,
                        emergency_precautionary = emergency_precautionary,
                        created_by= g.user.id,
                        removable = removable)
            
            db.session.add(item)
            db.session.commit()
            
            return redirect('/items')
        
        return render_template('/items/create-item.html', form=form)

    # @app.route('/items/<int:id>')

    @app.route('/items/<int:id>/edit', methods=["GET","POST"])
    def edit_item(id):
        """Render edit item content and handle form submission"""
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        form = EditItemForm()
        
        item = Item.query.get(id)
        
        if item.removable == False:
            flash('This item is not editable')
            return redirect('/items')
        
        if form.validate_on_submit():
            item.name = form.name.data
            item.category = form.category.data
            item.essential = bool(form.essential.data)
            item.rain_precautionary = bool(form.rain_precautionary.data)
            item.cold_precautionary = bool(form.cold_precautionary.data)
            item.heat_precautionary = bool(form.heat_precautionary.data)
            item.emergency_precautionary = bool(form.emergency_precautionary.data)
            item.removable = bool(request.form['removable'])
            
            db.session.commit()
            
            return redirect('/items')
        
        return render_template('/items/edit-item.html', form=form, item=item)

    @app.route('/items/<int:id>/delete', methods=['POST'])
    def delete_item(id):
        """Deletes an item from the databse if was created by the user"""
        
        
        if not g.user:
            flash("Please login", "error")
            return redirect('/login')
        
        item = Item.query.get(id)
        
        if item.removable == False:
            flash('This item is not removable')
            return redirect('/items')
        
        db.session.delete(item)
        db.session.commit()
        
        
        flash('Item deleted', 'success')
        return redirect('/items')
    
    return app

    
if __name__ == '__main__':
    app = create_app('packlist')
    connect_db(app)
    app.run(debug=True)