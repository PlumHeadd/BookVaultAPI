from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Sample data for demonstration
books = []

# Routes
@app.route('/books', methods=['GET'])
def list_books():
    return jsonify(books), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    required_fields = ['title', 'author', 'published_year', 'isbn']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    books.append(data)
    return jsonify(data), 201

@app.route('/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    global books
    books = [book for book in books if book['isbn'] != isbn]
    return jsonify({"message": "Book deleted"}), 200

@app.route('/books/<isbn>', methods=['PUT'])
def update_book(isbn):
    data = request.get_json()
    for book in books:
        if book['isbn'] == isbn:
            book.update(data)
            return jsonify(book), 200

    return jsonify({"error": "Book not found"}), 404

# Serve Swagger YAML
@app.route('/docs/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('docs', 'openapi.yaml')

# Swagger configuration
SWAGGER_URL = '/api-docs'
API_URL = '/docs/openapi.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI endpoint
    API_URL,  # OpenAPI YAML file endpoint
    config={'app_name': "Library Management API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Homepage route
@app.route('/')
def home():
    return "Welcome to the Library Management API! Navigate to /api-docs to explore the API."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)