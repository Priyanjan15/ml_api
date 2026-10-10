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
    "Adam's Peak": {
        'location': 'Ratnapura District, Sabaragamuwa Province',
        'description': 'A sacred mountain peak with a famous pilgrimage trail, offering breathtaking sunrise views.',
        'category': 'Adventure',
        'lat': 6.8096, 'lon': 80.4994,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Adams_peak_pilgrims.jpg/320px-Adams_peak_pilgrims.jpg',
    },
    'Sigiriya Rock Fortress': {
        'location': 'Matale District, Central Province',
        'description': 'An ancient rock fortress and UNESCO World Heritage Site with stunning frescoes and lion paw gateway.',
        'category': 'Heritage',
        'lat': 7.9570, 'lon': 80.7603,
        'rating': '4.9',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Sigiriya_%28141688197%29.jpeg',
    },
    'Temple of the Tooth': {
        'location': 'Kandy District, Central Province',
        'description': 'The sacred Buddhist temple housing the relic of the tooth of the Buddha, a UNESCO World Heritage Site.',
        'category': 'Temples',
        'lat': 7.2936, 'lon': 80.6413,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Temple_of_the_Tooth.jpg/320px-Temple_of_the_Tooth.jpg',
    },
    'Kandy City': {
        'location': 'Kandy District, Central Province',
        'description': 'The cultural capital of Sri Lanka, home to the sacred Temple of the Tooth Relic and scenic Kandy Lake.',
        'category': 'Cities',
        'lat': 7.2906, 'lon': 80.6337,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Kandy_lake.jpg/320px-Kandy_lake.jpg',
    },
    'Colombo City': {
        'location': 'Colombo District, Western Province',
        'description': 'Sri Lanka vibrant commercial capital with modern skyscrapers, historic temples, street food, and a busy port.',
        'category': 'Cities',
        'lat': 6.9271, 'lon': 79.8612,
        'rating': '4.4',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Colombo_skyline.jpg/320px-Colombo_skyline.jpg',
    },
    'Dambulla Cave Temple': {
        'location': 'Matale District, Central Province',
        'description': 'A UNESCO World Heritage Site with five stunning cave temples containing over 150 Buddha statues.',
        'category': 'Temples',
        'lat': 7.8567, 'lon': 80.6487,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Dambulla_cave_temple.jpg/320px-Dambulla_cave_temple.jpg',
    },
    'Anuradhapura Ancient City': {
        'location': 'Anuradhapura District, North Central Province',
        'description': 'Sacred ancient city and UNESCO site with colossal stupas, the sacred Bodhi Tree, and 2,500-year-old ruins.',
        'category': 'Heritage',
        'lat': 8.3114, 'lon': 80.4037,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Anuradhapura_Sri_Lanka.jpg/320px-Anuradhapura_Sri_Lanka.jpg',
    },
    'Polonnaruwa Ancient City': {
        'location': 'Polonnaruwa District, North Central Province',
        'description': 'A medieval capital with remarkably well-preserved ruins, statues, and the iconic Gal Vihara rock temple.',
        'category': 'Heritage',
        'lat': 7.9398, 'lon': 81.0004,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Gal_Vihara_02.jpg/320px-Gal_Vihara_02.jpg',
    },
    'Ella Rock': {
        'location': 'Badulla District, Uva Province',
        'description': 'A challenging but rewarding hike through tea estates with panoramic views of the Ella Gap.',
        'category': 'Hills',
        'lat': 6.8667, 'lon': 81.0466,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Nine_Arch_Bridge_Ella.jpg/320px-Nine_Arch_Bridge_Ella.jpg',
    },
    'Nine Arches Bridge': {
        'location': 'Badulla District, Uva Province',
        'description': 'An iconic colonial-era viaduct surrounded by lush tea plantations, best seen with a passing train.',
        'category': 'Heritage',
        'lat': 6.8750, 'lon': 81.0594,
        'rating': '4.8',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Nine_Arch_Bridge_Ella.jpg/320px-Nine_Arch_Bridge_Ella.jpg',
    },
    "Little Adam's Peak": {
        'location': 'Badulla District, Uva Province',
        'description': 'An easy hike with spectacular views of Ella and surrounding valleys, popular at sunrise.',
        'category': 'Hills',
        'lat': 6.8600, 'lon': 81.0450,
        'rating': '4.6',
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
    'Knuckles Mountain Range': {
        'location': 'Kandy District, Central Province',
        'description': 'A UNESCO World Heritage wilderness with misty peaks, rare wildlife, and spectacular trekking routes.',
        'category': 'Hills',
        'lat': 7.4167, 'lon': 80.7833,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Knuckles_mountain_range.jpg/320px-Knuckles_mountain_range.jpg',
    },
    'Horton Plains National Park': {
        'location': 'Nuwara Eliya District, Central Province',
        'description': 'A cloud forest plateau with Worlds End cliff drop, Bakers Falls, and endemic wildlife.',
        'category': 'Hills',
        'lat': 6.8009, 'lon': 80.8076,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Horton_Plains_National_Park.jpg/320px-Horton_Plains_National_Park.jpg',
    },
    'Sinharaja Forest Reserve': {
        'location': 'Ratnapura District, Sabaragamuwa Province',
        'description': 'Sri Lanka last viable area of primary tropical rainforest and a UNESCO World Heritage Site.',
        'category': 'Wildlife',
        'lat': 6.4019, 'lon': 80.4997,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Sinharaja_forest.jpg/320px-Sinharaja_forest.jpg',
    },
    'Kaudulla National Park': {
        'location': 'Polonnaruwa District, North Central Province',
        'description': 'Famous for large elephant gatherings around the Kaudulla reservoir during dry season.',
        'category': 'Wildlife',
        'lat': 8.1667, 'lon': 80.9000,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Minneriya_elephants.jpg/320px-Minneriya_elephants.jpg',
    },
    'Wasgomuwa National Park': {
        'location': 'Matale District, Central Province',
        'description': 'A remote and untouched park with elephants, leopards, and diverse birdlife away from the tourist crowds.',
        'category': 'Wildlife',
        'lat': 7.7333, 'lon': 80.8667,
        'rating': '4.4',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Udawalawe_Elephant.jpg/320px-Udawalawe_Elephant.jpg',
    },
    'Pinnawala Elephant Orphanage': {
        'location': 'Kegalle District, Sabaragamuwa Province',
        'description': 'Home to the worlds largest herd of captive elephants, where orphaned elephants are cared for and bred.',
        'category': 'Wildlife',
        'lat': 7.2994, 'lon': 80.3514,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Pinnawala_Elephant_Orphanage.jpg/320px-Pinnawala_Elephant_Orphanage.jpg',
    },
    'Hikkaduwa Beach': {
        'location': 'Galle District, Southern Province',
        'description': 'A lively beach resort famous for coral reefs, sea turtle sightings, surfing, and vibrant nightlife.',
        'category': 'Beaches',
        'lat': 6.1395, 'lon': 80.1067,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Hikkaduwa_beach.jpg/320px-Hikkaduwa_beach.jpg',
    },
    'Beruwala Beach': {
        'location': 'Kalutara District, Western Province',
        'description': 'One of Sri Lanka oldest resort areas, known for calm waters, luxury hotels, and a historic lighthouse.',
        'category': 'Beaches',
        'lat': 6.4781, 'lon': 79.9822,
        'rating': '4.3',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Bentota_beach.jpg/320px-Bentota_beach.jpg',
    },
    'Weligama Beach': {
        'location': 'Matara District, Southern Province',
        'description': 'Laid-back surf town with gentle waves ideal for beginners, and famous stilt fishermen.',
        'category': 'Beaches',
        'lat': 5.9742, 'lon': 80.4291,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Weligama_beach.jpg/320px-Weligama_beach.jpg',
    },
    'Passikudah Beach': {
        'location': 'Batticaloa District, Eastern Province',
        'description': 'A shallow, calm bay with crystal-clear turquoise waters, ideal for swimming and snorkelling.',
        'category': 'Beaches',
        'lat': 7.9272, 'lon': 81.5567,
        'rating': '4.6',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Passikudah_bay.jpg/320px-Passikudah_bay.jpg',
    },
    'Trincomalee': {
        'location': 'Trincomalee District, Eastern Province',
        'description': 'A stunning natural harbour city with pristine beaches, whale watching, and ancient Hindu temples.',
        'category': 'Beaches',
        'lat': 8.5874, 'lon': 81.2152,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Trincomalee_harbour.jpg/320px-Trincomalee_harbour.jpg',
    },
    'Pidurangala Rock': {
        'location': 'Matale District, Central Province',
        'description': 'A scenic rock near Sigiriya offering the best panoramic view of Sigiriya Rock Fortress at sunrise.',
        'category': 'Heritage',
        'lat': 7.9617, 'lon': 80.7572,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Sigiriya_%28141688197%29.jpeg',
    },
    'Pigeon Island': {
        'location': 'Trincomalee District, Eastern Province',
        'description': 'A marine national park with spectacular coral reefs, blacktip reef sharks, and sea turtles.',
        'category': 'Islands',
        'lat': 8.6167, 'lon': 81.2167,
        'rating': '4.7',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Trincomalee_harbour.jpg/320px-Trincomalee_harbour.jpg',
    },
    'Jaffna': {
        'location': 'Jaffna District, Northern Province',
        'description': 'A culturally rich northern city with unique Tamil heritage, ancient temples, and a historic Dutch fort.',
        'category': 'Cities',
        'lat': 9.6615, 'lon': 80.0255,
        'rating': '4.5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Jaffna_fort.jpg/320px-Jaffna_fort.jpg',
    },
    'Gregory Lake': {
        'location': 'Nuwara Eliya District, Central Province',
        'description': 'A scenic lake in the heart of Nuwara Eliya, popular for boating, cycling, and lakeside walks.',
        'category': 'Hills',
        'lat': 6.9667, 'lon': 80.7833,
        'rating': '4.4',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Nuwara_Eliya.jpg/320px-Nuwara_Eliya.jpg',
    },
    'Pettah Market': {
        'location': 'Colombo District, Western Province',
        'description': 'Colombo bustling bazaar district, a sensory overload of spices, fabrics, electronics, and street food.',
        'category': 'Food',
        'lat': 6.9366, 'lon': 79.8528,
        'rating': '4.3',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Colombo_skyline.jpg/320px-Colombo_skyline.jpg',
    },
    'Galle Face Green': {
        'location': 'Colombo District, Western Province',
        'description': 'A historic ocean-side promenade in Colombo, perfect for evening walks, street food, and sea breezes.',
        'category': 'Cities',
        'lat': 6.9144, 'lon': 79.8478,
        'rating': '4.4',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Colombo_skyline.jpg/320px-Colombo_skyline.jpg',
    },
    'Negombo Fish Market': {
        'location': 'Gampaha District, Western Province',
        'description': 'A vibrant early-morning fish market showcasing Sri Lanka rich fishing culture and fresh seafood.',
        'category': 'Food',
        'lat': 7.2096, 'lon': 79.8361,
        'rating': '4.2',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Negombo_beach.jpg/320px-Negombo_beach.jpg',
    },
}

def get_current_season():
    from datetime import datetime as _dt
    month = _dt.now().month
    # Map to seasons used in training CSV
    if month in [12, 1, 2, 3]:
        return 'December-March'
    elif month in [4, 5]:
        return 'March-May'
    elif month in [6, 7, 8, 9]:
        return 'May-September'
    else:
        return 'November-April'

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