This is a Django app for RSVP
1. virtualenv myEnv
2. source ./myEnv/bin/activate
3. pip install -r requirement.txt
4. python3 manage.py runserver

# Screenshots
## Dashboard
<img src="res_imgs/1.png" width="80%">

## Add New Event
<img src="res_imgs/2.png" width="80%">

## Add New Guest
<img src="res_imgs/3.png" width="80%">

Adding new entry generates a hash string and a QR code which is sent to the Guest, so guest can visit a unique link and update how many members from his/her family will attend the event.

Hash string is used so that no one can change other persons data without unique link or QR code.

## Before
<img src="res_imgs/4.1.png" width="80%">

## Guest Scanning QR code and updating the data
<img src="res_imgs/qrcode_hand.png" width="30%">

## After
<img src="res_imgs/4.2.png" width="80%">

## Event wise data
<img src="res_imgs/5.png" width="80%">