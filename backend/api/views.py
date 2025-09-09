from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project, Contact
from .serializers import ProjectSerializer, ContactSerializer
from django.shortcuts import render
from django.http import JsonResponse, FileResponse
import os
from .serializers import ContactSerializer
import smtplib
from email.message import EmailMessage


# Function-based view for handling the Project data
@api_view(['GET', 'POST'])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Function-based view for handling a single Project's details
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def contact_list(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()  # Save the contact

            # Prepare email message
            msg = EmailMessage()
            msg['Subject'] = contact.subject  # assuming 'subject' field exists in Contact model
            msg['From'] = contact.email       # the email user gave
            msg['To'] = "pandiyarajans372@gmail.com"  # your email to receive messages

            # Create HTML content using the message field (assuming contact.message exists)
            html_content = f"""
            <html>
            <body>
                <h2>New Contact Message</h2>
                <table border="1" style="border-collapse: collapse;">
                    <tr><th>Email</th><td>{contact.email}</td></tr>
                    <tr><th>Subject</th><td>{contact.subject}</td></tr>
                    <tr><th>Message</th><td>{contact.message}</td></tr>
                </table>
            </body>
            </html>
            """
            msg.add_alternative(html_content, subtype='html')

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                    smtp.login("pandiyarajans372@gmail.com", "chrd luua cwrc kazy")  # Use your Gmail App Password here
                    smtp.send_message(msg)
                print("Email sent successfully.")
            except Exception as e:
                print(f"Failed to send email: {e}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Function-based views for your custom data endpoints
@api_view(['GET'])
def home_data(request):
    data = {
        "name": "Pandiyarajan S",
        "description": "Hi, I'm Pandiyarajan — a passionate software developer who loves to learn and build. I'm always exploring new technologies and looking for opportunities to grow. My goal is to create clean, user-friendly applications that make the internet a better place, one project at a time.",
        "image": "/media/profile.jpg",
        "social_links": {
            "github": "https://github.com/pandiuser",
            "linkedin": "https://www.linkedin.com/in/pandiyarajans/",

        }
    }
    return Response(data)


def about_data(request):
    about_text = (
        "I am a dedicated and results-driven backend developer with over 3 years of experience in building, "
        "designing, and maintaining scalable web applications and RESTful APIs. My expertise lies primarily "
        "in Python and its powerful web frameworks such as Django, Flask, and FastAPI. "
        "Over the years, I’ve worked on projects ranging from enterprise-level certificate lifecycle management "
        "systems to real-time automation tools for network infrastructure. I bring a deep understanding of backend "
        "logic, data modeling, API security, and integration with third-party services. "
        "I'm passionate about writing clean, maintainable code, optimizing application performance, and delivering "
        "production-ready solutions. In addition to Python, I have hands-on experience with Docker, PostgreSQL, "
        "MongoDB, Linux, Shell scripting, and CI/CD pipelines. "
        "Whether it's creating APIs for modern front-end apps, automating repetitive tasks, or managing server-side logic, "
        "I enjoy solving complex problems and turning ideas into working systems. I believe in continuous learning and "
        "always strive to improve my technical and communication skills."
    )

    tech_stack = [
        {"name": "Python", "logo": "/static/tech/python-logo.png"},
        {"name": "Django", "logo": "/static/tech/django-logo.png"},
        # {"name": "FastAPI", "logo": "/static/tech/fastapi-logo.png"},
        {"name": "Flask", "logo": "/static/tech/flask-logo.png"},
        {"name": "React", "logo": "/static/tech/react-logo.png"},
        {"name": "JavaScript", "logo": "/static/tech/javascript-logo.png"},
        {"name": "HTML", "logo": "/static/tech/html-logo.png"},
        {"name": "CSS", "logo": "/static/tech/css-logo.png"},
        {"name": "Docker", "logo": "/static/tech/docker-logo.png"},
        {"name": "Kubernetes", "logo": "/static/tech/kubernetes-logo.png"},
        {"name": "PostgreSQL", "logo": "/static/tech/postgresql-logo.png"},
        {"name": "MongoDB", "logo": "/static/tech/mongodb-logo.png"},
        {"name": "AWS", "logo": "/static/tech/aws-logo.png"},
        {"name": "GIT", "logo": "/static/tech/git-logo.png"},
        {"name": "Linux", "logo": "/static/tech/linux-logo.png"},
        {"name": "JIRA", "logo": "/static/tech/jira-logo.png"},

    ]

    return JsonResponse({
        "about": about_text,
        "tech_stack": tech_stack,
    })


def download_resume(request):
    filepath = os.path.join('static', 'Pandiyarajan.pdf')  # adjust as needed
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='Pandiyarajan_Resume.pdf')


@api_view(['GET'])
def experience_view(request):
    data = [
        {
            "role": "Software Engineer",
            "company": "AppViewx",
            "duration": "Feb 2022 to Apr 2025",
            "description": """• Designed and automated 100+ Python-based workflows for Certificate Lifecycle Management (CLM), including
 certificate discovery, renewal, revocation, and expiry notifications, enhancing performance and reducing manual
 intervention.
 • Built a Django-based internal system for managing enterprise CLM, improving productivity by 67%.
 • Developed a Flask application for automating F5 LTM object creation (virtual servers, pools, nodes, monitors),
 reducing errors and manual workload.
 • Developed automation solutions using Integrated REST APIs with Python (Django/Flask/FastAPI) for various
 automation and monitoring use cases.
 • Created Python-based automation for SSH and API-driven tasks, streamlining internal operations.
 • Designed and developed an internal AppViewX SDK, reducing API call failures and deployment issues.
 • Implemented cross-platform notification workflows (ServiceNow, JIRA, Slack, Teams, PagerDuty, BMC Remedy) to
 simplify PKI and infra structure monitoring.
 • Experienced in working with enterprise customers across global regions, including the US, UK, and Singapore.
 • Built and fine-tuned a conversational AI chatbot using NLP and NER for intelligent query handling.
 • Created automation scripts to handle customer issues and reduce support overhead.
 • Provided real-time technical support during live calls with enterprise clients, ensuring timely resolution."""
        },
        {
            "role": "Software Engineer",
            "company": " Servion Global Solutions",
            "duration": "Apr 2025 to Present",
            "description": """Delivered comprehensive RingCentral RingEX and RingCX deployments by configuring
 Users, Sites, Roles, Templates, Queues, and IVRs, while managing global delivery teams
 across time zones to ensure successful client onboarding, scalable contact center
 operations, and consistent adherence to project timelines, budgets, and quality
 standards."""
        }
    ]
    return Response(data)
