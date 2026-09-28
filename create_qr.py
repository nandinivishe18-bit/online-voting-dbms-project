import qrcode
import os

laptop_ip = "http://YOUR_IP_ADDRESS:5000/results"

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)

qr.add_data(laptop_ip)
qr.make(fit=True)

img = qr.make_image(
    fill_color="black",
    back_color="white"
)

if not os.path.exists('static'):
    os.makedirs('static')

img.save("static/feedback-qr.png")

print("QR Code saved as 'static/feedback-qr.png'")
