from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField, DateField, FileField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.widgets import TextArea


class BroadcastForm(FlaskForm):
    # group = SelectField('Group', choices=[('Voters', 'Voters'), ('Candidates','Candidates')])
    group = SelectField('Group', choices=[('TeamScrappy', 'TeamScrappy')])
    message = PasswordField('Message',widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Broadcast')

class Booking(FlaskForm):
    name = StringField('Enter Your Full Name', validators=[DataRequired()])
    phone = StringField('Enter a valid Phone Number', validators=[DataRequired(), Length(min=10, max=10)])
    course = SelectField('Course of Study', choices=[("-Select a course-", "-Select a course-"),("Bachelor of Laws", "Bachelor of Laws"), ("Diploma in Paralegal Studies", "Diploma in Paralegal Studies"), ("Diploma in Law", "Diploma in Law"), ("Bachelor of Science in Economics", "Bachelor of Science in Economics"), ("Bachelor of Science in Agriculture Economics", "Bachelor of Science in Agriculture Economics"), ("Bachelor of Science in Agribusiness", "Bachelor of Science in Agribusiness"), ("Bachelor of Arts in Environment and Development Studies", "Bachelor of Arts in Environment and Development Studies"), ("Bachelor of Arts in Communication Studies", "Bachelor of Arts in Communication Studies"), ("Bachelor of Arts in Theology", "Bachelor of Arts in Theology"), ("Bachelor of Science in Psychology", "Bachelor of Science in Psychology"), ("Bachelor of Arts in Sociology", "Bachelor of Arts in Sociology"), ("Bachelor of Arts in Social Work", "Bachelor of Arts in Social Work"), ("Bachelor of Arts in French", "Bachelor of Arts in French"), ("Bachelor of Science in Management Studies", "Bachelor of Science in Management Studies"), ("Bachelor of Science in Banking and Finance", "Bachelor of Science in Banking and Finance"), ("Bachelor of Science in Business Administration(Marketing)", "Bachelor of Science in Business Administration(Marketing)"), ("Bachelor of Science in Business Administration(HRM)", "Bachelor of Science in Business Administration(HRM)"), ("Bachelor of Science in Business Administration(Finance)", "Bachelor of Science in Business Administration(Finance)"), ("Doctor of Pharmacy", "Doctor of Pharmacy"), ("Bachelor of Architecture", "Bachelor of Architecture"), ("Bachelor of Science in Planning", "Bachelor of Science in Planning"), ("Bachelor of Science in Real Estate", "Bachelor of Science in Real Estate"), ("Bachelor of Science in Graphic Design", "Bachelor of Science in Graphic Design"), ("Bachelor of Science in Fashion Design", "Bachelor of Science in Fashion Design"), ("Bachelor of Science in Landscape Design", "Bachelor of Science in Landscape Design"), ("Bachelor of Science in Interior Design", "Bachelor of Science in Interior Design"), ("Bachelor of Science in Computer Science", "Bachelor of Science in Computer Science"), ("Bachelor of Science in Civil Engineering", "Bachelor of Science in Civil Engineering"), ("Bachelor of Science in Information Technology", "Bachelor of Science in Information Technology"), ("Bachelor of Science in Environmental Engineering", "Bachelor of Science in Environmental Engineering"), ("Bachelor of Science in Nursing", "Bachelor of Science in Nursing"), ("Bachelor of Science in Physician Assistantship", "Bachelor of Science in Physician Assistantship"), ("Bachelor of Science in Public Health", "Bachelor of Science in Public Health"), ("Licensure Exams", "Licensure Exams"), ("ATHE", "ATHE"), ("Diploma", "Diploma")] )
    email = EmailField('Email', validators=[DataRequired()])
    studentId = StringField('Student Id', validators=[DataRequired()])
    # maxOccupancy = SelectField('Select Max Occupancy', choices=[("Terrace", "Terrace"),("Ground Floor", "Ground Floor"), ("First Floor", "First Floor"), ("Second Floor", "Second Floor")], validators=[DataRequired()])

    # relation = StringField('Relationship to emergency contact', validators=[DataRequired()])
    relation = SelectField('Relationship to emergency contact', choices=[("-Select an option-", "-Select an option-"),("Parent", "Parent"), ("Sibling", "Sibling"), ("Family Friend", "Family Friend"), ("Guardian", "Guardian")], validators=[DataRequired()])
    
    # bookingtype = SelectField('Booking Type', choices=[("-Select-", "-Select-"),("Single-Booking", "Single-Booking"), ("Multiple-Booking", "Multiple-Booking")], validators=[DataRequired()])
    # bookingnumber = IntegerField('Number of Bookings', validators=[DataRequired()])
    
    roomlocation = SelectField('Select Room Location', choices=[("-Select a room location-", "-Select a room location-"),("Terrace", "Terrace"),("Ground Floor", "Ground Floor"), ("First Floor", "First Floor"), ("Second Floor", "Second Floor")], validators=[DataRequired()])
    room = SelectField('Select Max. Occupancy', choices=[("-Select how many in a room-", "-Select how many in a room-"),(1,"One in a Room"), (2,"Two in a Room"),(3,"Three in a Room"), (4, "Four in a room")], validators=[DataRequired()])
    size = SelectField('Select Room Size', choices=[("-Select a room size-", "-Select a room size-"),("Small", "Small"),("Large", "Large")], validators=[DataRequired()])
    
    nameOfEmergencyContact = StringField('Name Of Emergency Contact', validators=[DataRequired()])
    emergencyContact = StringField('Emergency Contact', validators=[DataRequired(), Length(min=10, max=10)])
    level = SelectField('Level', choices=[("-Select your current level-", "-Select your current level-"),("100", "100"), ("200", "200"), ("300", "300"),("400", "400"),("500", "500"),("Diploma", "Diploma"),("N/A", "N/A")], validators=[DataRequired()])
    checkin = DateField('Check in Date', format='%Y-%m-%d')
    # special = SelectField('Special Request or Need', choices=[("-Select-", "-Select-"),("Top Bed", "Top Bed"), ("Down Bed", "Down Bed")])

    submit = SubmitField('Choose a room')

class NewRegistration(FlaskForm):
    firstname = StringField('Enter First Name', validators=[DataRequired()])
    lastname = StringField('Enter Last Name', validators=[DataRequired()])
    email = StringField('Enter E-mail', validators=[DataRequired()])
    phone = IntegerField('Enter a valid Phone Number', validators=[DataRequired()])
    studentid = StringField('Enter Student ID')
    course = StringField('Course of Study', validators=[DataRequired()])
    level = IntegerField('Level', validators=[DataRequired()])
    room = SelectField('Select Room', choices=[("-Select how many in a room-", "-Select how many in a room-"),("One in a Room", "One in a Room"), ("Two in a Room", "Two in a Room"), ("Four in a room", "Four in a room")], validators=[DataRequired()])
    checkin = DateField('Arrival Date', format='%Y-%m-%d')
    # special = SelectField('Special Request or Need', choices=[("-Select-", "-Select-"),("Top Floor", "Top Floor"), ("Down Bed", "Down Bed"), ("Ground Floor", "Ground Floor")])
    emergencyname = StringField('Kindly provide an Emergency Contact Name', validators=[DataRequired()])
    emergencyrelationship = StringField('Emergency Relationship', validators=[DataRequired()])
    emergencycontact = IntegerField('Enter Emergency Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PaymentForm(FlaskForm):
    name = StringField('Enter your Full Name', validators=[DataRequired()])
    id = IntegerField('Enter Student ID', validators=[DataRequired()])
    network = SelectField('Select your Network', choices=[("-Select a network provider-","-Select a network provider-"),("MTN","MTN"), ("VODAFONE","VODAFONE"), ("AIRTELTIGO","AIRTELTIGO")], validators=[DataRequired()])
    amountPayable = IntegerField('Amount Due', validators=[DataRequired()])
    amount = IntegerField('Enter how much you want to pay now', validators=[DataRequired()])
    roomNumber = StringField('Room Number', validators=[DataRequired()])
    phone = StringField('Enter Phone Number', validators=[DataRequired()])
    roomlocation = SelectField('Room Location', choices=[("-Select a room location-", "-Select a room location-"),("Terrace", "Terrace"),("Ground Floor", "Ground Floor"), ("First Floor", "First Floor"), ("Second Floor", "Second Floor")], validators=[DataRequired()])
    room = SelectField('Max. Occupancy', choices=[("-Select how many in a room-", "-Select how many in a room-"),(1,"One in a Room"), (2,"Two in a Room"),(3,"Three in a Room"), (4, "Four in a room")], validators=[DataRequired()])
    size = SelectField('Room Size', choices=[("-Select a room size-", "-Select a room size-"),("Small", "Small"),("Large", "Large")], validators=[DataRequired()])
    submit = SubmitField('Pay Now')
    course = SelectField('Course of Study', choices=[("-Select a course-", "-Select a course-"),("Bachelor of Laws", "Bachelor of Laws"), ("Diploma in Paralegal Studies", "Diploma in Paralegal Studies"), ("Diploma in Law", "Diploma in Law"), ("Bachelor of Science in Economics", "Bachelor of Science in Economics"), ("Bachelor of Science in Agriculture Economics", "Bachelor of Science in Agriculture Economics"), ("Bachelor of Science in Agribusiness", "Bachelor of Science in Agribusiness"), ("Bachelor of Arts in Environment and Development Studies", "Bachelor of Arts in Environment and Development Studies"), ("Bachelor of Arts in Communication Studies", "Bachelor of Arts in Communication Studies"), ("Bachelor of Arts in Theology", "Bachelor of Arts in Theology"), ("Bachelor of Science in Psychology", "Bachelor of Science in Psychology"), ("Bachelor of Arts in Sociology", "Bachelor of Arts in Sociology"), ("Bachelor of Arts in Social Work", "Bachelor of Arts in Social Work"), ("Bachelor of Arts in French", "Bachelor of Arts in French"), ("Bachelor of Science in Management Studies", "Bachelor of Science in Management Studies"), ("Bachelor of Science in Banking and Finance", "Bachelor of Science in Banking and Finance"), ("Bachelor of Science in Business Administration(Marketing)", "Bachelor of Science in Business Administration(Marketing)"), ("Bachelor of Science in Business Administration(HRM)", "Bachelor of Science in Business Administration(HRM)"), ("Bachelor of Science in Business Administration(Finance)", "Bachelor of Science in Business Administration(Finance)"), ("Doctor of Pharmacy", "Doctor of Pharmacy"), ("Bachelor of Architecture", "Bachelor of Architecture"), ("Bachelor of Science in Planning", "Bachelor of Science in Planning"), ("Bachelor of Science in Real Estate", "Bachelor of Science in Real Estate"), ("Bachelor of Science in Graphic Design", "Bachelor of Science in Graphic Design"), ("Bachelor of Science in Fashion Design", "Bachelor of Science in Fashion Design"), ("Bachelor of Science in Landscape Design", "Bachelor of Science in Landscape Design"), ("Bachelor of Science in Interior Design", "Bachelor of Science in Interior Design"), ("Bachelor of Science in Computer Science", "Bachelor of Science in Computer Science"), ("Bachelor of Science in Civil Engineering", "Bachelor of Science in Civil Engineering"), ("Bachelor of Science in Information Technology", "Bachelor of Science in Information Technology"), ("Bachelor of Science in Environmental Engineering", "Bachelor of Science in Environmental Engineering"), ("Bachelor of Science in Nursing", "Bachelor of Science in Nursing"), ("Bachelor of Science in Physician Assistantship", "Bachelor of Science in Physician Assistantship"), ("Bachelor of Science in Public Health", "Bachelor of Science in Public Health"), ("Licensure Exams", "Licensure Exams"), ("ATHE", "ATHE"), ("Diploma", "Diploma")] )

class DetailsForm(FlaskForm):
    checkin = DateField('Arrival Date', format='%Y-%m-%d')
    location = SelectField('Room Location', choices=[("-Select-", "-Select-"),("First Floor", "First Floor"), ("Second Floor", "Second Floor"), ("Ground Floor", "Ground Floor")])
    submit = SubmitField('Book Now')
