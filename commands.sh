#!/bin/bash 


# curl --header "Content-Type: application/json" \
#  --request POST \
#  --data '{"first_name":"Vitaliy","last_name":"Yezghor"}' \
#  http://localhost:5000/drivers/driver



 curl --header "Content-Type: application/json" \
  --request PUT \
  --data '{"first_name":"Vitaliy","last_name":"KPI TEF"}' \
  http://localhost:5000/drivers/driver/3


# curl --header "Content-Type: application/json" \
#  --request DELETE \
#  http://localhost:5000/drivers/driver/1


# curl --header "Content-Type: application/json" \
#  --request POST \
#  --data '{"driver_id": 3,"make":"Audi","model":"A4","plate_number":"AA 1234 OO"}' \
#  http://localhost:5000/vehicles/vehicle/

#curl --header "Content-Type: application/json" \
#  --request POST \
#  --data '{"make":"BMW","model":"M5","plate_number":"AA 7777 OO"}' \
#  http://localhost:5000/vehicles/vehicle/


# curl --header "Content-Type: application/json" \
#  --request PUT \
#  --data '{"driver_id": 3,"make":"Mercedes-Benz","model":"S63amg"}' \
#  http://localhost:5000/vehicles/vehicle/1


# curl --header "Content-Type: application/json" \
#  --request DELETE \
#  http://localhost:5000/vehicles/vehicle/1


# curl --request POST \
#  http://localhost:5000/vehicles/set_driver/2

# curl -i http://127.0.0.1:5000/drivers/driver?created_at__gte=10-31-245021