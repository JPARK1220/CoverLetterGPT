import os

import openai
from flask import Flask, redirect, render_template, request, url_for

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER

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
    text = request.args.get("result")

#     text = """Dear Hiring Manager,

# I am writing to express my interest in the Software Engineer Intern position at COX Automotive. As a passionate software engineer with experience in Python, Flutter, and Dart, I am excited to join a company that is disrupting the car wholesaler industry.

# I have a strong background in software engineering, having worked on projects that involve creating and maintaining web applications, developing mobile applications, and creating software solutions. I am also experienced in developing user interfaces and debugging code. My experience in Python, Flutter, and Dart has enabled me to develop applications that are user-friendly and efficient.

# I am confident that my skills and experience make me an ideal candidate for the Software Engineer Intern position at COX Automotive. I am excited to join a company that is making a real impact in the car wholesaler industry and I am eager to contribute to the success of the company.

# I am confident that I can bring a unique set of skills and experience to the team at COX Automotive and I am excited to learn more about the position. Please feel free to contact me if you have any questions or would like to discuss my qualifications further.

# Thank you for your time and consideration.

# Sincerely,
# [Your Name]"""
    print(text) # the response
    generate_pdf(text)
    # return render_template("index.html", result=text)


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

def generate_pdf(text):
    file_name = "placeholder"
    pdf = Canvas("{}.pdf".format(file_name), pagesize = LETTER)
    pdf.drawString(0, 12, text)
    pdf.save()
    return pdf
