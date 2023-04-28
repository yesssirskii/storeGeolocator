#importing required modules:
import csv, requests

#opening the 'stores_lat_lng.csv' file in write mode (this is the file into which correct data is written):
out_file = open('stores_lat_lng.csv', mode = 'w')

#opening the 'corrupt_stores.csv' file in write mode (this is the file into which insufficient data is written):
out_file2 = open('corrupt_stores.csv', mode = 'w')

#opening the 'stores.csv' file in read mode (this is the file from which data is collected):
with open('stores.csv', mode = 'r') as in_file:    
    csv_reader = csv.DictReader(in_file)

    #adding a header to the 'stores_lat_lng.csv' and 'corrupt_stores.csv' files for better readability:
    header = "{},{},{},{},\n".format('Internal Store Id', 'Legal Address Line', 'Legal State', 'Legal Country')
    out_file.write(header)
    out_file2.write(header)

    #parsing the 'stores.csv' file to get only the 4 specific needed columns and appending the result to the variable 'data',
    #aswell as sending the contents of the variable 'data' to the API, allowing it to give us a response:
    for row in csv_reader:
        data = "{},{},{},{}".format(row["Store Internal Id"], row["Legal Address Line"], row["Legal State"], row["Legal Country"])

        #defining the given Google Cloud Platform Geocoding API key:
        API_KEY = 'AIzaSyD2NsOcvJOGSuC5zARcA9-k4XkauokYpzc'

        #defining required parameters:
        params = {
        'key': API_KEY,
        'address': data
        }

        #defining the API endpoint:
        base_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(data)

        #getting the data in .json format using 'requests' module and the GET method:
        response = requests.get(base_url, params=params).json()

        #parsing throught the API response and getting latitude and longitude values for each store address ('store_info.json' file for reference):
                #parsing into the 'geometry' sub-category:
        geometry = response['results'][0]['geometry']
                #parsing to the 'latitude' sub-category:
        lat = geometry['location']['lat']
                #parsing to the 'longitude' sub-category:
        lng = geometry['location']['lng']

        #defining variable 'data_lat_lng' to write store info, latitude and longitude to 'stores_lan_lng.csv' file:
        data_lat_lng = "{},{},{},\n".format(data, lat, lng)
        insufficient_data = "{},\n".format(data)

        #printing its contents:
        print(data_lat_lng)

        #filtering the results so that sufficiently defined store addresses are written into the 'stores_lat_lng.csv' file
        if row["Legal Address Line"] != '' or row["Legal State"] != '' or row["Legal Country"] != '' :
                #writing data from the 'data_lat_lng' variable to the 'stores_lat_lng.csv' file:
                out_file.write(data_lat_lng)
        #filtering the results so that insufficiently defined store addresses are written into the 'corrupt_stores.csv' file (all data minus the latitude and longitude values)
        elif row["Legal Address Line"] == '' or row["Legal State"] == '' or row["Legal Country"] == '' :
                out_file2.write(insufficient_data)

#closing all files:
in_file.close()
out_file.close()
out_file2.close()
