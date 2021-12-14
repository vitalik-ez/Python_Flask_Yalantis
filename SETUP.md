You must have Python 3.9.1 to run this project. If you already have it then follow the commands (Unix/macOS) below:      
1. Clone the git repository with the command below:  
git clone https://github.com/vitalik-ez/Python_Flask_Yalantis.git  
2. Change directory:  
cd Python_Flask_Yalantis
3. Create Virtual Environment:  
python3 -m venv env
4. Activate Virtual Environment:  
source env/bin/activate
5. Install all dependencies:  
pip install -r requirements.txt
6. Set the following environment variables:  
export FLASK_ENV=development  
export FLASK_APP=main.py
7. Create a migration repository with the following command:  
flask db init
8. Then generate an initial migration:  
flask db migrate -m "Initial migration."  
9. Then you must apply the migration to the database:  
flask db upgrade  
10. Run project:  
flask run