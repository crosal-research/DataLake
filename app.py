##################################################
#  - Instanciates falcon App
#  - Instanciates resouces
#  - add resource to the App's route
##################################################

# import app packages
import falcon
import falcon.asgi

# import from app
from resources.Observation import Observations
from resources.Cliente import Cliente
from resources.Conta import Conta
from resources.Search import Search
from resources.Series import Series
from resources.Table import Table
from resources.Cliente import Cliente
from resources.Survey import Survey

# Instanciates falscon.App classe

app = falcon.asgi.App(middleware=falcon.CORSMiddleware(
    allow_origins='*', allow_credentials='*'))

#  Instnaciates resources to the app
conta = Conta()
cliente = Cliente()
search = Search()
observations = Observations()
users = Cliente()
series = Series()
tables = Table()
surveys = Survey()

### add resources to the route of App ###
# cliente
app.add_route('/api/client', cliente)
app.add_route('/api/client/{email}', cliente )

# conta
app.add_route('/api/accounts', conta)

# search
app.add_route('/api/search', search)


# observation
app.add_route('/api/observations', observations)

# users
app.add_route('/api/users', cliente)
app.add_route('/api/users/{email}', cliente)


# series
app.add_route('/api/series', series)
app.add_route('/api/series/{ticker}', series)

# tables
app.add_route('/api/tables', tables)
app.add_route('/api/tables/{ticker}', tables)

# surveys
app.add_route('/api/surveys', surveys)
app.add_route('/api/surveys/{survey_id}', surveys)
