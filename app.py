import asyncio
import os
from flask import Flask, flash,redirect,url_for,render_template,request, session
import urllib3
from forms import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import httpx
import csv
import requests
import urllib.request, urllib.parse
from datetime import datetime
from werkzeug.utils import secure_filename
import tempfile

from sendsmsasync import send_bulk_sms

app=Flask(__name__)
app.config['SECRET_KEY'] = '5791628basdfsabca32242sdfsfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class RoomConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    number = db.Column(db.Integer(), nullable=True)
    block = db.Column(db.Integer(), nullable=True)
    bedsTaken = db.Column(db.Integer(), nullable=True)
    bedsAvailable = db.Column(db.Integer(), nullable=True)
    location = db.Column(db.String(), nullable=True)
    maxOccupancy = db.Column(db.Integer(), nullable=True)
    size = db.Column(db.String(), nullable=True)
    code = db.Column(db.String(), nullable=True)
    vacant = db.Column(db.Boolean(), default=False)
    price = db.Column(db.Float(), nullable=True)

    def __repr__(self): 
        return f"RoomConfig('{self.name}', Vacant'{self.vacant}', Occupancy- '{self.size}',  Location- '{self.location}',  MaxOccupancy- '{self.bedsAvailable}' )"


class Transactions(db.Model):
    tablename = ['Transactions']

    id = db.Column(db.Integer, primary_key=True)
    occupantId = db.Column(db.String, nullable=False)
    occupantName = db.Column(db.String)
    bookingReference = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)
    roomId = db.Column(db.Integer)
    roomName = db.Column(db.String)
    roomBlock = db.Column(db.Integer)
    account = db.Column(db.String)
    balanceBefore = db.Column(db.Float)
    balanceAfter = db.Column(db.Float)
    prestoTransactionId = db.Column(db.String)
    momoId = db.Column(db.String)
    korbaId = db.Column(db.String)
    network = db.Column(db.String)
    channel = db.Column(db.String)
    paid = db.Column(db.Boolean, default=False)
    pending = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f"Transaction(': {self.id}', 'Amount:{self.amount}', 'Candidate:{self.candidate}', 'Paid:{self.paid}')"


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=True)
    number = db.Column(db.Integer(), nullable=True)
    maxOccupancy = db.Column(db.Integer(), nullable = True)
    occupancyStatus = db.Column(db.String(), nullable = True)
    occupants = db.Column(db.Integer(), nullable = True)
    bedsAvailable = db.Column(db.Integer(), nullable = True)
    floor = db.Column(db.String(), nullable = True)
    tier = db.Column(db.String(), nullable = True)
    price = db.Column(db.Float(), nullable = True)
    roomtype = db.Column(db.String(), nullable = True)
    slots = db.Column(db.Integer(), nullable = True) #BedsTaken
    space = db.Column(db.Boolean(), default=False) #BedAvailable

    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Block('{self.number}', Room('{self.number}', Occupancy- '{self.occupancyStatus}', )"


class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    range = db.Column(db.String(), nullable=True)
    basic = db.Column(db.Float(), nullable=True)
    premium = db.Column(db.Float(), nullable=True)
    space = db.Column(db.Boolean(), default=True)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Room Type('{self.name}', Space('{self.space}', )"

class Blocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    block = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=True)
    paid = db.Column(db.Float(), nullable=True, default=0)
    outstanding = db.Column(db.Float(), nullable=True, default=0)
    due = db.Column(db.Float(), nullable=True, default=0)

    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Blocks ('{self.name}', Space('{self.space}', )"



class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class RoomLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(), nullable=True)
    # user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

def __repr__(self): 
    return f"Room Type('{self.name}', Space('{self.space}' )"

class Occupant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True)
    studentId = db.Column(db.String(), nullable=True)
    balance = db.Column(db.Float(), default=0)
    phone = db.Column(db.String(), nullable=True)
    course = db.Column(db.String(), nullable=True)
    level = db.Column(db.String(), nullable=True)
    room = db.Column(db.String(), nullable=True)
    block = db.Column(db.String(), nullable=True)
    roomnumber = db.Column(db.String(), nullable=True)
    roomid = db.Column(db.String(), nullable=True)
    roomCost = db.Column(db.Float(), nullable=True, default=0)
    amountPaid = db.Column(db.Float(), nullable=True, default=0)
    due = db.Column(db.Float(), nullable=True)
    paid = db.Column(db.Boolean(), default=False)
    status = db.Column(db.String(), nullable=True)

