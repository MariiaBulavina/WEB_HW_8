from mongoengine import Document, BooleanField, StringField, connect

connect(db='hw_8', host='mongodb+srv://webuser18:password123456@cluster0.hhynnp6.mongodb.net/?retryWrites=true&w=majority')


class Contact(Document):

    fullname = StringField(max_length=100)
    email = StringField(max_length=50)
    address = StringField()
    sent = BooleanField(default=False)
    meta = {'collection': 'contacts'}

