from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, URLValidator, EmailValidator
from django.core.exceptions import ValidationError
from datetime import date

class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(
        Group,
        related_name="custom_users",  
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    nama = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._\-]+$',
                message="Nama hanya boleh diisi oleh huruf, angka, dan karakter titik (.), underscore (_), atau strip (-)"
            )
        ]
    )

    password = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(8, message="Password minimal 8 karakter."),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?/~\-]).+$',
                message="Password harus diisi huruf, angka, dan karakter spesial."
            )
        ]
    )

    tanggal_lahir = models.DateField(
        null=False,
        blank=False,
        help_text="Masukkan tanggal lahir"
    )

    nomor_hp = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^62\d{6,13}$',
                message="Nomor HP harus dimulai dengan kode negara 62 diikuti 6 sampai 13 digit angka tanpa simbol apapun"
            )
        ]
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        validators=[EmailValidator(message="Masukkan format email yang valid.")]
    )

    url_blog = models.URLField(
        max_length=255,
        null=False,
        blank=False,
        validators=[URLValidator(message="Masukkan URL yang valid.")]
    )

    deskripsi_diri = models.TextField(
        null=False,
        blank=False,
        validators=[
            MinLengthValidator(5, message="Deskripsi minimal 5 karakter"),
            MaxLengthValidator(1000, message="Deskripsi maksimal 1000 karakter")
        ]
    )

    npwp = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}\.\d{1}-\d{3}\.\d{3}$',
                message="NPWP harus dengan format XX.XXX.XXX.X-XXX.XXX dimana X adalah angka."
            )
        ]
    )

    STATUS_CHOICES = (
        ('Belum', 'Belum'),
        ('Sedang', 'Sedang'),
        ('Diterima', 'Diterima'),
        ('Ditolak', 'Ditolak'),
    )

    status_sertifikasi = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        null=False,
        blank=False
    )

    def clean(self):
        super().clean()

        if self.tanggal_lahir:
            today = date.today()
            age = today.year - self.tanggal_lahir.year - ((today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day))
            if age < 12:
                raise ValidationError({'tanggal_lahir': "Usia minimal 12 tahun."})