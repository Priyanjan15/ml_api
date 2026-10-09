from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import numpy as np
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load model and encoders
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('encoders.pkl', 'rb') as f:
    encoders = pickle.load(f)

# Destination metadata (matches home_screen.dart)
DESTINATION_INFO = {
    'Mirissa Beach': {
        'location': 'Matara District, Southern Province',
        'description': 'A stunning crescent beach famous for whale watching, surfing, and beautiful sunsets.',
        'category': 'Beaches',
        'lat': 5.9443, 'lon': 80.4551,
        'rating': '4.7',
        'image': 'https://www.thewildlifediaries.com/wp-content/uploads/2023/08/Mirissa-beach.jpg.webp',
    },
    'Arugam Bay': {
        'location': 'Ampara District, Eastern Province',
        'description': 'World-renowned surf spot and relaxed beach village on the east coast of Sri Lanka.',
        'category': 'Beaches',
        'lat': 6.8406, 'lon': 81.8354,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Beach_of_Arugam_Bay.jpg/960px-Beach_of_Arugam_Bay.jpg',
    },
    'Unawatuna Beach': {
        'location': 'Galle District, Southern Province',
        'description': 'A sheltered bay with calm turquoise waters, coral reefs, and a laid-back beach scene.',
        'category': 'Beaches',
        'lat': 6.0101, 'lon': 80.2494,
        'rating': '4.6',
        'image': 'https://storage.ghost.io/c/70/8b/708b2000-5c7e-45ce-bf29-9aed2c09de58/content/images/2024/01/WoC-Unawatuna-Beach-Featured.webp',
    },
    'Bentota Beach': {
        'location': 'Galle District, Southern Province',
        'description': 'A premier beach resort destination known for water sports, luxury hotels, and golden sands.',
        'category': 'Beaches',
        'lat': 6.4282, 'lon': 80.0003,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Bentota_beach.jpg/320px-Bentota_beach.jpg',
    },
    'Negombo Beach': {
        'location': 'Gampaha District, Western Province',
        'description': 'A lively beach town near the airport, famous for seafood, Dutch canals, and local culture.',
        'category': 'Beaches',
        'lat': 7.2096, 'lon': 79.8361,
        'rating': '4.3',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Negombo_beach.jpg/320px-Negombo_beach.jpg',
    },
    'Ella': {
        'location': 'Badulla District, Uva Province',
        'description': 'A scenic hill town surrounded by tea plantations, waterfalls, and the famous Nine Arch Bridge.',
        'category': 'Hills',
        'lat': 6.8667, 'lon': 81.0466,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Nine_Arch_Bridge_Ella.jpg/320px-Nine_Arch_Bridge_Ella.jpg',
    },
    'Nuwara Eliya': {
        'location': 'Nuwara Eliya District, Central Province',
        'description': 'Known as "Little England," famous for tea estates, a cool climate, and colonial-era charm.',
        'category': 'Hills',
        'lat': 6.9497, 'lon': 80.7891,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Nuwara_Eliya.jpg/320px-Nuwara_Eliya.jpg',
    },
    'Horton Plains': {
        'location': 'Nuwara Eliya District, Central Province',
        'description': 'A cloud forest plateau with World\'s End cliff drop, Baker\'s Falls, and endemic wildlife.',
        'category': 'Hills',
        'lat': 6.8009, 'lon': 80.8076,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Horton_Plains_National_Park.jpg/320px-Horton_Plains_National_Park.jpg',
    },
    'Yala National Park': {
        'location': 'Hambantota District, Southern Province',
        'description': 'Sri Lanka\'s most visited wildlife reserve, home to leopards, elephants, crocodiles, and hundreds of bird species.',
        'category': 'Wildlife',
        'lat': 6.3728, 'lon': 81.5215,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Leopard_yala.jpg/320px-Leopard_yala.jpg',
    },
    'Udawalawe National Park': {
        'location': 'Ratnapura District, Sabaragamuwa Province',
        'description': 'Best destination to see large herds of Sri Lankan elephants in their natural habitat.',
        'category': 'Wildlife',
        'lat': 6.4741, 'lon': 80.8997,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Udawalawe_Elephant.jpg/320px-Udawalawe_Elephant.jpg',
    },
    'Wilpattu National Park': {
        'location': 'Puttalam District, North Western Province',
        'description': 'Sri Lanka\'s largest national park, famous for leopards, sloth bears, and natural lakes called villus.',
        'category': 'Wildlife',
        'lat': 8.4562, 'lon': 80.0171,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Wilpattu_National_Park.jpg/320px-Wilpattu_National_Park.jpg',
    },
    'Minneriya National Park': {
        'location': 'Polonnaruwa District, North Central Province',
        'description': 'Famous for "The Gathering" — one of the largest elephant gatherings on Earth.',
        'category': 'Wildlife',
        'lat': 8.0394, 'lon': 80.8999,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Minneriya_elephants.jpg/320px-Minneriya_elephants.jpg',
    },
    'Sigiriya': {
        'location': 'Matale District, Central Province',
        'description': 'An ancient rock fortress and UNESCO World Heritage Site with stunning frescoes and lion\'s paw gateway.',
        'category': 'Heritage',
        'lat': 7.9570, 'lon': 80.7603,
        'rating': '4.9',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Sigiriya_%28141688197%29.jpeg',
    },
    'Anuradhapura': {
        'location': 'Anuradhapura District, North Central Province',
        'description': 'Sacred ancient city and UNESCO site with colossal stupas, the sacred Bodhi Tree, and 2,500-year-old ruins.',
        'category': 'Heritage',
        'lat': 8.3114, 'lon': 80.4037,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Anuradhapura_Sri_Lanka.jpg/320px-Anuradhapura_Sri_Lanka.jpg',
    },
    'Polonnaruwa': {
        'location': 'Polonnaruwa District, North Central Province',
        'description': 'A medieval capital with remarkably well-preserved ruins, statues, and the iconic Gal Vihara rock temple.',
        'category': 'Heritage',
        'lat': 7.9398, 'lon': 81.0004,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/p/p1/Polonnaruwa.jpg/320px-Polonnaruwa.jpg',
    },
    'Galle Fort': {
        'location': 'Galle District, Southern Province',
        'description': 'A UNESCO World Heritage colonial fortress with cobblestone streets, boutique cafes, and ocean views.',
        'category': 'Heritage',
        'lat': 6.0269, 'lon': 80.2170,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Galle_Fort.jpg/320px-Galle_Fort.jpg',
    },
    'Colombo': {
        'location': 'Colombo District, Western Province',
        'description': 'Sri Lanka\'s vibrant commercial capital with modern skyscrapers, historic temples, street food, and a busy port.',
        'category': 'Cities',
        'lat': 6.9271, 'lon': 79.8612,
        'rating': '4.4',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Colombo_skyline.jpg/320px-Colombo_skyline.jpg',
    },
    'Kandy': {
        'location': 'Kandy District, Central Province',
        'description': 'The cultural capital of Sri Lanka, home to the sacred Temple of the Tooth Relic and scenic Kandy Lake.',
        'category': 'Cities',
        'lat': 7.2906, 'lon': 80.6337,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kandy_lake.jpg/320px-Kandy_lake.jpg',
    },
    'Galle': {
        'location': 'Galle District, Southern Province',
        'description': 'A charming southern city blending Dutch colonial heritage with beach resorts and a buzzing arts scene.',
        'category': 'Cities',
        'lat': 6.0535, 'lon': 80.2210,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Galle_city.jpg/320px-Galle_city.jpg',
    },
}

