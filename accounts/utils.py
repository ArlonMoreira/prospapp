from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import VerificationCode
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

# from company.models import CompanyPeople
# from django.db.models import F

def get_token_for_user(user):
    refresh_token = RefreshToken.for_user(user)
    # companys = CompanyPeople.objects.filter(user=user, is_joined=True)
    # companys_joined = list(companys.values('company_id', 'role', 'is_joined', 'is_pending')
    #                        .annotate(company=F('company_id')).values('company', 'role', 'is_joined', 'is_pending'))
    
    return {
        'refresh': str(refresh_token),
        'token': str(refresh_token.access_token),
        # 'full_name': user.full_name,
        # 'profileImage': user.profileImage.url,
        # 'companys_joined': companys_joined
    }

def generated_random_code(user):
    numbers = get_random_string(length=6, allowed_chars='0123456789')

    instance = VerificationCode.objects.create(
        user=user,
        code=numbers
    )
    
    instance.save()

    return instance

def send_code_mail(user, code):

    title = 'Seu código de verificação'
    message = f'Seu código de verificação é: {code}'

    send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,        
    )

    
