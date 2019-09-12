class SqlQueries:
    create_tables = ("""
               CREATE TABLE IF NOT EXISTS  public.staging_cities(
                      id varchar(256),
                      city varchar(256),
                      city2 varchar(256),
                      zip_code varchar(256),
                      dst varchar(256),
                      geopoint varchar(256),
                      longitude varchar(256),
                      state varchar(256),
                      latitude varchar(256),
                      timezone varchar(256),
   					  city_id varchar(256)
 );

    CREATE TABLE IF NOT EXISTS public.staging_city_bikes_data(
                        id INT IDENTITY(1,1),        
                        tripduration  varchar(256),
                        starttime varchar(256),
                        stoptime varchar(256),
                        start_station_id varchar(256),
                        start_station_name varchar(256),
                        start_station_latitude varchar(256),
                        start_station_longitude varchar(256),
                        end_station_id varchar(256),
                        end_station_name varchar(256),
                        end_station_latitude varchar(256),
                        end_station_longitude varchar(256),
                        bikeid varchar(256),
                        usertype varchar(256),
                        birth_year varchar(256),
                        gender varchar(256)
        );

        CREATE TABLE IF NOT EXISTS public.cities (
            cityid int NOT NULL,
            city varchar(256),
            state varchar(256),
            zip_code varchar(256),
            geopoint varchar(256),
            lattitude float,
            longitude float
        );

        CREATE TABLE IF NOT EXISTS public.time (
            start_time timestamp NOT NULL,
            hour INTEGER,
            day INTEGER,
            week INTEGER,
            month INTEGER,
            year INTEGER,
            weekday INTEGER,
            PRIMARY KEY (start_time)
        );

    CREATE TABLE IF NOT EXISTS public.stations (
            stationid varchar(256) NOT NULL,
            station_name varchar(256),
            station_latitude float,
            station_longitude float,
            station_zipcode varchar(256)
        );

        CREATE TABLE IF NOT EXISTS public.trips (
            tripid int ,
            start_time timestamp NOT NULL,
            end_time timestamp NOT NULL,
            start_hour INTEGER,
            end_hour INTEGER,
            start_station varchar(256),
            end_station varchar(256),
            duration numeric(18,0),
            bikeid int,
            user_type (varchar),
            gender (varchar)
        );

        CREATE TABLE IF NOT EXISTS public.users (
            usertype varchar(256) NOT NULL,
            gender varchar(256)
        );

    """)
    cities_table_insert = ("""
        SELECT CAST(city_id as int), city, state, zip_code, geopoint, CAST(latitude as float), CAST(longitude as float)
        FROM staging_cities
    """)

    user_table_insert = ("""
        SELECT distinct usertype, gender
        FROM staging_city_bikes_data
    """)

    stations_table_insert = ("""
        SELECT distinct start_station_id, start_station_name, cast(start_station_latitude as float), cast(start_station_longitude as float), zip_code
        FROM staging_city_bikes_data a
        left join staging_cities b on a.start_station_latitude = b.latitude
        and a.start_station_longitude = b.longitude
    """)

    trips_table_insert = ("""
        SELECT distinct id, cast(starttime as timestamp), cast(stoptime as timestamp), extract(hour from cast(starttime as timestamp)), extract(hour from cast(stoptime as timestamp)), start_station_name, end_station_name, cast(tripduration as int), cast(bikeid as int), usertype, gender
        FROM staging_city_bikes_data
    """)

    time_table_insert = ("""
        SELECT cast(starttime as timestamp), extract(hour from cast(starttime as timestamp)), extract(day from cast(starttime as timestamp)), extract(week from cast(starttime as timestamp)), 
               extract(month from cast(starttime as timestamp)), extract(year from cast(starttime as timestamp)), extract(dayofweek from cast(starttime as timestamp))
        FROM staging_city_bikes_data
    """)
