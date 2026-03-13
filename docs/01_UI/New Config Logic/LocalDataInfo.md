# LocalData

This file describes the structure of the JSON cache, which is used to store the last configuration. The cache allows you to preload the last configuration when starting the program and reduce the load on the database.

## General description
Data is stored in **JSON** format. The structure repeats the logic of the interface tabs for visual similarity and convenience.

### Format features:
- **ID is missing**: The cache does not store primary and foreign keys of the database, since this is a temporary snapshot of the active configuration.
- **Complete coverage**: The cache contains absolutely all fields necessary for restoring the tuning state without an additional request to the database.

---

## JSON structure

```json
{
    "Used":"False",
    "current_setup": {
        "Session":{
            "Name": "Porshe cirlce rwd S2",
            "Car":"Porshe 911 GT3 RS",
            "pi_rating":988,
            "Road_Type":"Circle",
            "Location":"Racetrack",
            "Surface":"Dry"
        },
        "Info":{
            "weight_kg":1560,
            "weight_dist_front":40,
            "power_hp":500,
            "torque_nm":600,
            "suspension_travel":100,
            "engine_location":"Rear",
            "drive_type":"RWD",
            "Engine_placement":"Rear"
        },
        "Tires":{
            "pressure_front":1.9,
            "pressure_rear":1.8,
            "width_front":225,
            "width_rear":285,
            "compound":"Race"
        },
        "Alignment":{
            "camber_front":-1.6,
            "camber_rear":-0.7,
            "toe_front":0.2,
            "toe_rear":0.1,
            "caster":7.0
        },
        "Spring":{
            "spring_front":150.0,
            "spring_rear":160.0,
            "clearance_front":12.0,
            "clearance_rear":13.0,
            "spring_front_min":80.0,
            "spring_front_max":250.0,
            "spring_rear_min":80.0,
            "spring_rear_max":250.0,
            "clearance_front_min":0.0,
            "clearance_front_max":20.0,
            "clearance_rear_min":0.0,
            "clearance_rear_max":20.0
        },
        "Damping":{
            "rebound_front":11.0,
            "rebound_rear":13.0,
            "bump_front":7.5,
            "bump_rear":8.5,
            "rebound_front_min":0.0,
            "rebound_front_max":20.0,
            "rebound_rear_min":0.0,
            "rebound_rear_max":20.0,
            "bump_front_min":0.0,
            "bump_front_max":20.0,
            "bump_rear_min":0.0,
            "bump_rear_max":20.0
        },
        "Roll-Bar":{
            "roll_bar_front":21.0,
            "roll_bar_rear":30.0
        },
        "Aero":{
            "has_adjustable_aero_front":true,
            "has_adjustable_aero_rear":true,
            "front":150,
            "rear":100,
            "front_min":50,
            "front_max":150,
            "rear_min":50,
            "rear_max":150
        },
        "Brakes":{
            "balance":0.50,
            "power":160
        },
        "Differential":{
            "front_acceleration":0,
            "front_deceleration":0,
            "rear_acceleration":30,
            "rear_deceleration":30,
            "balance":0
        }
    }
}

