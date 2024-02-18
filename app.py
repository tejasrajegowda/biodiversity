from flask import Flask, render_template, request, abort, jsonify, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)


# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'roots'
app.config['MYSQL_DB'] = 'biodiversity_monitoring_system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # To get results as dictionaries

# Create MySQL connection
mysql = MySQL(app)



#Homepage
@app.route('/home', methods=['GET'])
def show_home():
    return render_template('home.html')

#Enter biological profiles
@app.route('/links', methods=['GET'])
def show_biological_profiles():
    return render_template('links.html')

#Species Insights
@app.route('/disp_links', methods=['GET'])
def show_species_insights():
    return render_template('disp_links.html')





# Route for signin page
@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check credentials in the database
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM USERS WHERE EMAIL = %s AND PASSWORD = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Redirect to the homepage upon successful signin
            return render_template('home.html')
        else:
            # Display an error message if signin fails
            error = 'Invalid email or password. Please try again.'
            return render_template('signin.html', error=error)

    return render_template('signin.html')



# Display all users
@app.route('/users_disp', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    users_data = cur.fetchall()
    cur.close()
    return jsonify(users_data)

# Route to show the form for adding user
@app.route('/users', methods=['GET'])
def show_user_form():
    return render_template('users.html')

# Route to handle form submission for adding user
@app.route('/users', methods=['POST'])
def add_user():
    try:
        # Retrieve data from the submitted form
        user_id = request.form.get('userId')
        username = request.form.get('username')
        name = request.form.get('name')
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO users (USER_ID, USERNAME, NAME, ROLE, EMAIL, PASSWORD) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (user_id, username, name, role, email, password)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return redirect('/home')
    except Exception as e:
        return jsonify({"error": str(e)}), 500





#SPECIES

#disp SPECIES form
@app.route('/species_disp', methods=['GET'])
def get_species():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM species')
    species_data = cur.fetchall()
    cur.close()
    return render_template('species_disp.html', species_data=species_data)

# Route to show the SPECIES form
@app.route('/species', methods=['GET'])
def show_species_form():
    return render_template('species.html')

# Route to handle SPECIES form submission
@app.route('/species', methods=['POST'])
def add_species():
    try:
        # Retrieve data from the submitted form
        species_id = request.form.get('speciesId')
        common_name = request.form.get('commonName')
        scientific_name = request.form.get('scientificName')
        habitat_type = request.form.get('habitatType')
        system_type = request.form.get('systemType')
        lifespan = request.form.get('lifespan')
        generation_length = request.form.get('generationLength')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO species (SPECIES_ID, COMMON_NAME, SCIENTIFIC_NAME, HABITAT_TYPE, SYSTEM_TYPE, LIFESPAN, GENERATION_LENGTH) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (species_id, common_name, scientific_name, habitat_type, system_type, lifespan, generation_length)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Species added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Route to show the SPECIES update form
@app.route('/species/<int:species_id>', methods=['GET'])
def show_species_upd_form(species_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM species WHERE SPECIES_ID = %s', (species_id,))
    species_data = cur.fetchone()
    cur.close()
    return render_template('upd_species.html', species_data=species_data)


# Route to handle SPECIES update form submission
@app.route('/species/<int:species_id>', methods=['POST'])
def update_species(species_id):
    try:
        # Retrieve data from the submitted form
        common_name = request.form.get('commonName')
        scientific_name = request.form.get('scientificName')
        habitat_type = request.form.get('habitatType')
        system_type = request.form.get('systemType')
        lifespan = request.form.get('lifespan')
        generation_length = request.form.get('generationLength')

        # Use Flask-MySQLdb to execute an UPDATE query
        cur = mysql.connection.cursor()
        query = "UPDATE species SET COMMON_NAME=%s, SCIENTIFIC_NAME=%s, HABITAT_TYPE=%s, SYSTEM_TYPE=%s, LIFESPAN=%s, GENERATION_LENGTH=%s WHERE SPECIES_ID=%s"
        values = (common_name, scientific_name, habitat_type, system_type, lifespan, generation_length, species_id)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Species updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#Route to handle SPECIES delete form submission
@app.route('/delete_species/<int:species_id>', methods=['GET', 'POST'])
def delete_species(species_id):
    # Check if the species with the given ID exists
    if not species_exists(species_id):
        abort(404,f"Species ID {species_id} not present or deleted already")  # Return a 404 Not Found error if the species doesn't exist

    if request.method == 'GET':
        return render_template('delete_species.html', species_id=species_id)
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM species WHERE species_id = %s', (species_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Species deleted successfully'})

