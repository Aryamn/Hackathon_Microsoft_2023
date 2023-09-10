import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup

# Replace 'YOUR_API_KEY' with your Stack Overflow API key
API_KEY = 'EFTu48nd)ulszUXg4YMOEA(('

# Stack Overflow API endpoints
BASE_URL = f'https://stackoverflow.microsoft.com/api/2.2/questions'

# Specify the tags you are interested in
tags = ['falcon']

# Construct the URL for fetching questions
questions = []

def fetchQuestionsAnswers():
    params = {
    'order': 'desc',
    'sort': 'activity',
    'tagged': ';'.join(tags),
    'filter': 'withbody',  # Include question body
    'key': API_KEY,
    }
    response =  requests.get(BASE_URL,params)
    if response.status_code == 200:
        data = response.json()
    
        for question in data['items']:
            item = {"title": "", "body": "", "id": "", "answer": ""}
            item['title'] = question['title']
            item['body'] = question['body']
            item['id'] = question['question_id']

            # Fetch accepted answer for the question
            params = {
                'order': 'desc',
                'sort': 'votes',
                'site': 'stackoverflow',
                'filter': 'withbody',  # Include answer body
                'key': API_KEY,
            }

            response = requests.get(BASE_URL + f'/{item["id"]}/answers', params=params)
            if response.status_code == 200:
                try:
                    accepted_answer = response.json()['items'][0]
                    item['answer'] = accepted_answer['body']
                except:
                    item['answer'] = 'No answer found'
            else:
                item['answer'] = 'No answer found'

            questions.append(item)

    else:
        print("Failed to fetch questions")

def buildPDF(fileName):
    options = {
    "page-size": "A4",
    "margin-top": "0mm",
    "margin-right": "0mm",
    "margin-bottom": "0mm",
    "margin-left": "0mm",
    }

    pdf_filename = fileName
    document = SimpleDocTemplate(pdf_filename, pagesize=letter)
    content = []
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    body_style = styles['Normal']

    for entry in questions:
        soup = BeautifulSoup(entry['title'], 'html.parser')
        title = soup.get_text()

        soup = BeautifulSoup(entry['body'], 'html.parser')
        question = soup.get_text()

        soup = BeautifulSoup(entry['answer'], 'html.parser')
        answer = soup.get_text()

        # Add title
        title_text = Paragraph(title, title_style)
        content.append(title_text)

        # Add question
        question_text = Paragraph(question, body_style)
        content.append(question_text)

        # Add answer
        answer_text = Paragraph(answer, body_style)
        content.append(answer_text)

    # Build the PDF
    document.build(content)


fetchQuestionsAnswers()
fileName = "questions_and_answers.pdf"
buildPDF(fileName)

