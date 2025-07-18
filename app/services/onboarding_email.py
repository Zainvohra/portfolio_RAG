from sqlalchemy.orm import Session
from app.models import User
from app.services.emails import send_email

ONBOARDING_TEMPLATES = [
    """Subject: Welcome to the Team!\n\nHi {name},\n\nWelcome to our company! We're excited to have you on board. Please complete your onboarding tasks as soon as possible.\n\nBest,\nThe Team\n""",
    """Subject: Your Onboarding Checklist\n\nHello {name},\n\nHere is your onboarding checklist. Please review and let us know if you have any questions.\n\n- Complete your profile\n- Read the employee handbook\n- Set up your work email\n\nThanks,\nHR Team\n"""
]

class OnboardingEmailService:
    def __init__(self, db: Session):
        self.db = db

    async def send_onboarding_email_to_user(self, user_id: int) -> str:
        user = self.db.query(User).filter(User.id == user_id).first()

        if user is None:
            return f"User with id {user_id} not found."
        
        if getattr(user, 'onboarding_status', None) != "pending":
            return f"User {user_id} onboarding status is not pending. Current status: {getattr(user, 'onboarding_status', None)}"
        
        for template in ONBOARDING_TEMPLATES:
            body = template.format(name=user.name)
            subject = body.split('\n')[0].replace('Subject: ', '')
            await send_email(to=str(user.email), subject=subject, body=body)
        
        setattr(user, 'onboarding_status', 'sent')
        
        self.db.commit()
        
        return f"All onboarding emails sent to user {user_id}."
