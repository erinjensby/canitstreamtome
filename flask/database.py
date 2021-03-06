###
### Database Manipulation functions                     
###
import psycopg2
#Database connection variables          
dbconnection = None
cur = None
#Filter variables
movie_filter_values = None
country_filter_values = None
person_filter_values = None
schema = "set schema 'jordan_dev';"

### Database connection startup and shutdone functions
def close_database_connection():
        global dbconnection
        if dbconnection is not None:
              dbconnection.close()  
def startup_database_connection():
        connect_to_database()
        update_filter_values()

def connect_to_database():
        global dbconnection
        global cur
        dbconnection = psycopg2.connect(host="swe-db.coznr5ylokhg.us-east-2.rds.amazonaws.com",database="canitstreamtome_db", user="canitstreamtome", password="swegrp18")
        cur = dbconnection.cursor()
        
def update_filter_values():
        global movie_filter_values,country_filter_values,person_filter_values
        query = schema+"select column_name from information_schema.columns where table_name = 'streamit_movie';"
        send_sql_query(query)
        list = get_sql_results()
        movie_filter_values = [element for tupl in list for element in tupl]
        
        query = schema+"select column_name from information_schema.columns where table_name = 'streamit_person';"
        send_sql_query(query)
        list = get_sql_results()
        person_filter_values = [element for tupl in list for element in tupl]
        
        query = schema+"select column_name from information_schema.columns where table_name = 'streamit_country';"
        send_sql_query(query)
        list = get_sql_results()
        country_filter_values = [element for tupl in list for element in tupl]
### Helper Functions
def send_sql_query(query):
        global dbconnection
        global cur
        if dbconnection is None:
                dbconnection = psycopg2.connect(host="swe-db.coznr5ylokhg.us-east-2.rds.amazonaws.com",database="canitstreamtome_db", user="canitstreamtome", password="swegrp18")
        try:
                cur = dbconnection.cursor()
                cur.execute(query)
        except psycopg2.DatabaseError as error:
                print("ERROR%")
                print(error)

def get_sql_results():
        global cur
        return cur.fetchall()

### Functions to insert DB entries      
def db_insert_movie(title, description,rating,release_date,language,poster_url):
        sql_query = schema+" insert into {0} (title,description,rating,release_date,language,poster_url) values ({1},{2},{3},{4},{5},{6})".format('streamit_movies',title,description,rating,release_date,language,poster_url)
        send_sql_query(sql_query)

def db_insert_person(last_name,first_name,dob,gender):
        sql_query = schema+"insert into streamit_person (last_name,first_name,dob,gender) values ({0},{1},{2},{3})".format(last_name,first_name,dob,gender)
        send_sql_query(sql_query)
def db_insert_country(name,population,languages,flag_url):
        sql_query = schema+"insert into streamit_country (name,population,languages,flag_url) values ({0},{1},{2},{3})".format(name,population,languages,flag_url)
        send_sql_query(sql_query)

### Functions to update DB entries
def db_update_movie(movie_id, column, value):
        sql_query = schema+"update streamit_movie set {0} = {1} where streamit_movie.movie_id = {2}".format(column,value,movie_id)
        set_sql_query(sql_query)
def db_update_person(person_id,column,value):
        sql_query = schema+"update streamit_person set {0} = {1} where streamit_person.person_id = {2}".format(column,value,person_id)
        set_sql_query(sql_query)
def db_update_country(country_id,column,value):
        sql_query = schema+"update streamit_country set {0} = {1} where streamit_country.country_id = {2}".format(column,value,country_id)
        set_sql_query(sql_query)

### Functions to select DB entries with filters
def db_select_movie(filtertype = None, value = None, comparison = "="):
        global movie_filter_values
        if filtertype in movie_filter_values:
                sql_query = schema+"select title,description,rating,release_date,language,poster_url,movie_cast from streamit_movie where {0} {1} {2}".format(filtertype,comparison,value)
        else:
                sql_query = schema+"select title,description,rating,release_date,language,poster_url,movie_cast from streamit_movie"
        send_sql_query(sql_query)
        return get_sql_results()
def db_select_country(filtertype = None, value = None, comparison = "="):
        global country_filter_values
        if filtertype in country_filter_values:
                sql_query = schema+"select name,population,languages,flag_url from streamit_country where {0} {1} {2}".format(filtertype,comparison,value)
        else:
                sql_query = schema+"select name,population,language,flag_url from streamit_country"
        send_sql_query(sql_query)
        return get_sql_results()
def db_select_person(filtertype = None, value = None, comparison = "="):
        global person_filter_values
        if filtertype in person_filter_values:
                sql_query = schema+"select last_name,first_name,photo_url,dob,gender from streamit_person where {0} {1} {2}".format(filtertype,comparison,value)
        else:
                sql_query = schema+"select last_name,first_name,photo_url,dob,gender from streamit_person"
        send_sql_query(sql_query)
        return get_sql_results()

### Testing functions

def test_db():   
        startup_database_connection()
        print("Openned connection succesfully")
        print(movie_filter_values)
        out = db_select_movie()
        print(out)
        close_database_connection()

test_db()
