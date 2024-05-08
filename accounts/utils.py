from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def send_order_email(order, pdf_path):
    # Create the email
    email = EmailMessage(
        subject="Order Confirmation",
        body=f"Thank you for your order, {order.user.first_name}. Please find the confirmation attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.email],  # Replace with the user's email address
    )

    # Attach the generated PDF to the email
    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        email.attach("order_confirmation.pdf", pdf_content, "application/pdf")

    # Send the email
    email.send()