class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    occupantId = db.Column(db.String())
    transactionId = db.Column(db.Integer())
    momoId = db.Column(db.String())
    prestoId = db.Column(db.String())
    provider = db.Column(db.String(), default = "KORBA")
    amount = db.Column(db.Float())
    balanceBefore = db.Column(db.Float())
    balanceAfter = db.Column(db.Float())
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    transactionType = db.Column(db.String(), default="Credit")

def __repr__(self): 
    return f"Ledger('{self.id}', Room('{self.roomnumber}', Paid- '{self.occupancyStatus}', )"


prestoUrl = "https://prestoghana.com"
environment = os.environ["ENVIRONMENT"]
try:
    server = os.environ["SERVER"]
except Exception as e:
    app.logger.error("Couldnt find server!")
    app.logger.error(e)
    server = "FALSE"


@app.route('/roomtype', methods=['GET', 'POST'])
def roomtype():
    roomtype = RoomType.query.all()
    return render_template('roomtype.html', roomtype=roomtype)

# @app.route('/blocks/<string:roomtype>', methods=['GET', 'POST'])
# def blocks(roomtype):
#     print(roomtype)
#     roomtype = RoomLocation.query.all()
#     return render_template('location.html', roomtype=roomtype)

@app.route('/location/<string:roomtype>/<string:tier>', methods=['GET', 'POST'])
def location(roomtype, tier):
    print(roomtype)
    session["roomtype"] = roomtype
    session["roomtier"] = tier
    roomtype = RoomLocation.query.all()
    return render_template('location.html', roomtype=roomtype)

@app.route('/rooms/<string:id>', methods=['GET', 'POST'])
def rooms(id):
    block = id

    session["roomlocation"] = id

    floor = RoomLocation.query.get_or_404(id)

    print("floor")
    floor = floor.location

    roomtype = session['roomtype']
    print(roomtype)

    # allrooms = Room.query.filter_by(block=block).order_by(Room.number.asc()).all()
    allrooms = Room.query.filter_by(maxOccupancy = roomtype, floor= floor, price=session["roomtier"], space=False).all()
    # allrooms = Room.query.all()
    print(allrooms)
    return render_template('rooms.html', rooms=allrooms, block=block)


@app.route('/roomselector/<int:id>', methods=['GET', 'POST'])
def roomselector(id):
    # Find occupant
    occupant = Occupant.query.get_or_404(id)
    print(occupant)

    location = session["location"]
    size = session["size"]
    room = session["room"]
# location=location, maxOccupancy=room, size=size
    # allrooms = Room.query.filter_by(block=block).order_by(Room.number.asc()).all()
    allrooms = RoomConfig.query.filter_by(vacant=True, location=location, size=size, bedsAvailable=room).all()
    # allrooms = Room.query.all()
    print(allrooms)
    return render_template('rooms.html', rooms=allrooms, block=block)

# NEW
@app.route('/updateRoomData', methods=['GET', 'POST'])
def updateRoomData():
    roomconfig = RoomConfig.query.all()
    for room in roomconfig:
        if room.bedsTaken < room.bedsAvailable:
            room.vacant = True
        db.session.commit()
    return "Done"


@app.route('/allrooms/<string:id>', methods=['GET', 'POST'])
def allrooms(id):
    block = id
    session["roomlocation"] = id
    allrooms = Room.query.filter_by(block=block).all()
    print(allrooms)
    return render_template('allrooms.html', rooms=allrooms, block=block)


