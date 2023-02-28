import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        # animal = request.form["animal"]
        position = request.form["position"]
        company = request.form["company"]
        description = request.form["description"]
        experience = request.form["experience"]
        purpose = request.form["purpose"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(position, company, description, experience, purpose),
            temperature=0.25,
            max_tokens = 400,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result) # the response
    return render_template("index.html", result=result)


def generate_prompt(position, company, description, experience, purpose):
#     return """Suggest three names for an animal that is a superhero.

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )
    return """Write me a personalized cover letter for a {position} position at {company}, {description}. 
        Highlight my experience in {experience}. Emphasize my excitement to work at a 
        company that aims to {purpose}. Make it sound human.""".format(
            position = position, company = company, description = description, experience = experience, purpose = purpose)
        # list of experiences, technologies, and skills relevant to job posting