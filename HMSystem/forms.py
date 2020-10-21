from django import forms
# from django.urls import reverse
import os,json
from crispy_forms.helper import FormHelper

from DHWebApp.models import Hstaff
from .models import Patient
from django.conf import settings
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML, Field
from crispy_forms.bootstrap import InlineCheckboxes
from django.conf import settings
import logging
logger = logging.getLogger("mylogger")
# from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class SRegisterForm(forms.ModelForm):
    class Meta:
        model = Hstaff
        fields = '__all__'
        widgets = {
            'hregno': forms.TextInput(attrs={'placeholder': 'Hospital Registration number *'}),
            'profession':forms.Select(attrs={'id': 'profession'}),
            'degree': forms.Select(attrs={'id':'degree'}),
            'specialization': forms.Select(attrs={'id':'speclzn'}),
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
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        self.helper.form_action = ''
        helper.form_show_labels = False
        self.fields['hregno'].required = False
        self.fields['degree'].required = False
        self.fields['specialization'].required = False
        self.helper.layout = Layout(
            Div(
                HTML("<h5>Hospital and Staff Info.:</h5>"),
                Row(
                    Column('profession',
                        css_class='form-group col-md-8'
                    ),
                    Column('degree','fname','gender','phone',
                        css_class='form-group col-md-6'
                    ),
                    Column('specialization','lname','email','adharid',
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
                Submit('staffRegister', 'Register',css_class='btn-primary'),
             css_class='register-form' 
 
            )
        )

def loadData():
    global chronicsData,allergiesData
    logger.info("load data processing")
    with open(settings.STATIC_ROOT+'/jsonData/chronics.json') as f:
        chrinics_json = json.load(f)
        chronicsData = [(str(chronic["name"]), str(chronic["name"])) for chronic in chrinics_json]

    with open(settings.STATIC_ROOT+'/jsonData/allergies.json') as f:
        allergies_json = json.load(f)
        allergiesData = [(str(allergy["name"]), str(allergy["name"])) for allergy in allergies_json]

class PatientRegisterForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'adharid':forms.TextInput(attrs={'class':'form-control','placeholder': 'Adhar Number *','pattern':"[0-9]{12}",'id':'adharid'}),
            'fname': forms.TextInput(attrs={'class':'form-control','placeholder': 'First Name *','id':'fname'}),
            'lname': forms.TextInput(attrs={'class':'form-control','placeholder': 'Last Name *','id':'lname'}),
            'birthdate': forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Birth date *','id':'dob','type': 'text', 'onfocus': '(this.type="date")', 'oninput':'dobfunction()'}),
            'bloodgrp':forms.Select(attrs={'class':'form-control','placeholder': 'Select Blood Group *','id':'bloodgrp','class':'form-control'}),
            'gender': forms.Select(attrs={'class':'form-control','placeholder': 'Select Gender*','id':'gender'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder': 'Email *','type':'email','id':'email'}),
            'phone': forms.TextInput(attrs={'class':'form-control','placeholder': 'Phone number *','name':'country_code','pattern':"[1-9]{1}[0-9]{9}",'id':'phone'}),
            'country': forms.Select(attrs={'class':'form-control','placeholder': 'Select Country *','id':'country'}),
            'state': forms.Select(attrs={'class':'form-control','placeholder': 'Select State *','id':'state'}),
            'district': forms.Select(attrs={'class':'form-control','id':'district','placeholder': 'Select District *'}),
            'city': forms.TextInput(attrs={'class':'form-control','id':'city','placeholder': 'Enter City *'}),
            'zipcode': forms.TextInput(attrs={'class':'form-control','id':'zipcode','placeholder': 'Enter Zipcode *','type':'tel','pattern':"[0-9]{6}"}),
            'visitcount':forms.TextInput(attrs={'class':'form-control','id':'visno','type': 'text','placeholder': 'Patient Visit count *'}),
            'registeredDate':forms.TextInput(attrs={'class':'form-control','id':'pregdate','type': 'text','placeholder': 'Patient Registration date *'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        loadData()
        self.fields['chronics'] = forms.MultipleChoiceField(choices = chronicsData,widget=forms.SelectMultiple(attrs={'class':'form-control','id':'chronics'}))
        self.fields['allergies'] = forms.MultipleChoiceField(choices = allergiesData,widget=forms.SelectMultiple(attrs={'class':'form-control','id':'allergies'}))
        self.fields['asignDoctor']=forms.CharField(widget=forms.Select(attrs={'class':'asignDoctor'}))
        self.fields['age'] = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'age','placeholder': 'age *',}))
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'regpatient'
        helper.form_show_labels = False
        self.fields['chronics'].label = False
        self.fields['allergies'].label = False
        self.fields['hregno'].required = False
        self.fields['email'].required = False
        self.fields['chronics'].required = False
        self.fields['allergies'].required = False
        self.fields['visitcount'].required = False
        self.fields['registeredDate'].required = False
        self.helper.layout = Layout(
            Div(
                HTML("<h5 class='pdtitile'>Enter Patient Details:</h5>"),
                Row(
                    Column('adharid','fname','bloodgrp','visitcount',
                        css_class='form-group col-md-4'
                    ),
                    Column('email','lname','birthdate','registeredDate',
                        css_class='form-group col-md-4'
                    ),
                    Column('phone','gender','age',
                        css_class='form-group col-md-4'
                    ),
                    Column('asignDoctor',
                        css_class='form-group col-md-5'
                    ),
                     css_class='row' 
                ),
                Div(
                    Row(
                        Column(
                        HTML("<h5>Patient Address:</h5>"),
                        css_class='col-md-10'
                        ),
                        Column('country','city',
                            css_class='form-group col-md-4'
                        ),
                        Column('state','zipcode',
                            css_class='form-group col-md-4'
                        ),
                        Column('district',
                            css_class='form-group col-md-4'
                        ),
                        css_class='row address' 
                    ),
                    Row(
                        Column(
                            HTML("<h5>Select Chronics If Have:</h5>"),
                            InlineCheckboxes('chronics'),
                            css_class='col-md-6'
                        ),
                        Column(
                            HTML("<h5>Select Drug Allergies If Have:</h5>"),
                            InlineCheckboxes('allergies'),
                            css_class='col-md-6'
                        )
                    ),
                    Submit('regPatient', 'Register',css_class='btn-primary',css_id='pregbtn'),
                    css_class='pregisterpop'
                ),
                css_class='register-form' 
            )
        )

class searchPatientForm(forms.Form):
    PSadharid = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Patient Adharid *'}))
    PSphone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Mobile Number *'}))

    def __init__(self, *args, **kwargs):
        super(searchPatientForm,self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_class = 'serchpatient'
        helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                HTML("<h5>Search Patient:</h5>"),
                Row(
                    Column('PSadharid',
                        css_class='form-group col-md-4'
                    ),
                    Column('PSphone',
                        css_class='form-group col-md-4'
                    ),
                    Column(
                         HTML("<button name='searchPatient' class='popOTp d-inline btn btn-primary'><i class='fas fa-search'></i> Search</button>"),
                        css_class='form-group col-md-4'
                    ),
                     css_class='row' 
                ),
                css_class='register-form' 
            )
        )

class OtpForm(forms.Form):
    OTP = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter OTP *'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_class = 'otpform'
        helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                HTML("<h5>OTP SENT to the patients registered mobile number:</h5>"),
                Row(
                    Column('OTP',
                        css_class='form-group col-md-4'
                    ),
                    Column(
                         HTML("<button class='popOTp d-inline btn btn-primary'><i class='fas fa-search'></i> Verify</button>"),
                        css_class='form-group col-md-4'
                    ),
                     css_class='row' 
                ),
                css_class='register-form' 
            )
        )

class assignDoctorForm(forms.Form):
    asignDoctor=forms.CharField(widget=forms.Select(attrs={'class':'asignDoctor form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_class = 'asssignDForm'
        helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                HTML("<h5>Assign Doctor To The Patient:</h5>"),
                Row(
                    Column('asignDoctor',
                        css_class='form-group col-md-6'
                    ),
                    Column(
                         HTML("<button class='assignDbtn d-inline btn btn-primary'> AssignDoctor </button>"),
                        css_class='form-group col-md-4'
                    ),
                     css_class='row' 
                ),
                css_class='register-form' 
            )
        )


class PatientAllergies(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        loadData()
        self.fields['chronics'] = forms.MultipleChoiceField(choices = chronicsData,widget=forms.SelectMultiple(attrs={'class':'form-control','id':'chronics'}))
        self.fields['allergies'] = forms.MultipleChoiceField(choices = allergiesData,widget=forms.SelectMultiple(attrs={'class':'form-control','id':'allergies'}))
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'patientAllr'
        helper.form_show_labels = False
        self.fields['chronics'].label = False
        self.fields['allergies'].label = False
        self.fields['chronics'].required = False
        self.fields['allergies'].required = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column(
                        HTML("<h5>Chronics</h5>"),
                        InlineCheckboxes('chronics'),
                        css_class='form-group col-md-6'
                    ),
                    Column(
                        HTML("<h5>Allergic Drugs</h5>"),
                        InlineCheckboxes('allergies'),
                        css_class='form-group col-md-6'
                    ),
                    css_class='register-form'
                ),
                Submit('regPatient', 'Add Chronic/Allergies',css_class='btn-primary',css_id='paregbtn'),
                )
            )


