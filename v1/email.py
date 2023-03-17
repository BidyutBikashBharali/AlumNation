# ENV PART
from decouple import config

# PYTHON CORE
import os, sys

# EMAIL PART
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

from fastapi import BackgroundTasks



from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from bson import json_util
from v1.serializers import userResponseEntity, adminResponseEntity
import os, sys, json
from datetime import datetime

from .database import cnct

from . import schema, oauth2, utils

router = APIRouter()






def mass_mailing(email_from, email_to, subject, content):
    try:
        SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
        if SENDGRID_API_KEY is None:
            SENDGRID_API_KEY = config('SENDGRID_API_KEY')

        to_emails = []
        for email in email_to:
            to_emails.append(To(email))
        message = Mail(
            from_email = email_from,
            to_emails = to_emails,
            subject= subject,
            html_content = content,
            is_multiple=True
            )
            
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        
    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)



@router.post('/email')
async def massMailing(email_schma: schema.EmailSchema, background_tasks: BackgroundTasks, admin_id: str = Depends(oauth2.require_admin)):
    try:
        client = cnct.client
        adminData = await client.alumNation_db.admin_collection.find_one({'_id': ObjectId(str(admin_id))})
        if adminData is None:
            return {"status": "No such admin exist!"}
        
        email_schma = dict(email_schma)

        content_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>WELCOME</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
            </head>
            <body>

            <!-- Header -->
            <header class="w3-container w3-teal">
            <h1 class="w3-text-blue">Welcome From Alum-Nation</h1>
            </header>

            <!-- Content -->
            <div class="w3-container">
            <p>Welcome to the latest edition of the W3.CSS Newsletter. In this issue, we'll be highlighting some of the newest features and updates to our CSS framework.</p>
            <p>First up, we've added a new responsive grid system that makes it even easier to create complex layouts for your web pages. With the new grid, you can easily create columns and rows that adjust automatically based on the size of the user's screen.</p>
            <p>We've also updated some of our popular components, like the modal and the slideshow, to include even more customization options. And we've added a bunch of new icons to our icon library, so you can find the perfect icon for your project.</p>
            <p>Finally, we've added some new color themes to our library, so you can easily change the color scheme of your website without having to manually update each element.</p>
            <p>That's all for this edition of the W3.CSS Newsletter. If you have any questions or feedback, feel free to reply to this email and we'll get back to you as soon as possible.</p>
            <p>Thanks for using W3.CSS!</p>
            <p>{email_schma.get("content")}</p>
            </div>

            <!-- Footer -->
            <footer class="w3-container w3-teal">
            <p>&copy; 2023 Alum-Nation</p>
            </footer>

            </body>
            </html>

            """


        background_tasks.add_task(mass_mailing, email_schma.get("email_from"), email_schma.get("email_to"), email_schma.get("subject"), content_html)
        
        return {"status": "success"}
    
    except Exception as emsg:

        subject = "SECURITY ISSUE"
        current_file_name = os.path.basename(__file__)
        line = sys.exc_info()[-1].tb_lineno
        errortype =  type(emsg).__name__
        print("File Name : ", current_file_name)
        print("Error on line : ", line)
        print("error type : ", errortype)
        print("Error msg : ", emsg)