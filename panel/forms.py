
from django import forms
from django.forms import widgets
from django.contrib.auth.password_validation import validate_password

cidr_choices =  reversed([(x, '/%s' % x) for x in range(33)])
ip_procotol = (
    ('tcp', 'tcp'),
    ('udp', 'udp'),
    ('icmp', 'icmp'),
    # ('58', '58'),
)

class SecurityGroupForm(forms.Form):
    ip_address = forms.CharField()
    port = forms.IntegerField()

    cidr_block = forms.ChoiceField( choices=cidr_choices )
    ip_protocol = forms.ChoiceField( choices=ip_procotol )

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}),validators=[validate_password])
    new_password = forms.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}),validators=[validate_password])