@app.route('/admin/rooms/<string:option>', methods=['GET', 'POST'])
def adminallrooms(option):
    if option == 'all':
        allrooms = RoomConfig.query.all()
    elif option == 'vacant':
        allrooms = RoomConfig.query.filter_by(vacant = True).all()
    elif option == 'taken':
        allrooms = RoomConfig.query.filter_by(vacant = False).all()
    else:
        allrooms = RoomConfig.query.all()

    print(allrooms)
    return render_template('allrooms.html', rooms=allrooms)


@app.route('/admin/occupants/<string:option>', methods=['GET', 'POST'])
def adminalloccupants(option):
    if option == 'reserved':
        all = Occupant.query.filter_by(status = "reserved").all()
    print(all)

    return render_template('occupants.html', alloccupants=all)




@app.route('/blocks', methods=['GET', 'POST'])
def block():
    allbocks = Blocks.query.all()
    return render_template('blocks.html', blocks = allbocks)

@app.route('/occupants', methods=['GET', 'POST'])
def occupants():
    alloccupants = Occupant.query.order_by(Occupant.id.desc()).all()
    return render_template("occupants.html", alloccupants = alloccupants)

def send_sms(phone,message, senderId):
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":senderId}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    print(url)


def sendsms(phone,message):
    url = "https://unify-base.rancard.com/api/v2/sms/public/sendMessage"
    message = {
        "apiKey": "dGFsYW5rdTpUYWxhbmt1Q3U6MTY1OkFQSWtkczAxNDI0Nzg1NDU=",
        "contacts": [phone],
        "message": message + "\n\nPowered By PrestoGhana.",
        "scheduled": False,
        "hasPlaceholders": False,
        "senderId": "Pronto"
    }
    r = requests.post(url, json=message)
    print(r.text)
    return r.text

# NEW
@app.route('/form',methods=['GET','POST'])
def pronto():
    form=Booking()

    if request.method=='POST':
        if form.validate_on_submit():
            newOccupant = Occupant(
                name = form.name.data,
                phone = form.phone.data,
                studentId = form.studentId.data,
                course = form.course.data,
                level = form.level.data
            )

            db.session.add(newOccupant)
            db.session.commit()
            session['occupantId'] = newOccupant.id
            session['location'] = form.roomlocation.data
            session['room'] = form.room.data
            session['size'] = form.size.data

            print(session)

            sendTelegram("New Occupant Created!: \nOccupant: " + str(newOccupant.id )+". "+newOccupant.name + "\nStudentId: " + newOccupant.studentId + "\nCourse: " + newOccupant.course + "\nLevel: " + newOccupant.level )
        
            return redirect(url_for('roomselector', id=newOccupant.id))
        
        else:
            print(form.errors)
        return render_template('pronto.html', form=form)
    return render_template('pronto.html', form=form)


# @app.route('/extractDatacsv', methods=['GET', 'POST'])
# def extractDatacsv():
#     with open('/Users/kweku/Documents/Projects/html/pronto/instance/RoomConfig.csv', newline='') as csvfile:
#         csv_reader = csv.DictReader(csvfile)

#         csvData = []

#         for r in RoomConfig.query.all():
#             db.session.delete(r)
#             db.session.commit()


#         for row in csv_reader:
#             print(row)
#             csvData.append(row)
#             # newRoomConfig = RoomConfig(block=row["BLOCK"], floor=row["FLOOR"], number=row["ROOM_NUMBER"], roomtype=row["ROOM_TYPE"], maxOccupancy=row["MAX_OCCUPANCY"], occupants=row["OCCUPANTS"], price=row["PRICE"], bedsAvailable=row["MAX_OCCUPANCY"], tier = row["TIER"], space=True )
#             newRoomConfig = RoomConfig(name=row["Block/Room"], code=row["code"], bedsTaken=row["bedsTaken"], block=row["block"], number=row["room"], bedsAvailable=row["bedsAvailable"], location=row["roomLocation"], maxOccupancy = row["maxOccupancy"], size=row["size"], vacant=bool(["vacant"]), price=int(["price"]) )
#             db.session.add(newRoomConfig)
        
#         db.session.commit()

#         return csvData
    
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Check if the post request has the file part
#         if 'file' not in request.files:
#             return 'No file part in the request'
        
