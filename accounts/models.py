from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UsersManager(BaseUserManager):

    # No método create_user, **extra_fields é usado para aceitar campos adicionais que possam ser fornecidos ao criar um usuário. 
    # Isso torna a função mais flexível, permitindo que você passe quaisquer campos extras que o modelo de usuário possa ter, 
    # sem precisar modificá-la toda vez que adicionar um novo campo ao modelo.
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError('E-mail é um campo obrigatório.')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField( #E-mail será o campo principal para autenticação do usuário.
        verbose_name="E-mail",
        unique=True,
        blank=False,
        null=False
    )
    full_name = models.CharField(
        max_length=125,
        verbose_name="Nome completo",
        unique=True,
        blank=False,
        null=False        
    )
    doc_number = models.CharField(
        verbose_name="CPF",
        max_length=11,
        min_length=11,
        unique=True, #Regra não mais implementada: O CPF não pode ser único, pois caso deseja se associar a outra empresa terá que criar outra conta com outro e-mail de acesso.
        blank=False,
        null=False
    )
    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
    )
    is_admin = models.BooleanField(
        verbose_name="Administrador",
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name="Superusuário",
        default=False
    )
    date_joined = models.DateTimeField(
        verbose_name="Data/Cadastro",
        default=timezone.now
    )
    profileImage = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
        default='profiles/default_profile.png'
    )

    objects = UsersManager()

    USERNAME_FIELD = 'email' #No django USERNAME_FIELD é utilizado para identificar qual campo será utilizado como identificador único, nesse caso, USERNAME_FIELD
    REQUIRED_FIELDS = ['doc_number', 'full_name']  #Determinar quais campos são obrigatórios para criar um super usuário.

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
