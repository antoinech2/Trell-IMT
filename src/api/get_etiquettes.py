from app import app
from flask_login import login_required

from src.database.models import Etiquette


@app.route('/get_etiquettes', methods=['GET'])
@login_required
def get_etiquettes():
    return [{"id": etiquette.id, "name" : etiquette.label, "description":etiquette.description, "type":etiquette.type, "color": etiquette.color} for etiquette in Etiquette.query.all()]