#         file = request.files['file']
        
#         # Check if a file was selected
#         if file.filename == '':
#             return 'No file selected'

#         filename = 'RoomConfig.csv'

#         # Save file with new name
#         file.save(os.path.join(app.instance_path, filename))


#         # Process the uploaded file (in this example, simply save it)
#         file.save(file.filename)
        
#         return 'File uploaded successfully'
    
#     return render_template('uploadexcel.html')

def remove_bom(csv_data):
    if csv_data.startswith('\ufeff'):
        return csv_data[1:]
    return csv_data


@app.route("/broadcast", methods=['GET','POST'])
def broadcast():
    form = BroadcastForm()

    # contacts = "fetchVoters(award.slug)"
    contacts = "data"
    # numberOfContacts = len(contacts)
    file_path = None

    app.logger.info(session)

    loadingMessage = "Broadcasting message to " + str("numberOfContacts") + " contacts, this might take a while😭"
    if request.method == 'POST':
        if 'file' in request.files:
            
            file = request.files['file']
            
            # Check if a file was selected
            if file.filename == '':
                return 'No file selected'

            # Save the file to a secure temporary location
            filename = file.filename
            file_path = os.path.join(app.instance_path, filename)
            print(file_path)
            file.save(file_path)

            with open(file_path, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                
                csvData = []

                for row in csv_reader:
                    print(row)
                    csvData.append(row["phoneNumber"])

                total = len(csvData)
                filtered = list(dict.fromkeys(csvData))
                unique = len(filtered)

                print("Total " + str(total) + " - Unique " + str(unique))
                contacts = filtered
                
                app.logger.info(session)
                app.logger.info("form.csrf_token.data")
                app.logger.info(form.csrf_token.data)
                message = form.message.data
                message += "\n \nPowered By PrestoGhana"
                app.logger.info(message)

                # for contact in contacts:
                #     send_sms(contact, message, form.group.data)
          
                # List of recipients
                recipients = contacts

                # Run the event loop
                asyncio.run(send_bulk_sms(recipients, message, form.group.data ))
                # try:
                #     loop = asyncio.get_event_loop()
                #     loop.close()
                # except Exception as e:
                #     print(e)

                flash('You have successfully sent ' + str(unique) + ' messages.')
                return redirect(url_for('broadcast'))

    return render_template('broadcast.html',  contacts=contacts, numberOfContacts=0, form=form, loadingMessage=loadingMessage)



@app.route('/upload/<string:field>', methods=['GET', 'POST'])
def upload_csv(field):
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part in the request'
        
        file = request.files['file']
        
        # Check if a file was selected
        if file.filename == '':
            return 'No file selected'

        # Save the file to a secure temporary location
        filename = file.filename
        file_path = os.path.join(app.instance_path, filename)
        print(file_path)
        file.save(file_path)

        if field == "rooms":
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)

                csvData = []

                for r in RoomConfig.query.all():
                    db.session.delete(r)
                    db.session.commit()

                for row in csv_reader:
                    print("------row------")
                    print(row)
                    print("------end------")
                    csvData.append(row)
                    print(row["price"])
                    price = row["price"]
                    float(price)

                    newRoomConfig = RoomConfig(name=row["Block/Room"], code=row["code"], bedsTaken=row["bedsTaken"], block=row["block"], number=row["room"], bedsAvailable=row["bedsRemaining"], location=row["roomLocation"], maxOccupancy = row["bedsAvailable"], size=row["size"], price=price )
                    db.session.add(newRoomConfig)
                
                db.session.commit()

                roomdatastatus = updateRoomData()
                print(roomdatastatus)

                return csvData
            
        elif field == "courses":
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                
                csvData = []

                for row in csv_reader:
                    print(row)
                    newCourses = Courses(name=remove_bom(row["Course"]) )
                    db.session.add(newCourses)
                
                db.session.commit()

                return csvData
        elif field == "sms":
            with open(file_path, newline='') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                
                csvData = []

                for row in csv_reader:
                    print(row)
                    csvData.append(row["phoneNumber"])

                total = len(csvData)
                filtered = list(dict.fromkeys(csvData))
                unique = len(filtered)

                print("Total " + str(total) + " - Unique " + str(unique))
                return broadcast(filtered)
                # return redirect(url_for('broadcast', data=filtered))
        else:
            return 404
    
    return render_template('uploadexcel.html')


