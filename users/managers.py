from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password= None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email= self.normalize_email(email=email)
        user= self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using= self._db)

        return user
    def create_superuser(self, email, password= None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser'):
            raise ValueError("Super user must have is_superuser= True")
        if not extra_fields.get('is_staff'):
            raise ValueError("Super user must have is_staff= True")
        
        return self.create_user(email, password, **extra_fields)