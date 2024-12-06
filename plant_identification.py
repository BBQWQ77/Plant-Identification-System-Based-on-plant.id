from datetime import datetime
from kindwise import PlantApi, PlantIdentification, ClassificationLevel
import re

api = PlantApi(api_key='your own api_key')


def identify_plant(image_path, classification_level=ClassificationLevel.SPECIES):
    images = [image_path]
    details = ['common_names', 'taxonomy', 'image']
    disease_details = ['local_name', 'description', 'treatment', 'cause']
    language = ['en']
    similar_images = True
    latitude_longitude = (49.20340, 16.57318)
    health = 'all'
    custom_id = 14
    date_time = datetime.now()
    max_image_size = 1500
    classification_raw = False

    with open(image_path, 'rb') as image:
        identification_from_stream: PlantIdentification = api.identify(image.read())

    return parse_suggestions(str(identification_from_stream))


def parse_suggestions(output):
    suggestion_pattern = re.compile(
        r"Suggestion\(id=.*?, name='(.*?)', probability=(.*?), similar_images=.*?url='(.*?)'",
        re.DOTALL,
    )
    matches = suggestion_pattern.findall(output)

    suggestions = [
        {"name": match[0], "probability": float(match[1]), "image_url": match[2]}
        for match in matches
    ]
    return suggestions
