from passlib.apps import custom_app_context as pwd_context

passw = ""

print(pwd_context.encrypt(passw))
