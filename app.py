from flask import Flask, render_template, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # Instead of 'render_template', use 'render_template_string' if the HTML is directly in the root
    with open('movieSearch.html', 'r') as f:
        html_content = f.read()
    return render_template_string(html_content, name="Selvin")

if __name__ == '__main__':
    app.run(debug=True)