class AddChronics(forms.Form):
    chronic = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'chrsearch','placeholder':'Search/Add New Chronics *'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'addchrform'
        helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Row(
                    Column('chronic',
                    css_class="form-group col-md-8"
                    ),
                    Column(
                        Submit('submit', 'Add Chronic',css_class='btn-primary',css_id='addChr'),
                        css_class="form-group col-md-4"
                    ),
                    css_class='register-form'
                )
            )
        )

class AddAllergies(forms.Form):
    allergy = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'allrsearch','placeholder':'Search/Add New Allergic Drug *'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'addallrform'
        helper.form_show_labels = False
        self.helper.layout = Layout(
              Div(
                Row(
                    Column('allergy',
                    css_class="form-group col-md-8"
                    ),
                    Column(
                        Submit('submit', 'Add Allergy',css_class='btn-primary',css_id='addAllr'),
                        css_class="form-group col-md-4"
                    ),
                    css_class='register-form'
                )
            )
        )

class AdultCheapComplaint(forms.Form):
    ACheapComplaint = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'acpmlntrsearch','placeholder':'Search/Add New Complaint *'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'ACheapComplaintform'
        helper.form_show_labels = False
        self.helper.layout = Layout(
              Div(
                Row(
                    Column('ACheapComplaint',
                    css_class="form-group col-md-8"
                    ),
                    Column(
                        Submit('submit', 'Add New Complaint',css_class='btn-primary',css_id='AChpCplnt'),
                        css_class="form-group col-md-4"
                    ),
                    css_class='register-form'
                )
            )
        )

