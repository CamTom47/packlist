from datetime import datetime

def count_trips_completed(trips):
    count = 0
    
    for trip in trips:
        if trip.status == 2:
            count += 1
            
    return count

def count_upcoming_trips(trips):
    count = 0
    
    for trip in trips:
        if trip.status == 1:
            count += 1
            
    return count

def average_trip_mileage(trips):
    mileage = 0;
    
    if (len(trips) == 0):
        return 0;
    else:
        
        for trip in trips:
            
            if trip.status == 2:
                mileage += trip.mileage
            
        average_mileage = round(mileage/len(trips), 2)
        
        return average_mileage

def total_mileage_completed(trips):
    total_mileage = 0;
    for trip in trips:
        if trip.status == 2:
            
            total_mileage += trip.mileage
               
    return total_mileage

def total_days_backpacking(trips):
    duration = 0
    
    for trip in trips:
        if trip.status == 2:
            duration += abs((trip.end_date - trip.start_date).days)
        
    return duration

