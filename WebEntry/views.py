import base64
import os
from darknet.main import raw_img_to_covert_processed_img
import pymysql
import uuid
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import time
import datetime
from django.conf import settings
import MySQLdb as my


# Create your views here.

@api_view(["POST"])
def imageprocess(data):
    try:
        # Loading JSON data into the variable "received_json_data"
        received_json_data = json.loads(data.body)

        # Parsing JSON data
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

        # GETTING THE CURRENT TIME USING THE FUNCTION "time()"
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        # Passing raw image to image conversion function
        img_raw_val = ImageConversion(img_raw_val, timestamp)

        # ESTABLISHING DATABASE CONNECTION
        db = pymysql.connect("localhost", "root", "", "waste_mainframe_db")

        # Prepare a cursor object using cursor() method
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

        # Execute SQL query using execute() method.
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


@api_view(["POST"])
def getwastedetails(data):
    try:
        # Loading JSON data into the variable "received_json_data"
        reseived_json_data = json.loads(data.body)

        from_time_and_date = reseived_json_data['from']
        to_time_and_date = reseived_json_data['to']

        # ESTABLISHING DATABASE CONNECTION
        db = pymysql.connect("localhost", "root", "", "waste_mainframe_db")

        # Prepare a cursor object using cursor() method
        cursor = db.cursor()

        # QUERY
        sql = "SELECT waste_details.refid, waste_details.waste_type,waste_details.loc_type,waste_details.img_raw_url," \
              "waste_details.img_processed_url,waste_details.time_date,waste_details.waste_char,waste_details.waste_shape," \
              "waste_details.waste_status,waste_details.waste_fun_status,waste_details.source_type,waste_details.on_progress," \
              "waste_location_details.latitude,waste_location_details.longitude,waste_location_details.country,	waste_location_details.state," \
              "waste_location_details.district,	waste_location_details.region,	waste_location_details.city,waste_location_details.street," \
              "waste_location_details.pincode,	waste_product_details.waste_prod_name," \
              "waste_product_details.waste_prod_address,waste_product_details.other " \
              "FROM waste_details INNER JOIN waste_location_details ON waste_details.refid = waste_location_details.refid " \
              "INNER JOIN waste_product_details ON waste_location_details.refid = waste_product_details.refid " \
              "WHERE waste_details.time_date between %s and %s;"

        try:
            # QUERY EXECUTION
            cursor.execute(sql, (str(from_time_and_date), str(to_time_and_date)))
            waste_details = cursor.fetchall()

            final_lst = []
            final_dic = {}

            # Storing attributes of a table in a list
            waste_lst = ["refid", "waste_type", "loc_type", "img_raw_url", "img_processed_url", "time_date",
                         "waste_char", "waste_shape", "waste_status", "waste_fun_status", "source_type",
                         "on_progress", "latitude", "longitude", "country", "state", "district", "region",
                         "city", "street", "pincode", "waste_prod_name", "waste_prod_address", "other"]

            # Iterating through the data and storing it to the dictionary and appending the dictionary to the list
            for x in waste_details:
                for y in range(len(x)):
                    final_dic[waste_lst[y]] = x[y]
                final_lst.append(final_dic.copy())

        except my.Error as e:
            print(e)
            # Rollback in case there is any error
            print("**************Rollback***************")
            db.rollback()

            # Execute SQL query using execute() method.
            cursor.execute("SELECT VERSION()")

            # Fetch a single row using fetchone() method.
            data = cursor.fetchone()
            print("Database version : %s " % data)

            # DISCONNECT DATABASE CONNECTION
            db.close()
        return JsonResponse(
            (
                {"statustype": "Success", "Data": final_lst, "statusmessage": "Submited Successfull",
                 "statuscode": "200"}),
            safe=False)
    except ValueError as e:
        print(str(e))
        return JsonResponse(
            ({"statustype": "Failure", "statusmessage": "Submited data is failure", "statuscode": "400"}), safe=False)
