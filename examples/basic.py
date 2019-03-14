from microngo import Microngo
from datetime import datetime
from random import randrange

#
# Client
#

db = Microngo('localhost', 27017, db="microngo_test")

#
# Insert data
#

contact			= db.insert("Contact")
contact.Name	= "Suryadi"
contact.Gender	= "male"
contact.Created	= datetime.utcnow()
contact.Status	= 1
contact.Phone	= {
	"Home":	"(233) 233176",
	"Cell":	"+62122312"
}
contact_id = contact.save()

# Print info
print("Contact ID:", contact_id)
print()

# Insert many
calls = db.insert("Calls")
for i in range(0, 10):
	calls.No	= i
	calls.Phone	= randrange(1000, 9999)
	
	# Add
	calls.add()

# Save
calls.save()

#
# Read data
#

contact_data = db.query("Contact").find().sort('Name', 1).first()
if contact_data:
	print("Name:", contact_data.Name)
	print("Gender:", contact_data.Gender)
	print()

calls_data = db.query("Calls").find().all()
for item in calls_data:
	print("No:", item.No)
	print("Phone:", item.Phone)

print()

#
# Update data
#

suryadi_data = db.query("Contact").find_by(Name="Suryadi").first()
if suryadi_data:
	suryadi_data.Name = "Em Suryadi"
	suryadi_data.save()
	print("Update ID", suryadi_data._id)

print()

#
# Delete data
#

calls_data = db.query("Calls").find().limit(5).sort('No', 1).all()
for call in calls_data:
	print("Call No", call.No)
	call.remove()