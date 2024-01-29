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

# Route for signin page
@app.route('/signin', methods=['GET', 'POST'])
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







#disp SPECIES form
@app.route('/species_disp', methods=['GET'])
def get_species():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM species')
    species_data = cur.fetchall()
    cur.close()
    return jsonify(species_data)

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








# Display all taxonomy entries
@app.route('/taxonomy_disp', methods=['GET'])
def get_taxonomy():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM taxonomy')
    taxonomy_data = cur.fetchall()
    cur.close()
    return jsonify(taxonomy_data)

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







# Display all populations
@app.route('/population_disp', methods=['GET'])
def get_population():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM population')
    population_data = cur.fetchall()
    cur.close()
    return jsonify(population_data)

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
        conservation_status = request.form.get('conservationStatus')
        population_count = request.form.get('populationCount')
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





# Display all locations
@app.route('/location_disp', methods=['GET'])
def get_location():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM location')
    location_data = cur.fetchall()
    cur.close()
    return jsonify(location_data)

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






# Display all wildlife reserves
@app.route('/wildlife_reserve_disp', methods=['GET'])
def get_wildlife_reserves():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM wildlife_reserve')
    reserves_data = cur.fetchall()
    cur.close()
    return jsonify(reserves_data)

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
