from django.db import models
from accounts.models import Account
from orders.models import Payment
import qrcode
from django.core.files import File
from PIL import Image ,ImageDraw
from io import BytesIO


class Qrcode(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    description=models.TextField(max_length=200)
    qr_code=models.ImageField(upload_to='photos/qrcode',blank=True)



    def save(self,*args, **kwargs):
        qrcode_img=qrcode.make(self.description)
        width, height = qrcode_img.size
        cwidth=800-width
        chight=800-height
        a=int(cwidth/2)
        b=int(chight/2)
        (print(a,b))
        canvas=Image.new('RGB',(800,800),'white')
        draw=ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img,(a,b))
        fname=f'qr_code-{self.description}.png'
        buffer=BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super(Qrcode, self).save(*args, **kwargs)






# Create your models here.
