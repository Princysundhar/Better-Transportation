from django.db import models

# Create your models here.

class login_table(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)

class user_table(models.Model):
    LOGIN_TABLE = models.ForeignKey(login_table, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000)

class feedback_table(models.Model):
    USER_TABLE = models.ForeignKey(user_table, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    feedback = models.CharField(max_length=1000)

class workers_table(models.Model):
    LOGIN_TABLE = models.ForeignKey(login_table, default=1, on_delete=models.CASCADE)
    workername = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    landmark = models.CharField(max_length=1000,default=1)
    place = models.CharField(max_length=100,default=1)
    postcode = models.CharField(max_length=100,default=1)
    latitude = models.CharField(max_length=100,default=1)
    longitude = models.CharField(max_length=100,default=1)
    aadhar = models.CharField(max_length=100,default=1)
    photo = models.CharField(max_length=1000)

class rating_review_table(models.Model):
    USER = models.ForeignKey(user_table, default=1, on_delete=models.CASCADE)
    WORKER = models.ForeignKey(workers_table, default=1, on_delete=models.CASCADE)
    rating = models.CharField(max_length=100)
    review = models.CharField(max_length=1000)
    date = models.CharField(max_length=100)

class request_table(models.Model):
    USER_TABLE = models.ForeignKey(user_table, default=1, on_delete=models.CASCADE)
    WORKER_TABLE = models.ForeignKey(workers_table, default=1, on_delete=models.CASCADE)
    remark = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    latitude = models.CharField(max_length=1000 , default=1)
    longitude = models.CharField(max_length=1000, default=1)
    status = models.CharField(max_length=100, default=1)
    amount = models.CharField(max_length=100)


class payment_table(models.Model):
    REQUEST_TABLE = models.ForeignKey(request_table,on_delete=models.CASCADE,default=1)
    USER_TABLE = models.ForeignKey(user_table, default=1, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=100)

class credit_point_table(models.Model):
    LOGIN_TABLE = models.ForeignKey(login_table, default=1, on_delete=models.CASCADE)
    coins = models.CharField(max_length=100)

class bank(models.Model):
    bank_name = models.CharField(max_length=100)
    account_no = models.CharField(max_length=100)
    IFSC_code = models.CharField(max_length=100)
    amount = models.IntegerField()
    LOGIN_TABLE = models.ForeignKey(login_table, default=1, on_delete=models.CASCADE)


class secret_code_table(models.Model):
    USER_TABLE = models.ForeignKey(user_table, default=1, on_delete=models.CASCADE)
    WORKER_TABLE = models.ForeignKey(workers_table, default=1, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)

class complaints_table(models.Model):
    LOGIN_TABLE = models.ForeignKey(login_table, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    complaint = models.CharField(max_length=1000)
    ctype = models.CharField(max_length=100)
    reply = models.CharField(max_length=200)
    rdate = models.CharField(max_length=20)

class chat(models.Model):
    chat = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    USER_TABLE = models.ForeignKey(user_table, default=1, on_delete=models.CASCADE)
    WORKER_TABLE = models.ForeignKey(workers_table, default=1, on_delete=models.CASCADE)


