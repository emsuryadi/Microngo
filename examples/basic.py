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

contact = db.insert("contact")
contact.name = "Suryadi"
contact.gender = "male"
contact.created = datetime.utcnow()
contact.status = 1
contact.phone = {
	"home": "(233) 233176",
	"cell": "+62122312"
}
contact_id = contact.save()
print("contact id:", contact_id) # Print info

# Insert many
calls = db.insert("calls")
for i in range(0, 10):
	calls.no = i
	calls.phone = randrange(1000, 9999)
	calls.add() # Add
calls.save() # Save

#
# Read data
#

contact_data = db.query("contact").find().sort('name', 1).first()
if contact_data:
	print("name:", contact_data.name)
	print("gender:", contact_data.gender)

calls_data = db.query("calls").find().all()
for item in calls_data:
	print("no:", item.no)
	print("phone:", item.phone)

#
# Update data
#

suryadi_data = db.query("contact").find_by(name="Suryadi").first()
if suryadi_data:
	suryadi_data.name = "Em Suryadi"
	suryadi_data.save()
	print("update id", suryadi_data._id)

#
# Paginate
#

paginated_data = db.query("calls").find().paginate(1, per_page=2)
# Info
print("total pages:", paginated_data.pages)
print("current page:", paginated_data.page)
print("has next page:", paginated_data.has_next())
print("next page:", paginated_data.next_num)
print("has prev page:", paginated_data.has_prev())
print("prev page:", paginated_data.prev_num)
# Item
for call in paginated_data.items:
	print("call no.", call.no)

#
# Delete data
#

calls_data = db.query("calls").find().limit(5).sort('no', 1).all()
for call in calls_data:
	print("call no.", call.no)
	call.remove()