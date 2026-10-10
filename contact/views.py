
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import generics

from .models import ContactMessage
from .serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


class ContactMessageCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        contact = serializer.save()

        subject = f"New Website Inquiry from {contact.name}"

        message = (
            "New inquiry received from The Digital Saathi website.\n\n"
            f"Name: {contact.name}\n"
            f"Email: {contact.email}\n"
            f"Phone: {contact.phone or 'Not provided'}\n"
            f"Service: {contact.service or 'Not specified'}\n\n"
            f"Message:\n{contact.message}"
        )

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_RECEIVER_EMAIL],
                reply_to=[contact.email],
            )
            email.send(fail_silently=False)

        except Exception:
            logger.exception(
                "Email sending failed for contact enquiry ID %s",
                contact.pk,
            )
