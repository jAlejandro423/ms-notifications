import os
import smtplib
from email.mime.multipart import MIMEMultipart # Multipurpose Internet Mail Extensions
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from dotenv import load_dotenv

#Cargar variables de entorno
load_dotenv()

app = Flask(__name__) #Incializar aplicación de Flask

#Función para enviar los correos electrónicos
def send_email(subject, recipient, body_html):
    email_sender = os.getenv('GoogleMail__EmailSender')
    email_password = os.getenv('GoogleMail__ApiKey')
    smtp_server = os.getenv('GoogleMail__Host')
    smtp_port = os.getenv('GoogleMail__Port')

    print(f"Email sender: {email_sender}")
    print(f"Email password: {email_password}")
    print(f"SMTP server: {smtp_server}")
    print(f"SMTP port: {smtp_port}")

    #Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje en formato HTML
    msg.attach(MIMEText(body_html, 'html'))

    try:
        # Conectar al servidor SMTP de Gmail
        with smtplib.SMTP(smtp_server, int(smtp_port)) as server: #Concetarse al servidor
            server.starttls() # Asegura la conexión
            server.login(email_sender, email_password)
            server. sendmail(email_sender, recipient, msg.as_string())


        return True
    except Exception as e:
        return False, str(e)
    
# Endpoint para enviar el correo

@app.route('/send-email', methods=["POST"])
def send_email_endpoint():
    data = request.json
    subject = data.get('subject')
    recipient = data.get('recipient')
    body_html = '<h1>Welcome to Our Service!</h1>'

    success = send_email(subject, recipient, body_html)
    print(f"Success: {success}")
    if success:
        print('Email sent succesfully!')
        return jsonify({'message': 'Email sent succesfully'})
    else:
        print('Failed to send email')
        return jsonify({'message': 'Failed to sent email'})
    

if __name__ == "__main__":
    app.run(debug=True)

#Prueba de colaborador