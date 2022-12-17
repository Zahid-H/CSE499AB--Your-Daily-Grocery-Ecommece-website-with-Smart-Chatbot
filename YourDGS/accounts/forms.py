from django import forms
from .models import Account,UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters long"
            )


    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'



class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'pin_code', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

