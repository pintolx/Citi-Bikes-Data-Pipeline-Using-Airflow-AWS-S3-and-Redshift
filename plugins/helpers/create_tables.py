class SqlCreateTables:
    create_tables = """
               CREATE TABLE IF NOT EXISTS  public.staging_cities(
                      city_id INT NOT NULL,
                      city varchar(256) NOT NULL,
                      zip_code varchar(256),
                      dst int64,
                      geopoint varchar(256),
                      longitude float64,
                      state varchar(256),
                      latitude float64,
                      timezone int64);

                CREATE TABLE IF NOT EXISTS public.staging_city_bikes_data(
                        tripduration  int,
                        starttime timestamp NOT NULL,
                        stoptime timestamp NOT NULL,
                        start_station_id int,
                        start_station_name varchar(256),
                        start_station_latitude float,
                        start_station_longitude float,
                        end_station_id int,
                        end_station_name varchar(256),
                        end_station_latitude float,
                        end_station_longitude float,
                        bikeid int,
                        usertype varchar(256),
                        birth_year float,
                        gender int
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
            station_latitude numeric(18,0),
            station_longitude numeric(18,0),
            station_zipcode varchar(256)
        );

        CREATE TABLE public.trips (
            tripid INT IDENTITY(1,1),
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
    """