import base64
import os

from darknet.main import raw_img_to_covert_processed_img
from darknet import main
import pymysql
from django.shortcuts import render
import uuid
from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json
import time
import datetime
from django.conf import settings


# Create your views here.

@api_view(["POST"])
def imageprocess(data1):
    try:
        # Loading JSON data into the variable "received_json_data"
        received_json_data = json.loads(data1.body)
        source_type_val = received_json_data['source_type']
        waste_type_val = received_json_data['waste_type']
        loc_type_val = received_json_data['loc_type']
        img_raw_val = received_json_data['img_raw']
        waste_char_val = received_json_data['waste_char']
        waste_shape_val = received_json_data['waste_shape']
        waste_status_val = received_json_data['waste_status']
        waste_prod_name_val = received_json_data['waste_prod_name']
        waste_prod_address_val = received_json_data['waste_prod_address']
        other_val = received_json_data['other']
        latitude_val = received_json_data['latitude']
        longitude_val = received_json_data['longitude']
        country_val = received_json_data['country']
        state_val = received_json_data['state']
        district_val = received_json_data['district']
        region_val = received_json_data['region']
        city_val = received_json_data['city']
        street_val = received_json_data['street']
        pincode_val = received_json_data['pincode']
        waste_fun_status = 1

        # PRINTING THE EXTRACTED DATA
        # print(str(source_type_val))
        # print(str(waste_type_val))
        # print(str(loc_type_val))
        # print(str(img_raw_val))
        # print(str(img_processed_val))
        # print(str(time_date_val))
        # print(str(waste_char_val))
        # print(str(waste_shape_val))
        # print(str(waste_status_val))
        # print(str(waste_prod_name_val))
        # print(str(waste_prod_address_val))
        # print(str(other_val))
        # print(str(latitude_val))
        # print(str(longitude_val))
        # print(str(country_val))
        # print(str(state_val))
        # print(str(district_val))
        # print(str(region_val))
        # print(str(city_val))
        # print(str(street_val))
        # print(str(pincode_val))
        # print(str(on_progress_val))

        # GETTING THE CURRENT TIME USING THE FUNCTION "time()"
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        img_raw_val = ImageConversion(img_raw_val, timestamp)

        # ESTABLISHING DATABASE CONNECTION
        db = pymysql.connect("localhost", "root", "", "waste_mainframe_db")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # QUERY
        sql_max_val = """select max(refid) from waste_details"""

        sql_waste_details = """INSERT INTO waste_details(refid, waste_type, loc_type, img_raw_url, img_processed_url, time_date, waste_char, waste_shape, waste_status, waste_fun_status, source_type, on_progress) 
        VALUES(%s, %s, %s, %s, null , %s, %s, %s, %s, %s, %s, null )"""

        sql_product_details = """insert into waste_product_details(refid, waste_prod_name, waste_prod_address, other) 
        values(%s,%s,%s,%s);"""

        sql_location_details = """insert into waste_location_details(refid,latitude,longitude,country,state,district,region,city,street,pincode) 
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

        # TO FETCH THE CURRENT "refid"
        try:
            cursor.execute(sql_max_val)

            rows = cursor.fetchall()

            refid_val = 0
            for row in rows:
                if str(row[0]) == "null" or str(row[0]) == "None":
                    refid_val = 1
                else:
                    refid_val = row[0] + 1

            # print("*** Convert Raw image to  Processed image************")

            # QUERY EXECUTION
            cursor.execute(sql_waste_details, (
                str(refid_val), str(waste_type_val), str(loc_type_val), str(img_raw_val),
                str(timestamp), str(waste_char_val), str(waste_shape_val), str(waste_status_val), str(waste_fun_status),
                str(source_type_val)))

            cursor.execute(sql_product_details, (str(refid_val), str(waste_prod_name_val), str(waste_prod_address_val),
                                                 str(other_val)))
            cursor.execute(sql_location_details, (str(refid_val), str(latitude_val), str(longitude_val),
                                                  str(country_val), str(state_val), str(district_val), str(region_val),
                                                  str(city_val), str(street_val), str(pincode_val)))

            # Commit your changes in the database
            db.commit()

            # CONVERT RAW IMAGE TO PROCESSED IMAGE
            returnkey, returnprocessedImgPath = raw_img_to_covert_processed_img(str(refid_val),
                                                                                "../" + str(img_raw_val),
                                                                                "../WasteProcessedImage")

            # Query to update "img_processed_url" from the table "waste_details"
            update_query = "UPDATE waste_details SET img_processed_url  = %s WHERE refid  = %s"
            update_query_input = (returnprocessedImgPath, returnkey)
            cursor.execute(update_query, update_query_input)

            # Commit your changes in the database
            db.commit()

        except:
            # Rollback in case there is any error
            print("**************Rollback***************")
            db.rollback()

        # execute SQL query using execute() method.
        cursor.execute("SELECT VERSION()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Database version : %s " % data)

        # DISCONNECT DATABASE CONNECTION
        db.close()
        return JsonResponse(({"statustype": "Success", "statusmessage": "Submited Successfull", "statuscode": "200"}),
                            safe=False)
    except ValueError as e:
        print(str(e))
        return JsonResponse(
            ({"statustype": "Failure", "statusmessage": "Submited data is failure", "statuscode": "400"}), safe=False)


def ImageConversion(img_base_64, timestamp):
    # CONVERTING RAW IMAGE TO PROCESSED IMAGE
    # Changing directory to the main directory
    os.chdir(settings.BASE_DIR)
    # Storing base64 image content as string in "imgstr"
    imgstr = str(img_base_64)
    # Decoding base64 image to jpeg image
    imgdata = base64.b64decode(imgstr)
    # Generating name for the image and setting path to store the image
    path = 'WasteRawImage/' + str(uuid.uuid4()) + '.jpg'
    # Opening the specified path and writing the converted jpeg image
    with open(path, "wb+") as fh:
        fh.write(imgdata)
    fh.close()
    return path

# def openSource():
#     try:
#         print(str(json.loads(data.body)['refid']))
#
#         # Open database connection
#         db = pymysql.connect("localhost", "root", "", "waste_mainframe_db")
#
#         # prepare a cursor object using cursor() method
#         cursor = db.cursor()
#         #         sql = """INSERT INTO EMPLOYEE(refid,
#         # waste_type,
#         # loc_type,
#         # img_raw_url,
#         # img_processed_url,
#         # time_date,
#         # waste_char,
#         # waste_shape,
#         # waste_status,
#         # )VALUES (1,1,2,'L3yetLycKOvehsluDinJ8u40AOX26Dim7fvU','L3yetLycKOvehsluDinJ8u40AOX26Dim7fvU',
#         # 2019-05-08 15:19:23,2,5,35,3)"""
#         received_json_data = "'{}'".format(str(json.loads(data.body)['refid']))
#
#         sql = """INSERT INTO testnew(number)VALUES (%s)"""
#         print(sql)
#         try:
#             # Execute the SQL command
#             cursor.execute(sql, str(json.loads(data.body)['refid']))
#             print(sql)
#             # Commit your changes in the database
#             db.commit()
#         except:
#             print("**************Rollback***************")
#
#             # Rollback in case there is any error
#             db.rollback()
#
#         # execute SQL query using execute() method.
#         cursor.execute("SELECT VERSION()")
#
#         # Fetch a single row using fetchone() method.
#         data = cursor.fetchone()
#         print("Database version : %s " % data)
#
#         # disconnect from server
#         db.close()
#
#         return JsonResponse(sql, safe=False)
#     except ValueError as e:
#         return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
