from app import app
from flask_login import login_required

from src.database.models import Etiquette


@app.route('/get_etiquettes', methods=['GET'])
@login_required
def get_etiquettes():
    """Retrieve etiquettes list from database

    Get all available etiquette that can be added to a task

    Request response :
    JSON object with list of etiquettes
    """
    return [etiquette.as_dict() for etiquette in Etiquette.query.all()]
