# Store geolocator  
## Description

This is a simple python program incorporating the Google Cloud Platform geolocation API in order to get the geolocation of a number of stores. The program opens the **'stores.csv'** file, parses through it to get only a certain number of columns.  
  
The data from these columns is then sent to the API which returns the store's latitude and longitude values.
Finally, the program spits the latitude and longitude values into the newly created **'stores_lat_lng.csv'** file.
