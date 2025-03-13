from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password  # make_password-ийг импортлох
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None):
        if not email:
            raise ValueError(_('Танд email заавал шаардлагатай байна.'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number)
        user.set_password(password)  # Нууц үгийг шифрлэх
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None):
        return self.create_user(username, email, phone_number, password)


class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=200)  # Нууц үгийг шифрлэхийн тулд set_password ашиглана
    verify = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Бид email-г хэрэглэгчийн нэр гэж ашиглах болно
    REQUIRED_FIELDS = ['username', 'phone_number']

    def __str__(self):
        return self.email

    def set_password(self, raw_password):
        """Нууц үгийг шифрлэх"""
        self.password = make_password(raw_password)

class Human (models.Model):
    human_ID  = models.BigAutoField(auto_created= True, primary_key= True, serialize= False, verbose_name="ID")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    urgiin_ovog = models.CharField(max_length= 150 )
    ovog = models.CharField(max_length= 150)
    ys_undes = models.CharField(max_length= 150)
    name = models.CharField(max_length= 150)
    RD = models.CharField(max_length= 100, verbose_name = "Регистерийн дугаар", unique=True)
    birth_date = models.DateField()
    birth_counter = models.CharField(max_length= 100)
    birth_year = models .CharField(max_length= 100)
    gender = models.CharField(max_length= 100, choices=[
        ('эрэгтэй', 'Эрэгтэй'),
        ('эмэгтэй', 'Эмэгтэй'),
        ('бусад', 'Бусад')
    ])
    
    def __str__(self):
        return f"{self.name} ({self.RD})"

class Lavlah(models.Model):
    lavlah_ID = models.BigAutoField(auto_created = True, primary_key= True, serialize= False, verbose_name= "ID", unique= True)
    nershil = models.CharField(max_length= 150)

class Who (models.Model):
    who_ID = models.BigAutoField(auto_created= True, primary_key= True, serialize= False, verbose_name= "ID", unique = True)
    human = models.ForeignKey(Human, on_delete = models.CASCADE , related_name="relations")
    relations  = models.ForeignKey(Human , on_delete= models.CASCADE ,related_name= "related_to")
    lavlah = models.CharField(max_length=250)

class LavlahEdu(models.Model):
    lavlahEdu_ID = models.BigAutoField(auto_created= True, primary_key= True, serialize= False, verbose_name= "ID", unique= True)
    nershil = models.CharField(max_length = 120)

class Edu (models.Model):
    edu_ID = models.BigAutoField(auto_created=True, primary_key= True, serialize= False, verbose_name="ID", unique=True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE)
    lavlavEdu = models.ForeignKey(LavlahEdu, on_delete=models.CASCADE)

class School (models.Model):
    school_ID = models.BigAutoField(auto_created = True, primary_key= True, serialize= False, verbose_name= "ID", unique = True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE)
    start_time = models.DateField()
    end_time = models.DateField()
    school_name = models.CharField(max_length=250)

class Mergejil(models.Model):
    mergejil_ID = models.BigAutoField(auto_created= True, primary_key = True, serialize= False, verbose_name = "ID", unique=True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE)
    mergejil = models.CharField(max_length= 250)

class Health(models.Model):
    health_ID = models.BigAutoField(auto_created = True, primary_key= True, serialize= False, verbose_name = "ID", unique= True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE)
    history = models.TextField(null = True, blank=True)
    health_date = models.DateField()

class Marry(models.Model):
    marry_ID = models.BigAutoField(auto_created=True, primary_key=True, serialize= False, verbose_name = "ID", unique= True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE, related_name="marries")
    marryd = models.ForeignKey(Human , on_delete=models.CASCADE, related_name="married_to")
    marry_date = models.DateField()

class Divorce(models.Model):
    divorce_ID = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID" , unique=True)
    human = models.ForeignKey(Human , on_delete= models.CASCADE , related_name="divorces")
    divorced = models.ForeignKey(Human, on_delete= models.CASCADE, related_name="divorced_by")
    divorce_date = models.DateField()
    shaltgaan = models.TextField(null=True, blank= True)

class Death(models.Model):
    death_ID = models.BigAutoField(auto_created=True, primary_key= True, serialize=False, verbose_name="ID", unique=True)
    human = models.ForeignKey(Human , on_delete=models.CASCADE)
    death_time = models.DateField()
    shaltgaan = models.TextField(null = True, blank=True)

class Image(models.Model):
    img_ID = models.BigAutoField(auto_created= True, primary_key= True, serialize=False,verbose_name="ID", unique=True)
    human = models.ForeignKey(Human , on_delete= models.CASCADE)
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    discription = models.CharField(max_length= 250, null = True, blank=True)
    def __str__(self):
        return self.discription


class Shape (models.Model):
    shape_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID", unique=True)
    x = models.FloatField()
    y = models.FloatField()
    type = models.CharField(max_length=10)
    color = models.CharField(max_length=100, blank = True, null=True)
    parent_id = models.IntegerField(null = True, blank = True)
    label= models.CharField(max_length=120, null = True, blank = True)
    human_ID = models.OneToOneField(
        Human, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        unique=True  # 🎯 Давхардахаас сэргийлэх
    )
    is_verified = models.BooleanField(default=False)  # Баталгаажсан эсэхийг тэмдэглэх талбар

    def __str__(self):
        return f"Shape {self.shape_id} at ({self.x}, {self.y})"