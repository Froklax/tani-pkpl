from django import forms
from django.utils.html import strip_tags
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nama', 'password', 'tanggal_lahir', 'nomor_hp', 'email', 'url_blog', 'deskripsi_diri', 'npwp', 'status_sertifikasi']

        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Hanya boleh huruf, angka, dan karakter . _ -'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Minimal 8 karakter dengan huruf, angka, dan karakter spesial'
            }),
            'tanggal_lahir': forms.DateInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'type': 'date'
            }),
            'nomor_hp': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Kode negara 62 diikuti 6 sampai 13 digit angka tanpa simbol'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Harus format email valid'
            }),
            'url_blog': forms.URLInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Harus format url valid'
            }),
            'deskripsi_diri': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'rows': 3,
                'placeholder': 'Masukkan deskripsi diri (min 5, max 1000 karakter)'
            }),
            'npwp': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2',
                'placeholder': 'Format XX.XXX.XXX.X-XXX.XXX (X adalah angka)'
            }),
            'status_sertifikasi': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-black px-3 py-2'
            }),
        }

        labels = {
            'nama': 'Nama Lengkap',
            'password': 'Password',
            'tanggal_lahir': 'Tanggal Lahir',
            'nomor_hp': 'Nomor HP',
            'email': 'Email',
            'url_blog': 'URL Blog',
            'deskripsi_diri': 'Deskripsi Diri',
            'npwp': 'NPWP',
            'status_sertifikasi': 'Status Sertifikasi',
        }

    def clean_nama(self):
        return strip_tags(self.cleaned_data.get('nama'))

    def clean_deskripsi_diri(self):
        return strip_tags(self.cleaned_data.get('deskripsi_diri'))