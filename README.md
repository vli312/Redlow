#Redlow Projet CS5614

A web-based product that assists homebuyers by displaying the average and median housing prices by zip code for the DMV area. Satellite imagery is used to map neighborhoods, and real estate data from Zillow is aggregated to calculate and visualize median and average housing prices in 2024.

Additionally, a crowdsourced neighborhood insights feature allows local residents to contribute ratings and qualitative reviews regarding school quality, crime rates, amenities, and overall community experience.

Redlow is built with JavaScript + CSS for the frontend, Django for the backend, and PostgreSQL for the database. Redlow also uses Folium for visualizing geo-locations and displaying maps on the web page.

The application currently allows users to explore property price history and make price forecasts at the neighborhood and zip code level around the NoVA region. The application also supports basic-level authentication. It allows users to sign in, sign out, and register as new users. In conjunction with the authentication feature, the application also supports users providing their insights on neighborhood or zip code regions by submitting their reviews.

It is recommended to use Anaconda for project development, which can be installed here - https://www.anaconda.com/download

After finished installing Anaconda, in project working directory, type in the commands below to create and activate your working environment
```
conda env create --name envname --file=environments.yml
conda activate env
```

After activating the environment, set up your PostgresQL database by configuring the port, database, and user credentials in Redlow/setting.py.
```
python manage.py makemigrations
python manage.py migrate
```

To speed up database set up, a dummy set data from Zillow Research Database is provided. After installing all dependencies/libraries and making all migration changes, use the following command to populate the database. 
```
python manage.py import_zillow_data
```

To run the application locally, use the following command to start the server
```
python manage.py runserver
```