def get_current_season():
    month = datetime.now().month
    # Dry season: Dec–Apr; Wet season: May–Nov
    return 'Dry' if month in [12, 1, 2, 3, 4] else 'Wet'

def get_top_recommendations(country, n=3):
    le_country     = encoders['country']
    le_category    = encoders['category']
    le_season      = encoders['season']
    le_destination = encoders['destination']

    # Check if country is known
    if country not in le_country.classes_:
        # Fall back to UK (most generic European tourist profile)
        country = 'UK'

    season = get_current_season()
    country_enc = le_country.transform([country])[0]
    season_enc  = le_season.transform([season])[0]

    # Try all categories and collect probability scores
    results = []
    categories = list(le_category.classes_)

    for cat in categories:
        cat_enc = le_category.transform([cat])[0]
        X = np.array([[country_enc, cat_enc, season_enc]])

        # Get probability for each destination
        proba = model.predict_proba(X)[0]
        dest_classes = le_destination.classes_

        for i, prob in enumerate(proba):
            dest_name = dest_classes[i]
            results.append({
                'name': dest_name,
                'score': float(prob),
                'category': cat,
            })

    # Sort by score, deduplicate by destination name, take top N
    results.sort(key=lambda x: x['score'], reverse=True)
    seen = set()
    top = []
    for r in results:
        if r['name'] not in seen:
            seen.add(r['name'])
            info = DESTINATION_INFO.get(r['name'], {})
            top.append({
                'name':        r['name'],
                'location':    info.get('location', ''),
                'description': info.get('description', ''),
                'category':    info.get('category', r['category']),
                'lat':         info.get('lat', 0.0),
                'lon':         info.get('lon', 0.0),
                'rating':      info.get('rating', '4.5'),
                'image':       info.get('image', ''),
                'score':       round(r['score'], 4),
            })
        if len(top) == n:
            break

    return top


@app.route('/recommend', methods=['GET'])
def recommend():
    country = request.args.get('country', 'UK')
    purpose = request.args.get('purpose', 'Leisure')
    recs = get_top_recommendations(country, n=3)
    return jsonify({'recommendations': recs, 'country': country, 'season': get_current_season()})


@app.route('/countries', methods=['GET'])
def countries():
    return jsonify({'countries': list(encoders['country'].classes_)})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'season': get_current_season()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)