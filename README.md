### A data analysis web based Django Project.

#### Requirements:
    - Python: >= 3.6
    - Django: 1.11
    
#### Installation:

1. clone the git repository. Go inside of the project directory.
2. create a virtual environment: `virtualenv venv`
3. activate the virual enviroment using `source venv/bin/activate`
4. Go to inside `/src` directory
5. install the requirements: `pip install -r requirements.txt`
   (if error occurs while installing PyYAML, then run `sudo apt-get install python3.6-dev`)
6. Migrate database: `python manage.py migrate`
7. Add Seed data using fixtures: `python manage.py loaddata analysis_types.yaml`
7. collect static files: `python manage.py collectstatic`
8. Run the server: `python manage.py runserver`