from groq import Groq

API_KEY = "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"

client = Groq(api_key=API_KEY)

def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert HR consultant and resume analyzer.

Analyze the resume below against the job description and return ONLY a JSON response in this exact format:
{{
    "match_score": <number between 0-100>,
    "matched_skills": [<list of skills found in both resume and JD>],
    "missing_skills": [<list of skills in JD but not in resume>],
    "strengths": [<3-4 strong points about this candidate>],
    "improvements": [<3-4 specific suggestions to improve the resume>],
    "summary": "<2-3 sentence overall assessment>"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return ONLY the JSON. No extra text, no markdown, no explanation.
"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    sample_jd = """
    We are looking for a Python Developer with experience in:
    - Python and Django
    - REST APIs
    - PostgreSQL
    - Machine Learning basics
    - Git and version control
    """

    from parser import extract_resume_text
    resume_text = extract_resume_text("c:\\Users\\LENOVO\\Downloads\\Tasmiya Arshad Resume.pdf")

    result = analyze_resume(resume_text, sample_jd)
    print(result)