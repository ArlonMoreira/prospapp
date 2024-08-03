from rest_framework_simplejwt.tokens import RefreshToken
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
