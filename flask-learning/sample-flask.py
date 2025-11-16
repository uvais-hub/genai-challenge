from flask import Flask    # Import the Flask class from the flask package

# Create an instance of the Flask class. This represents your web application.
app = Flask(__name__)

# Define a route for the root URL ('/').
# When a user visits the homepage, this function will be called.
@app.route("/")
def home():
    # Return a simple string as the response for the homepage.
    return "Hello, Flask!"

# This block ensures the app runs only if this file is executed directly, not imported.
if __name__ == "__main__":
    # Start the Flask development server with debug mode enabled.
    app.run(debug=True)