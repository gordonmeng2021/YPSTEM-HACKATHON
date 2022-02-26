# Entry point for the application.
from . import app    # For application discovery by the 'flask' command.
from . import views  # For import side-effects of setting up routes.

#To run the file:
#Type "set FLASK_APP=portfolio.webapp" in terminal.
#Navigate into the portfolio folder, then launch the program using "python -m flask run"