@app.route('/extractroomtypecsv', methods=['GET', 'POST'])
def extractroomtypecsv():
    with open('Documents/ROOM_TYPE.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csvData = []

        for row in csv_reader:
            print(row)
            csvData.append(row)
            newRoom = RoomType(name=row["ROOM_TYPE"], range=row["PRICE_RANGE"], basic=row["BASIC"], premium=row["PREMIUM"] )
            db.session.add(newRoom)
        
        db.session.commit()

        return csvData
    


@app.route('/extractroomlocationcsv', methods=['GET', 'POST'])
def extractroomlocationcsv():
    with open('Documents/ROOM_LOCATION.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        csvData = []

        for row in csv_reader:
            print(row)
            csvData.append(row)
            newRoom = RoomLocation(floor=row["FLOOR"], location=row["ROOM_LOCATION"])
            db.session.add(newRoom)
        
        db.session.commit()

        return csvData
    

    
@app.route('/route_name', methods=['GET', 'POST'])
def extractCsv(filename):
     with open(filename, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            number = line['number']

            id = id.split('-')[0]
            if status == 'paid' and len(id) <= 3:
                amount = line['amount']

                print(str(id) + " - " + amount)
            
                # find candidate and add amount to votes ... 
                candidate = Candidates.query.get_or_404(id)
                candidate.votes += float(amount)
                print(str(id) + " - " + amount)

        db.session.commit()
        all = []
        candidates = Candidates.query.all()
        for candidate in candidates:
            candidate = {
                candidate.name:candidate.votes
            }
            all.append(candidate) 
        return make_response(all)




@app.route('/new',methods=['GET','POST'])
def new():
    form=NewRegistration()
    if request.method=='POST':
        # Handle POST Request here
        return render_template('new.html')
    return render_template('new.html', form=form)


@app.route('/payment/<string:id>', methods=['GET', 'POST'])
def payment(id):
    form=PaymentForm()
    print(id)
    session["roomnumber"] = id
    room = RoomConfig.query.get_or_404(id)
    form.roomNumber.data = room.name
    occupant = Occupant.query.get_or_404(session['occupantId'])

    try:
        occupant.roomCost = float(room.price)
        occupant.roomid = room.id
        db.session.commit()
    except Exception as e:  
        print(e)

        # TODO: ACCEPT URL PARAMS

    if request.method == 'POST':
        if form.validate_on_submit:
            print("validated")
            baseUrl = "https://sandbox.prestoghana.com"
            paymentUrl = "https://sandbox.prestoghana.com/korba"
            min = float(room.price)*0.75
            if form.amount.data == None:
                form.amount.data = min
                # name, occupantid, roomid, indexnumber

            concatenationbookingreference = str(occupant.id)+occupant.name+room.name
            
            transaction = Transactions(
                occupantId = occupant.id,
                occupantName = occupant.name,
                amount = form.amount.data, 
                roomId = room.id,
                roomName = room.name,
                roomBlock = room.block,
                account = occupant.phone,
                balanceBefore = occupant.balance,
                bookingReference = concatenationbookingreference
                )
            
            try:
                db.session.add(transaction)
                db.session.commit()
            except Exception as e:
                sendTelegram("Couldnt transaction!!! FOLLOW UP IN LOGS.")
                # return redirect()
            
            return redirect(paymentUrl+'/pay/prontohostel?amount='+form.amount.data+'?name='+form.name.data+'?reference='+concatenationbookingreference)

        # handle transactions here.


    #         paymentInfo = {
    #                 "appId":"prontohostel",
    #                 "ref":form.name.data,
    #                 "reference":str(form.id.data),
    #                 "description":str(form.id.data),
    #                 "paymentId":form.id.data, 
    #                 "phone":"0"+str(form.phone.data[-9:]),
    #                 "amount":form.amount.data,
    #                 "total":str(form.amount.data), #TODO:CHANGE THIS!
    #                 "recipient":"external", #TODO:Change!
    #                 "percentage":"5",
    #                 "callbackUrl":baseUrl+"/notify/",#TODO: UPDATE THIS VALUE
    #                 "firstName":form.name.data,
    #                 "network":form.network.data,
    #             }
     
    #         r = httpx.post(paymentUrl, json=paymentInfo)
    #         print(r)

    #         # sendsms(str(paymentInfo["paymentId"]), paymentInfo["firstName"],paymentInfo["description"], "web", paymentInfo["phone"], )
    #         updateOccupant(paymentInfo["amount"], occupant)
    #         return "Done!"
    #     else:
    #         print(form.errors)
            
    else:
        room = RoomConfig.query.get_or_404(id)
        print(room.price)
        min = float(room.price)
        #min = float(room.price)*0.75
        print("This is a get request")

        occupant = Occupant.query.get_or_404(session["occupantId"])
        occupant.room = room.number
        occupant.block = room.block
        db.session.commit()

        form.id.data = occupant.studentId
        form.name.data = occupant.name
        form.phone.data = occupant.phone
        form.amount.data = min
        form.roomNumber.data = room.name

        # form.roomNumber.data ="Block " + room.block +" Room " +str(room.number)
    return render_template('payment.html', form=form, occupant=occupant, minAmount=min, maxAmount=room.price)



def confirmPrestoPayment(transaction):
    r = requests.get(prestoUrl + '/verifykorbapayment/'+transaction.ref).json()
    
    print(r)
    print("--------------status--------------")
    status = r.get("status")
    print(status)

    if status == 'success' or environment == 'DEV' and server == "FALSE":

        print("Attempting to update transctionId: " +str(transaction.id) + " to paid! in " + environment + "environment || SERVER:" + server)

        # findtrasaction, again because of the lag.
        state = Transactions.query.get_or_404(transaction.id)
        if state.paid != True:
            try:
                state.paid = True
                state.pending = False
                db.session.commit()
                print("Transaction : "+str(transaction.id) + " has been updated to paid!")

            except Exception as e:
                app.logger.info("Failed to update transctionId: "+str(transaction.id )+ " to paid!")
                app.logger.error(e)
                sendTelegram(e)

            return True
        return False

    else:
        print(str(transaction.id) + " has failed.")
        return False
    
def createLedgerCredit(transaction):
    # find vote with same transaction id.
    alreadyCounted = Ledger.query.filter_by(transactionId = transaction.id).first()
    if alreadyCounted != None: #If found.
        return None

    # try: #Create a new ledger entry
    #     newVote = Votes(candidateId=transaction.candidate, name=transaction.candidateName, award = transaction.award, costPerVote=transaction.costPerVote, votes = transaction.votes, transactionId=transaction.id)
    #     db.session.add(newVote)
    #     db.session.commit()
    # except Exception as e:
    #     app.logger.error(e)
    #     votingAlert(str(e))
    #     app.logger.error("Couldnt create vote for " + transaction.candidateName)

    # try: #Attatch vote to candidate
    #     candidate = Candidates.query.get_or_404(int(transaction.candidate))
        
    #     transaction.votesBefore = candidate.votes
    #     transaction.votesAfter = candidate.votes + newVote.votes

    #     app.logger.info("----------------------- Updating votes ---------------------------")
    #     app.logger.info("Attempting to update " + candidate.name + " votes from " + str(transaction.votesBefore) + " to " + str(transaction.votesAfter))
    #     votingAlert("Attempting to update " + candidate.name + " votes from " + str(transaction.votesBefore) + " to " + str(transaction.votesAfter))
        
    #     candidate.votes += newVote.votes
    #     transaction.voteId = newVote.id

    #     db.session.commit()

    #     app.logger.info("----------------------- Updated Successfully! ---------------------------")

    # except Exception as e:
    #     app.logger.error("Updating candidate " + candidate.name + " votes has failed." )
    #     app.logger.error(e)
    #     votingAlert(str(e))

    return "Pending Ledger Logic"


@app.route('/confirm/<string:transactionId>', methods=['GET', 'POST'])
def confirm(transactionId):
    message = "In Progress"

    transaction = Transactions.query.get_or_404(transactionId)
    occupant = Occupant.query.get_or_404(transaction.occupantId)
    room = RoomConfig.query.get_or_404(transaction.roomId)
    
    print("Attempting to confirm transaction: \n TransactionId: " + transaction.id + "\nOccupant: " + occupant.id + ". " + occupant.name + "\nRoom: "+ room.name)

    if transaction.paid == False:
        message = "Failed Transaction"
        if confirmPrestoPayment(transaction) == True:

            message = "Duplicate"
            # CREATE A CREDIT TO AN OCCUPANT.
            credit = createLedgerCredit(transaction)
            if credit != None: #If a credit was already created
                updateOccupant(transaction.amount, transaction.occupantId, "paid")
            else:
                app.logger.error("Transaction: " + str(transaction.id) + " was attempting to be recreated.")
        else:
            message = "This transaction has either failed or is being processed. Please check or try again."

    responseBody = {
        "message":message,
        "transactionId":transaction.id,
        "prestoTransactionId":transaction.ref,
        "paid":transaction.paid
    }
    print(responseBody)
    return responseBody



@app.route('/reserve/<int:id>', methods=['GET', 'POST'])
def reserve(id):
    occupant = Occupant.query.get(id)
    occupant.status = "reserved"
    db.session.commit()

    updateOccupant(0, occupant, "reserved")

    flash(f'Block '+ occupant.block +' '+ 'Room ' + occupant.room +' has been reserved for ' + occupant.name  )
    return redirect(url_for('home'))


# confirm route!
# if transaction is paid once!
def updateOccupant(amount, occupant, action="paid"):
    amountBalance = occupant.roomCost - float(amount) #6000 - 3000 = 3000
    
    # update block 
    block = Blocks.query.get_or_404(occupant.block) #find Block
    block.paid += amount #Update amount paid per block

    # Current balance + amount paid
    occupant.amountPaid += amount
    occupant.due = amountBalance #wrong
    outstanding = occupant.roomCost - amount
    
    block.due += occupant.roomCost
    block.outstanding += outstanding

    # set room to hidden if full
    room =  RoomConfig.query.get_or_404(occupant.roomid)
    room.bedsTaken += 1
    room.bedsAvailable -= 1
    
    db.session.commit()

    if action == "reserved":
        message = "You have successfully reserved "+ str(room.name) +". Please make a payment of no less than GHS 1000 by the 30th of July 2023 to confirm your reservation."
        sendTelegram("RESERVATION: \nBlock " + str(room.block)+ " Room " + str(room.number) + "has been "+ action +" successfully by "+ str(occupant.name)+ " " + str(occupant.phone)+ ".\nAmount Paid "+ str(amount) + "\nRemaining Beds: "+ str(room.bedsAvailable))
    
    elif action == "purchase":
        message = "Receipt Number:" + occupant.phone + "\n Date: "+ datetime.utcnow().strftime('%c') + "\nGuest Name:" + occupant.name + "\nBooking Reference: " + transaction + "\nPayment Method: " + paymentMethod + "\nReview occupancy terms and conditions here. \nDial *192*456*908# and use your booking reference to make future payments during your occupancy term. \nThank you for choosing Pronto Hostels. We hope you have a great stay with us!"

        sendTelegram("PURCHASE: \nBlock " + str(room.block)+ " Room " + str(room.number) + "has been "+ action +" successfully by "+ str(occupant.name)+ " " + str(occupant.phone)+ ".\nAmount Paid "+ str(amount) + "\nRemaining Beds: "+ str(room.bedsAvailable))
    
    # TRY CATCH FOR EACH!
    sendsms(occupant.phone, message)
    # sendTelegram("Block " + str(room.block)+ " Room " + str(room.number) + "has been "+ action +" successfully by "+ str(occupant.name)+ " " + str(occupant.phone)+ ".\nAmount Paid "+ str(amount) + "\nRemaining Beds: "+ str(room.bedsAvailable))

    if room.bedsAvailable <= 0:
        room.vacant = False
        db.session.commit()
        sendTelegram("Block " + str(room.block)+ " Room " + str(room.number) + " is no more vacant")

    return occupant
# -------------- ADMIN -----------

@app.route('/resetDashboard', methods=['GET', 'POST'])
def resetDashboard():
    for b in Blocks.query.all():
        b.paid = 0
        b.outstanding = 0
        b.due = 0
    
    for o in Occupant.query.all():
        db.session.delete(o)

    db.session.commit()

    return "Done!"

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    occupants = Occupant.query.all()
    totalOccupants = Occupant.query.count()
    paid = 0
    due = 0
    for o in occupants:
        if o.amountPaid:
            paid +=  o.amountPaid 
        if o.due:
            due += o.roomCost
    
    totalNumberOfBeds = 0

    for r in Room.query.all():
        totalNumberOfBeds += r.maxOccupancy

    availableBeds = totalNumberOfBeds-totalOccupants
    occupancyRate = totalNumberOfBeds/availableBeds

    print("totalNumberOfBeds:" + str(totalNumberOfBeds))
    print("availableBeds:" + str(availableBeds))
    # print("totalNumberOfBeds:" + totalNumberOfBeds)

    occupancyRate = round(occupancyRate/100, 2)
    amountOutstanding =  due - paid

    # for bed in beds:


    
    return render_template('dashboard.html', occupancyRate=str(occupancyRate)+"%",outstanding=amountOutstanding, paid=paid, due=due, tenants="6000")

@app.route('/allblocks/<string:id>', methods=['GET', 'POST'])
@app.route('/allblocks', methods=['GET', 'POST'])
def allblocks(id="0"):
    print(id)
    blocks = Blocks.query.all()
    filterDict = {
        "0":"All",
        "1":"outstanding",
        "2":"due",
        "3":"paid"
    }
    print(filterDict[id])
    return render_template('allblocks.html', blocks=blocks, filter=filterDict[id])

@app.route('/adminblock/<int:id>', methods=['GET', 'POST'])
def adminblock(id):
    occupants = Occupant.query.filter_by(block = id).all()
    print(occupants)
    return render_template('adminoccupants.html', alloccupants=occupants)

@app.route('/master', methods=['GET', 'POST'])
def master():

    return render_template('master.html')


@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('home.html')

@app.route('/details', methods=['GET', 'POST'])
def details():
    form=DetailsForm()
    if request.method=='POST':
        # Handle POST Request here
        return render_template('details.html')
    return render_template('details.html', form=form)

@app.route('/viewrooms', methods=['GET', 'POST'])
def viewrooms():

    return render_template('viewrooms.html')

# @app.route('/sendTelegram', methods=['GET', 'POST'])
def sendTelegram(params):
    url = "https://api.telegram.org/bot5873073506:AAGRf5b4sjmEzDUbApytx4lKoew_WbdrGsA/sendMessage?chat_id=-839615923&text=" + urllib.parse.quote(params)
    content = urllib.request.urlopen(url).read()
    print(content)
    return content

# @app.route('/sendsms', methods=['GET', 'POST'])

    r = sendsms(phone,message)
    print(r)
    return "r"

# @app.route('/route_name', methods=['GET', 'POST'])
# def method_name():
#        paymentInfo = {
#             "appId":"pronto",
#             "ref":payment.ref,
#             "reference":payment.ref,
#             "paymentId":payment.id, 
#             "phone":"0"+payment.account[-9:],
#             "amount":payment.amount,
#             "total":payment.total,
#             "recipient":"payment", #TODO:Change!
#             "percentage":"3",
#             "callbackUrl":prestoHerokuUrl+"prontoconfirm/"+str(payment.id),#TODO: UPDATE THIS VALUE
#             "firstName":payment.account,
#             "network":mobileNetwork,
#         }

#     r = httpx.post(url, json = paymentInfo)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, host='0.0.0.0', debug=True)