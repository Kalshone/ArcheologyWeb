from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import EditorRegistrationCode
from .models import EditorTablePermission

class EditorSignUpForm(UserCreationForm):
    editor_code = forms.CharField(max_length=50, required=True, help_text='Enter the editor registration code')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'editor_code')

    def clean_editor_code(self):
        code = self.cleaned_data.get('editor_code')
        try:
            registration_code = EditorRegistrationCode.objects.get(code=code, is_used=False)
        except EditorRegistrationCode.DoesNotExist:
            raise forms.ValidationError("Invalid or used registration code")
        return code
    
class EditorTablePermissionForm(forms.ModelForm):
    class Meta:
        model = EditorTablePermission
        fields = ['can_add', 'can_edit', 'can_delete']