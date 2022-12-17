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


"""ERROR CASES:

1) Insufficient store information:
        - Required store information to accurately display geolocation: INTERNAL STORE ID, LEGAL ADDRESS LINE, LEGAL STATE, LEGAL COUNTRY.
        - If there is a typefeller in any of these fields, incorrect latitude and longitude will be displayed.
        - If ANY of these fields are empty (other than INTERNAL STORE ID which, to the API, is irrelevant), incorrect latitude and longitude values will be displayed.
        - Have to check what happens if you add data (post code etc.)
        - If a dummy address is provided, an IndexError is thrown...?
2) Multiple latitude and longitude values for a single location:
        - https://stackoverflow.com/questions/34628171/google-maps-geocode-never-returns-multiple-results
        - https://groups.google.com/g/google-maps-js-api-v3/c/UAyUg1BWyoo
        - https://medium.com/geoblinktech/3-pitfalls-to-avoid-when-working-with-googles-geocoding-api-4a7871a88600
3) Separating insufficiently defined store addresses:
        - Store addresses which lack the required fields listed in 1) are stored into a separate file, 'corrupt_stores.csv'.
        - These stores will NOT be listed in the 'stores_lat_lng.csv' file."""

"""TO DO:

Figure out why the program keeps printing the same longitude and latitude.
        THIS IS DONE! I had to convert the variable 'data_output' from a list to a string so the API could read it properly (this was a problem early on, in the final code there is no variable 'data_output', rather 'line')
Fix German characters not displaying properly when parsed through.
        THIS IS DONE!
Figure out how to remove the last comma and qoutation marks when parsing (other than using data.append('\n), because that adds them, without it its parsed as just one long line).
        THIS IS DONE! I created a variable 'line' which uses regex syntax to parse through the .csv file 'store_data' in a different way than .append does. This worked, and now there are no excess commas nor qoutation marks in the .csv file 'parsed_data.csv'.
Figure out how to apply the API to multiple stores instead of one (will need to pay fot this, so I'll need to find an API that offers this for free, or a cheaper one at least).
        THIS IS DONE! I used the Google Cloud Platform geocoding API which has the API batch requests feature.

###DEAD CODE (for reference):

!!!This code contains comments which refer to variables and file names that are not present in the final version of the code!!! Just keep that in mind;)

str1 = " "
s = str1.join(line)

#defining array variable 'data_output' into which the data from the input file 'store_data.csv' will be added
data_output = []
print(row[1], row[22], row[23], row[24], row[25], row[26])
data_output.append(row["Store Internal Id"])
data_output.append(row["Legal Address Line"])
data_output.append(row["Legal State"])
data_output.append(row["Legal Country"])
data_output.append('\n')
print(line)
   
#removing the commas from the new .csv file (THIS CODE IS NOT NEEDED, can delete)
df = open('parsed_data.csv', mode = 'r')
df["Store Internal Id"] = df["Store Internal Id"].replace(",", "")
df.to_csv('parsed_data.csv')
with open("parsed_data.csv", mode = "r") as csv_file:
   csv_reader2 = csv.DictReader(csv_file, delimiter = ",")
   
   for row in csv_reader2:
       if d["Store Internal Id"]:
        csv_file.write(row.replace(",",""))

#implementing the API using requests and json (on only one address from the 'parsed_data.csv' file for now)
gmaps = googlemaps.Client(key = 'AIzaSyD2NsOcvJOGSuC5zARcA9-k4XkauokYpzc')
print(line)
gmaps_result = googlemaps.geocode(line)
print(gmaps_result)
#defining the given Google Cloud Platform API key
API_KEY = 'AIzaSyD2NsOcvJOGSuC5zARcA9-k4XkauokYpzc'

gmaps_key = googlemaps.Client(key = 'AIzaSyD2NsOcvJOGSuC5zARcA9-k4XkauokYpzc')

line["LAT"] = None
line["LON"] = None

#defining variable 'address' which contains parsed addresses
address = line
print(address)

d#efining required parameters
params = {
       'key': API_KEY,
       'address': line
}

#defining the API endpoint
base_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(line)

gmaps_key = googlemaps.Client(key = 'AIzaSyD2NsOcvJOGSuC5zARcA9-k4XkauokYpzc')

#getting the data in JSON format
response = requests.get(base_url, params=params).json()

for item in data:
            data_view = item['data']
            for details in data_view:
                print(details['latitude']+" **"+details['longitude']) 

#defining variable 'address' which contains parsed addresses
address = line
print(address)

#parsing the JSON data to display the longitude and latitude only
for item in data:
    lat = item['data']['latitude']
    lon = item['data']['longitude']
    print("Latitude:",lat,"Longitude:",lon)

geometry = data['location']
lat = geometry['lat']
lon = geometry['lng']
print("Latitude:",lat,"\nLongitude:",lon)

geometry = response['results'][0]['geometry']
lat = geometry['location']['lat']
lng = geometry['location']['lng']

for item in data:
    data_view = item['data']
    for details in data_view:
        print(details['latitude']+" **"+details['longitude'])

#printing the API response
print(data)

#parsing the JSON data to display the longitude and latitude only
for item in data:
    lat = item['data']['latitude']
    lon = item['data']['longitude']
    print("Latitude:",lat,"Longitude:",lon)

geometry = data['location']
lat = geometry['lat']
lon = geometry['lng']
print("Latitude:",lat,"\nLongitude:",lon)

#printing data from variable 'data' to .json file for better readability of variable content
d = open ('store_info.json', mode = "w")
jayson = json.dumps(line)
d.write(jayson)
d.close()

#adding the recieved latitude and longitude values back to the 'stores.csv' csv file (this is not needed, I experimented):
new_row_longitude = next(csv_reader)
new_row_longitude.append("Longiude")
adding_data = open('stores.csv', mode = 'a')
latitude = []
longitude = []

csv_reader2 = csv.writer(adding_data)
csv_reader2.writerow(str(latitude))
csv_reader2.writerow(str(longitude))

#printing store info, latitude, longitude:
print(line,latitude,longitude)
#printing data from variable 'data' to a new .json file 'store_info.json' for better readability of the API response content (because the API response is given in .json format):
d = open ('store_info.json', mode = "w")
save_to_json = json.dumps(response)
d.write(save_to_json)
d.close()"""