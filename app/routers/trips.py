from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from ..db import cur
from ..helpers.sql import serialize


class Trip(BaseModel):
    name: str            
    location: str            
    start_date: date         
    end_date: date         
    mileage: int | None = None
    notes: str | None = None
    lat: float | None = None
    lng: float | None = None
    status: int         

router = APIRouter(
    prefix='/trips',
    tags=['trips']
)

@router.get('/')
def find_all_trips():
    """Show all trips"""

    query = """
            SELECT id, name, location, start_date, end_date, mileage, notes, lat, lng, status
            FROM trips
            """
    cur.execute(query)
    trips = cur.fetchall()
    
    return trips

@router.get('/{trip_id}')
def find_a_trip(trip_id):
    """Show the details of a trip"""
    
    query = """
        SELECT id, name, location, start_date, end_date, mileage, notes, lat, lng, status
        FROM trips
        WHERE id = %s
        """
    cur.execute(query, trip_id)
    trip = cur.fetchone()
    return trip

@router.post('/')
def create_new_trip(data: Trip):
    """Creata a new trip"""
    
    data = data.model_dump()
    
    query = """
            INSERT INTO trips (name, location, start_date, end_date, mileage, notes, lat, lng, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING name, location, start_date AS "startDate", end_date AS "endDate", mileage, notes, lat, lng, status
            """
    cur.execute(query, (
         data['name'],
         data['location'],
         data['start_date'],
         data['end_date'],
         data['mileage'],
         data['notes'],
         data['lat'],
         data['lng'],
         data['status']))
    
    new_trip = cur.fetchone()
    return new_trip


@router.put('/{trip_id}')
def edit_a_trip(trip_id, data: Trip):
    """Handle edit trip form"""
    
    data = data.model_dump()
    
    set_cols  = serialize(data)["set_cols"]
    raw_values = serialize(data)["raw_values"]
    
    query = f"""
            UPDATE trips
            SET
            {set_cols}
            WHERE id = %s
            RETURNING *
            """
    
    cur.execute(query, (*raw_values, trip_id))
    updated_trip = cur.fetchone()
    
    return updated_trip
    

@router.delete('/{trip_id}')
def delete_trip(trip_id):
    """Delete trip"""
    return

@router.post('/{trip_id}/addpack')
def add_pack_to_trip(trip_id):
    """Add a pack to a trip"""

    
    # get pack id from request
    return

@router.delete('/{trip_id}')
def remove_pack_from_trip(trip_id,pack_id):
    """Remove a pack from a trip"""
    return

# @router('/trips/<int:trip_id>/<int:pack_id>/check')
# def evaluate_pack_for_trip(trip_id, pack_id):
#     """Check the contents of a users pack against forecasted weather conditions"""
    
#     if not g.user:
#         flash("Please login", "error")
#         return redirect('/login')
    
#     trip = Trip.query.get(trip_id)
#     pack = Pack.query.get(pack_id)
#     pack_items = pack.items
#     pack_item_names = [];
    
#     for item in pack_items:
#         pack_item_names.ndr(item.name)
    
#     categories = get_categories(pack_items)
    
#     weather_information = get_weather_highs_lows(trip.lat, trip.lng)
    
#     if weather_information["temp_high"] >= 80:
#         heat_items = Item.query.filter(
#                 and_(Item.heat_precautionary == True,
#                     Item.essential == False,
#                     or_(Item.created_by == 1,
#                         Item.created_by == g.user.id))).all() 
#     else: 
#         heat_items = []
        
        
#     if weather_information["temp_low"] <= 45:
#         cold_items = Item.query.filter(
#                 and_(Item.cold_precautionary == True,
#                     Item.essential == False,
#                     or_(Item.created_by == 1,
#                         Item.created_by == g.user.id))).all()    
#     else: 
#         cold_items = []
        
        
#     if weather_information["chance_of_rain"] >= 25:
#         rain_items = Item.query.filter(
#                 and_(Item.rain_precautionary == True,
#                     Item.essential == False,
#                     or_(Item.created_by == 1,
#                         Item.created_by == g.user.id))).all()    
#     else: 
#         rain_items = []
        
        
#     essential_items = Item.query.filter(
#         and_(Item.essential == True, 
#             or_(Item.created_by == 1, Item.created_by == g.user.id)))
    
#     emergency_items = Item.query.filter(
#         and_(Item.emergency_precautionary == True,
#             Item.essential == False,
#             or_(Item.created_by == 1,
#                 Item.created_by == g.user.id))).all()
    
    
    
#     return render_template('packs/check_pack.html', pack_items=pack_items,
#                         categories=categories,
#                         trip = trip,
#                         pack = pack,
#                         weather_information = weather_information,
#                         heat_items = heat_items,
#                         cold_items = cold_items,
#                         rain_items = rain_items,
#                         essential_items = essential_items,
#                         emergency_items = emergency_items,
#                         pack_item_names=pack_item_names)
    
# @router('/trips/<int:trip_id>/<int:pack_id>/check/edit', methods=['POST'])
# def add_packcheck_items(trip_id, pack_id):
#     """Check the contents of the selected pack against the weather conditions of trip duration and provide suggested items to add"""
#     if not g.user:
#         flash("Please login", "error")
#         return redirect('/login')
    
#     pack = Pack.query.get(pack_id)
#     trip = Trip.query.get(trip_id)
        
#     new_items = request.form.getlist('pack-items')

#     if new_items:
#         for new_item in new_items:
#             """Add items that were not originally in the pack"""
#             item = Item.query.filter(Item.name == new_item).first()

#             pack_item = PackItem(pack_id = pack.id, item_id=item.id)

#             db.session.add(pack_item)
#             db.session.commit()
            
#     return redirect(f'/trips/{trip_id}')