CREATE TABLE public.staging_cities(
			  city_id int NOT NULL,
              city varchar(256) NOT NULL,
              zip_code varchar(256),
              dst int64,
              geopoint varchar(256),
              longitude float64,
              state varchar(256),
              latitude float64,
              timezone int64);
              
CREATE TABLE public.staging_city_bikes_data(
				tripduration  int64,
				starttime timestamp NOT NULL,
				stoptime timestamp NOT NULL,
				start_station_id int64,
				start_station_name varchar(256),
                start_station_latitude float64,
                start_station_longitude float64,
                end_station_id int64,
                end_station_name varchar(256),
                end_station_latitude float64,
                end_station_longitude float64,
                bikeid int64,
                usertype varchar(256),
                birth_year float64,
                gender int64
);

CREATE TABLE public.cities (
	cityid int4 AUTOINCREMENT NOT NULL,
	city varchar(256),
    state varchar(256),
    zip_code varchar(256),
	geopoint varchar(256),
	lattitude float64,
	longitude float64
);

CREATE TABLE public.time (
	start_time timestamp NOT NULL,
	hour INTEGER,
	day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER,
    PRIMARY KEY (start_time)
);

CREATE TABLE public.stations (
	stationid varchar(256) NOT NULL,
	station_name varchar(256),
	station_latitude numeric(18,0),
	station_longitude numeric(18,0),
    station_zipcode varchar(256)
);

CREATE TABLE public.trips (
	tripid int AUTOINCREMENT,
	start_time timestamp NOT NULL,
	end_time timestamp NOT NULL,
	start_station varchar(256),
	end_station varchar(256),
	duration numeric(18,0),
	bikeid int4
);

CREATE TABLE public.users (
	usertype varchar(256) NOT NULL,
	gender varchar(256),
	date varchar(256)
);