# Helper function to check if a species with the given ID exists
def species_exists(species_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT species_id FROM species WHERE species_id = %s', (species_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None


# Route to show the stored procedure form
@app.route('/stored_procedure', methods=['GET'])
def show_stored_procedure_form():
    return render_template('stored_procedure.html')

# Route to handle the stored procedure request
@app.route('/stored_procedure/<string:scientific_name>', methods=['GET'])
def get_stored_procedure_data(scientific_name):
    try:
        # Call the stored procedure
        cursor = mysql.connection.cursor()
        cursor.callproc('GetSpeciesDataByScientificName', [scientific_name])

        # Retrieve the result of the first SELECT statement (species data)
        species_data = cursor.fetchone()

        # Retrieve the result of the second SELECT statement (taxonomy data)
        cursor.nextset()
        taxonomy_data = cursor.fetchone()

        # Retrieve the result of the third SELECT statement (population data)
        cursor.nextset()
        population_data = cursor.fetchone()

        # Retrieve the result of the fourth SELECT statement (location data)
        cursor.nextset()
        location_data = cursor.fetchone()

        # Retrieve the result of the fifth SELECT statement (wildlife reserve data)
        cursor.nextset()
        wildlife_reserve_data = cursor.fetchone()

        cursor.close()

        return render_template('stored_procedure.html', 
                               species_data=species_data,
                               taxonomy_data=taxonomy_data,
                               population_data=population_data,
                               location_data=location_data,
                               wildlife_reserve_data=wildlife_reserve_data)

    except Exception as e:
        return f"Error: {str(e)}"



#TAXONOMY


# Display all taxonomy entries
@app.route('/taxonomy_disp', methods=['GET'])
def get_taxonomy():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM taxonomy')
    taxonomy_data = cur.fetchall()
    cur.close()
    return render_template('taxonomy_disp.html', taxonomy_data=taxonomy_data)

# Route to show the form for adding taxonomy entry
@app.route('/taxonomy', methods=['GET'])
def show_taxonomy_form():
    return render_template('taxonomy.html')

# Route to handle form submission for adding taxonomy entry
@app.route('/taxonomy', methods=['POST'])
def add_taxonomy():
    try:
        # Retrieve data from the submitted form
        taxonomy_id = request.form.get('taxonomyId')
        scientific_name = request.form.get('scientificName')
        kingdom = request.form.get('kingdom')
        phylum = request.form.get('phylum')
        sp_class = request.form.get('spClass')
        orders = request.form.get('orders')
        family = request.form.get('family')
        genus = request.form.get('genus')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO taxonomy (TAXONOMY_ID, SCIENTIFIC_NAME, KINGDOM, PHYLUM, SP_CLASS, ORDERS, FAMILY, GENUS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (taxonomy_id, scientific_name, kingdom, phylum, sp_class, orders, family, genus)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Taxonomy entry added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to show the TAXONOMY update form
@app.route('/taxonomy/<int:taxonomy_id>', methods=['GET'])
def show_taxnomy_upd_form(taxonomy_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM TAXONOMY WHERE TAXONOMY_ID = %s', (taxonomy_id,))
    taxonomy_data = cur.fetchone()
    cur.close()
    return render_template('upd_taxonomy.html', taxonomy_data=taxonomy_data)

# Route to handle TAXONOMY update form submission
@app.route('/taxonomy/<int:taxonomy_id>', methods=['POST'])
def update_taxonomy(taxonomy_id):
    try:
        # Retrieve data from the submitted form
        scientific_name = request.form.get('scientificName')
        kingdom = request.form.get('kingdom')
        phylum = request.form.get('phylum')
        sp_class = request.form.get('spClass')
        orders = request.form.get('orders')
        family = request.form.get('family')
        genus = request.form.get('genus')

        # Use Flask-MySQLdb to execute an UPDATE query
        cur = mysql.connection.cursor()
        query = "UPDATE taxonomy SET SCIENTIFIC_NAME=%s, KINGDOM=%s, PHYLUM=%s, SP_CLASS=%s, ORDERS=%s, FAMILY=%s, GENUS=%s WHERE TAXONOMY_ID=%s"
        values = (scientific_name, kingdom, phylum, sp_class, orders, family, genus, taxonomy_id)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Taxonomy updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# delete taxonomy operation
@app.route('/delete_taxonomy/<string:taxonomy_id>', methods=['GET', 'POST'])
def delete_taxonomy(taxonomy_id):
    # Check if the taxonomy with the given ID exists
    if not taxonomy_exists(taxonomy_id):
        abort(404, f"Taxonomy ID {taxonomy_id} not present or deleted already")  # Return a 404 Not Found error if the taxonomy doesn't exist

    if request.method == 'GET':
        return render_template('delete_taxonomy.html', taxonomy_id=taxonomy_id)
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM taxonomy WHERE TAXONOMY_ID = %s', (taxonomy_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Taxonomy deleted successfully'})

# Helper function to check if a taxonomy with the given ID exists
def taxonomy_exists(taxonomy_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT TAXONOMY_ID FROM taxonomy WHERE TAXONOMY_ID = %s', (taxonomy_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None




#POPULATION

# Display all populations
@app.route('/population_disp', methods=['GET'])
def get_population():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM population')
    population_data = cur.fetchall()
    cur.close()
    return render_template('population_disp.html', population_data=population_data)

# Route to show the form for adding population
@app.route('/population', methods=['GET'])
def show_population_form():
    return render_template('population.html')

# Route to handle form submission for adding population
@app.route('/population', methods=['POST'])
def add_population():
    try:
        # Retrieve data from the submitted form
        population_id = request.form.get('populationId')
        scientific_name = request.form.get('scientificName')
        population_count = int(request.form.get('populationCount'))  # Convert to integer

        # Determine conservation status based on population count
        if population_count <= 500:
            conservation_status = 'Critically Endangered'
        elif 501 <= population_count <= 2000:
            conservation_status = 'Endangered'
        elif 2001 <= population_count <= 10000:
            conservation_status = 'Vulnerable'
        else:
            conservation_status = 'Least Concern'

        population_trend = request.form.get('populationTrend')
        date_assessed = request.form.get('dateAssessed')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO population (POPULATION_ID, SCIENTIFIC_NAME, CONSERVATION_STATUS, POPULATION_COUNT, POPULATION_TREND, DATE_ASSESSED) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (population_id, scientific_name, conservation_status, population_count, population_trend, date_assessed)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Population added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# Route to show the POPULATION update form
@app.route('/population/<string:population_id>', methods=['GET'])
def show_population_upd_form(population_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM POPULATION WHERE POPULATION_ID = %s', (population_id,))
    population_data = cur.fetchone()
    cur.close()
    return render_template('upd_population.html', population_data=population_data)

# Route to handle POPULATION update form submission
@app.route('/population/<string:population_id>', methods=['POST'])
def update_population(population_id):
    try:
        # Retrieve data from the submitted form
        scientific_name = request.form.get('scientificName')
        population_count = int(request.form.get('populationCount'))  # Convert to integer
        # Determine conservation status based on updated population count
        if population_count <= 500:
            conservation_status = 'Critically Endangered'
        elif 501 <= population_count <= 2000:
            conservation_status = 'Endangered'
        elif 2001 <= population_count <= 10000:
            conservation_status = 'Vulnerable'
        else:
            conservation_status = 'Least Concern'

        population_trend = request.form.get('populationTrend')
        date_assessed = request.form.get('dateAssessed')

        # Use Flask-MySQLdb to execute an UPDATE query
        cur = mysql.connection.cursor()
        query = "UPDATE population SET SCIENTIFIC_NAME=%s, CONSERVATION_STATUS=%s, POPULATION_COUNT=%s, POPULATION_TREND=%s, DATE_ASSESSED=%s WHERE POPULATION_ID=%s"
        values = (scientific_name, conservation_status, population_count, population_trend, date_assessed, population_id)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Population updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# delete population operation
@app.route('/delete_population/<string:population_id>', methods=['GET', 'POST'])
def delete_population(population_id):
    # Check if the population with the given ID exists
    if not population_exists(population_id):
        abort(404, f"Population ID {population_id} not present or deleted already")  # Return a 404 Not Found error if the population doesn't exist

    if request.method == 'GET':
        return render_template('delete_population.html', population_id=population_id)
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM population WHERE POPULATION_ID = %s', (population_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Population deleted successfully'})

# Helper function to check if a population with the given ID exists
def population_exists(population_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT POPULATION_ID FROM population WHERE POPULATION_ID = %s', (population_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None




#LOCATION

# Display all locations
@app.route('/location_disp', methods=['GET'])
def get_location():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM location')
    location_data = cur.fetchall()
    cur.close()
    return render_template('location_disp.html', location_data=location_data)

# Route to show the form for adding location
@app.route('/location', methods=['GET'])
def show_location_form():
    return render_template('location.html')

# Route to handle form submission for adding location
@app.route('/location', methods=['POST'])
def add_location():
    try:
        # Retrieve data from the submitted form
        location_id = request.form.get('locationId')
        scientific_name = request.form.get('scientificName')
        geographic_region = request.form.get('geographicRegion')
        state = request.form.get('state')
        pincode = request.form.get('pincode')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO location (LOCATION_ID, SCIENTIFIC_NAME, GEOGRAPHIC_REGION, STATE, PINCODE) VALUES (%s, %s, %s, %s, %s)"
        values = (location_id, scientific_name, geographic_region, state, pincode)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Location added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to show the LOCATION update form
@app.route('/location/<int:location_id>', methods=['GET'])
def show_location_upd_form(location_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM location WHERE LOCATION_ID = %s', (location_id,))
    location_data = cur.fetchone()
    cur.close()
    return render_template('upd_location.html', location_data=location_data)

# Route to handle LOCATION update form submission
@app.route('/location/<int:location_id>', methods=['POST'])
def update_location(location_id):
    try:
        # Retrieve data from the submitted form
        scientific_name = request.form.get('scientificName')
        geographic_region = request.form.get('geographicRegion')
        state = request.form.get('state')
        pincode = request.form.get('pincode')

        # Use Flask-MySQLdb to execute an UPDATE query
        cur = mysql.connection.cursor()
        query = "UPDATE location SET SCIENTIFIC_NAME=%s, GEOGRAPHIC_REGION=%s, STATE=%s, PINCODE=%s WHERE LOCATION_ID=%s"
        values = (scientific_name, geographic_region, state, pincode, location_id)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Location updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#delete location operation
@app.route('/delete_location/<string:location_id>', methods=['GET', 'POST'])
def delete_location(location_id):
    # Check if the location with the given ID exists
    if not location_exists(location_id):
        abort(404, f"Location ID {location_id} not present or deleted already")  # Return a 404 Not Found error if the location doesn't exist

    if request.method == 'GET':
        return render_template('delete_location.html', location_id=location_id)
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM location WHERE LOCATION_ID = %s', (location_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Location deleted successfully'})

# Helper function to check if a location with the given ID exists
def location_exists(location_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT LOCATION_ID FROM location WHERE LOCATION_ID = %s', (location_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None



#WILDLIFE RESERVE

# Display all wildlife reserves
@app.route('/wildlife_reserve_disp', methods=['GET'])
def get_wildlife_reserve():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM wildlife_reserve')
    wildlife_reserve_data = cur.fetchall()
    cur.close()
    return render_template('wildlife_reserve_disp.html', wildlife_reserve_data=wildlife_reserve_data)


# Route to show the form for adding wildlife reserve
@app.route('/wildlife_reserve', methods=['GET'])
def show_wildlife_reserve_form():
    return render_template('wildlife_reserve.html')

# Route to handle form submission for adding wildlife reserve
@app.route('/wildlife_reserve', methods=['POST'])
def add_wildlife_reserve():
    try:
        # Retrieve data from the submitted form
        reserve_id = request.form.get('reserveId')
        name = request.form.get('name')
        coordinates = request.form.get('coordinates')
        area = request.form.get('area')
        pincode = request.form.get('pincode')
        iconic_species = request.form.get('iconicSpecies')
        established_year = request.form.get('establishedYear')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO wildlife_reserve (RESERVE_ID, NAME, COORDINATES, AREA, PINCODE, ICONIC_SPECIES, ESTABLISHED_YEAR) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (reserve_id, name, coordinates, area, pincode, iconic_species, established_year)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Wildlife reserve added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to show the WILDLIFE_RESERVE update form
@app.route('/wildlife_reserve/<int:reserve_id>', methods=['GET'])
def show_wildlife_reserve_upd_form(reserve_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM WILDLIFE_RESERVE WHERE RESERVE_ID = %s', (reserve_id,))
    reserve_data = cur.fetchone()
    cur.close()
    return render_template('upd_wildlife_reserve.html', reserve_data=reserve_data)

# Route to handle WILDLIFE_RESERVE update form submission
@app.route('/wildlife_reserve/<int:reserve_id>', methods=['POST'])
def update_wildlife_reserve(reserve_id):
    try:
        # Retrieve data from the submitted form
        name = request.form.get('name')
        coordinates = request.form.get('coordinates')
        area = request.form.get('area')
        pincode = request.form.get('pincode')
        iconic_species = request.form.get('iconicSpecies')
        established_year = request.form.get('establishedYear')

        # Use Flask-MySQLdb to execute an UPDATE query
        cur = mysql.connection.cursor()
        query = "UPDATE wildlife_reserve SET NAME=%s, COORDINATES=%s, AREA=%s, PINCODE=%s, ICONIC_SPECIES=%s, ESTABLISHED_YEAR=%s WHERE RESERVE_ID=%s"
        values = (name, coordinates, area, pincode, iconic_species, established_year, reserve_id)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Wildlife reserve updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# delete wildlife reserve operation
@app.route('/delete_wildlife_reserve/<int:reserve_id>', methods=['GET', 'POST'])
def delete_wildlife_reserve(reserve_id):
    # Check if the wildlife reserve with the given ID exists
    if not wildlife_reserve_exists(reserve_id):
        abort(404, f"Wildlife Reserve ID {reserve_id} not present or deleted already")  # Return a 404 Not Found error if the wildlife reserve doesn't exist

    if request.method == 'GET':
        return render_template('delete_wildlife_reserve.html', reserve_id=reserve_id)
    elif request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM wildlife_reserve WHERE RESERVE_ID = %s', (reserve_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Wildlife Reserve deleted successfully'})

# Helper function to check if a wildlife reserve with the given ID exists
def wildlife_reserve_exists(reserve_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT RESERVE_ID FROM wildlife_reserve WHERE RESERVE_ID = %s', (reserve_id,))
    result = cur.fetchone()
    cur.close()
    return result is not None




# Display all observations
@app.route('/observations_disp', methods=['GET'])
def get_observations():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM observations')
    observations_data = cur.fetchall()
    cur.close()
    return jsonify(observations_data)

# Route to show the form for adding observation
@app.route('/observations', methods=['GET'])
def show_observation_form():
    return render_template('observations.html')

# Route to handle form submission for adding observation
@app.route('/observations', methods=['POST'])
def add_observation():
    try:
        # Retrieve data from the submitted form
        observation_id = request.form.get('observationId')
        username = request.form.get('username')
        species_observed = request.form.get('speciesObserved')
        reserve_id = request.form.get('reserveId')
        pincode = request.form.get('pincode')
        observation_date = request.form.get('observationDate')

        # Use Flask-MySQLdb to execute an INSERT query
        cur = mysql.connection.cursor()
        query = "INSERT INTO observations (OBSERVATION_ID, USERNAME, SPECIES_OBSERVED, RESERVE_ID, PINCODE, OBSERVATION_DATE) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (observation_id, username, species_observed, reserve_id, pincode, observation_date)
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()

        # Return a success message
        return jsonify({"message": "Observation added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    









# Your other Flask routes...

if __name__ == '__main__':
    app.run(debug=True)
