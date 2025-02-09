from flask import Flask, request, render_template, jsonify
import spacy
app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")
JOB_ROLES = {
    "Software Engineer": ["python", "flask", "django", "api", "sql", "git"],
    "Data Analyst": ["data analysis", "statistics", "python", "sql", "excel", "power bi"],
    "Frontend Developer": ["html", "css", "javascript", "react", "bootstrap", "figma"],
    "Cybersecurity Analyst": ["network security", "hacking", "penetration testing", "python", "cloud", "aws"],
    "Machine Learning Engineer": ["python", "tensorflow", "pytorch", "nlp", "ai", "deep learning"],
    "UI/UX Designer": ["ui", "ux", "figma", "adobe", "prototyping", "html", "css"]
}
def extract_skills(resume_text):
    doc = nlp(resume_text.lower())
    extracted_skills = set()
    for token in doc:
        for job, skills in JOB_ROLES.items():
            if token.text in skills:
                extracted_skills.add(token.text)
    return list(extracted_skills)
def match_job_role(skills):
    best_match = None
    highest_match = 0
    for job, required_skills in JOB_ROLES.items():
        match_count = len(set(skills) & set(required_skills))
        if match_count > highest_match:
            highest_match = match_count
            best_match = job
    return best_match
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if request.method == 'POST':
        resume_text = request.form['resume_text']
        skills = extract_skills(resume_text)
        best_job_match = match_job_role(skills)
        return jsonify({"skills": skills, "best_match": best_job_match})
if __name__ == '__main__':
    app.run(debug=True)