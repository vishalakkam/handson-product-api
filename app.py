from flask import Flask, request, jsonify
import os

app = Flask(__name__)

products = []

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"})

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": data["price"]
    }

    products.append(product)

    return jsonify(product), 201

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    for product in products:
        if product["id"] == product_id:
            data = request.get_json()

            product["name"] = data["name"]
            product["price"] = data["price"]

            return jsonify(product)

    return jsonify({"error": "Product not found"}), 404

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return jsonify({"message": "Product deleted"})

    return jsonify({"error": "Product not found"}), 404


app_port = int(os.getenv("APP_PORT", "8080"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app_port)