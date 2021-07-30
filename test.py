import bcrypt

password1 = '1234'
tmp1 = bcrypt.hashpw(password1.encode('utf-8'),bcrypt.gensalt())
print(tmp1)
print(tmp1.decode('utf-8'))
# DB에 저장시에는 decode해서 저장
password2 = '1234'
tmp2 = bcrypt.hashpw(password2.encode('utf-8'),bcrypt.gensalt())
print(tmp2)
print(tmp2.decode('utf-8'))
flag1 =bcrypt.checkpw(password2.encode('utf-8'),tmp1)
print(flag1) # 다시 비교할때는 encoding 해서 비교
flag2= bcrypt.checkpw(password1.encode('utf-8'),tmp2)
print(flag2)