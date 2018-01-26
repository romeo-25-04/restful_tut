from app import app
from app import views

app.run(debug=app.config['DEBUG'])
