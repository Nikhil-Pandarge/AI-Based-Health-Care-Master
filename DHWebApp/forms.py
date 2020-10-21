from django import forms

from crispy_forms.helper import FormHelper

from .models import Hospital

from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML


class HRegisterForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = '__all__'
        widgets = {
            'hregno': forms.TextInput(attrs={'placeholder': 'Hospital Registration number *'}),
            'hname': forms.TextInput(attrs={'placeholder': 'Enter Hospital Name *'}),
            'fname': forms.TextInput(attrs={'placeholder': 'First Name *'}),
            'lname': forms.TextInput(attrs={'placeholder': 'Last Name *'}),
            'gender': forms.Select(),
            'email': forms.TextInput(attrs={'placeholder': 'Email *','type':'email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number *','name':'country_code','pattern':"[1-9]{1}[0-9]{9}"}),
            'adharid':forms.TextInput(attrs={'placeholder': 'Adhar Number *','pattern':"[0-9]{12}"}),
            'contry': forms.Select(attrs={'placeholder': 'Select Country *','id':'country'}),
            'state': forms.Select(attrs={'placeholder': 'Select State *','id':'state'}),
            'district': forms.Select(attrs={'placeholder': 'Select District *','id':'district'}),
            'city': forms.TextInput(attrs={'placeholder': 'Enter City *'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'Enter Zipcode *','type':'tel','pattern':"[0-9]{6}"}),
            # 'Su': forms.TextInput(attrs={'placeholder': 'Enter Zipcode *','type':'tel','pattern':"[0-9]{5-6}"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_enctype = 'multipart/form-data'
        helper.form_class= 'hrform'
        helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                HTML("<h5>Hospital and Owner Info:</h5>"),
                # HTML("<label>Upload Hospital Logo:</label>"),
                Row(
                    Column('hregno','fname','gender','phone',
                        css_class='form-group col-md-6'
                    ),
                    Column('hname','lname','email','adharid',
                        css_class='form-group col-md-6'
                    ),
                     css_class='row' 
                ),
                HTML("<h5>Hospital Address:</h5>"),
                Row(
                    Column('contry','district','zipcode',
                        css_class='form-group col-md-6'
                    ),
                    Column('state','city',
                        css_class='form-group col-md-6'
                    ),
                    css_class='row' 
                ), 
                Submit('submit', 'Register',css_class='btn-primary'),
             css_class='register-form' 
 
            )
        )

class LoginForm(forms.Form):
    profession = forms.CharField(widget=forms.Select(attrs={'placeholder': 'Select Role','id':'role'}))
    hregno = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Hospital Registration Number *'}))
    adharid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Adhar Number *','pattern':"[0-9]{12}"}))
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_class='lform'
        helper.form_show_labels = False
        helper.layout = Layout(
            Div(
                Row(
                    Column('profession',
                        css_class='form-group col-md-7'
                    ),
                    Column('hregno',
                        css_class='form-group col-md-6'
                    ),
                    Column('adharid',
                        css_class='form-group col-md-6'
                    )
                ),
                
                Submit('submit', 'Login',css_class='btn-primary'),
             css_class='register-form' 
 
            )
        )


  