class ChildCheapComplaint(forms.Form):
    ChCheapComplaint = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'chcmplntsearch','placeholder':'Search/Add New Complaint *'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'ChCheapComplaintform'
        helper.form_show_labels = False
        self.helper.layout = Layout(
              Div(
                Row(
                    Column('ChCheapComplaint',
                    css_class="form-group col-md-8"
                    ),
                    Column(
                        Submit('submit', 'Add New Complaint',css_class='btn-primary',css_id='ChChpCplnt'),
                        css_class="form-group col-md-4"
                    ),
                    css_class='register-form'
                )
            )
        )
  
class SearchBlog(forms.Form):
    searchblog = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'searchblog','placeholder':'Search Blog Here *'}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'SearchBlog'
        helper.form_show_labels = False
        self.helper.layout = Layout(
              Div(
                Row(
                    Column('searchblog',
                    css_class="form-group col-md-8"
                    ),
                    Column(
                        Submit('submit', 'Search Blog',css_class='btn btn-primary',css_id='searchBlogbtn'),
                        css_class="form-group col-md-4"
                    ),
                    css_class='register-form'
                )
            )
        )

relatives=(('grandparents','grandparents'),
        ('parents','parents'),
        ('aunts','aunts'),
        ('uncles','uncles'),
        ('nieces','nieces'),
        ('nephews','nephews'),
        ('siblings','siblings'),
        ('children','children')
        )
class PatientsfamilyHistory(forms.Form):
    relative = forms.ChoiceField(choices=relatives, widget=forms.Select(attrs={'class':'form-control'}))
    disease = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'fdisease','placeholder':'Enter Major medical conditions and causes of death *'}))
    diseseAge = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'fdisease','placeholder':'Age of disease onset and age at death *'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = self.helper = FormHelper()
        helper.form_method = 'post' # get or post
        helper.form_action = ''
        helper.form_id = 'SearchBlog'
        helper.form_show_labels = False
       
        self.helper.layout = Layout(
              Div(
                Row(
                    Column('relative','diseseAge',
                    css_class="form-group col-md-4"
                    ),
                    Column('disease',
                    css_class="form-group col-md-4"
                    ),
                    Column(
                        Submit('submit', 'Submit',css_class='btn btn-primary',css_id='familyHistorybtn'),
                        css_class="form-group col-md-4"
                    ),
                    css_class='register-form'
                )
            )
        )