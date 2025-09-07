# CoffeeControl

## Requirements
The project is built with Django and requires the following libraries:
```
pip install django
pip install pillow
```

## How to run
Open a terminal (for example, PowerShell) and navigate to the folder where the project is located.

Example:
```
cd C:\Users\ASUS\Desktop\CoffeeControl
```

Once inside the folder, start the development server with:
```
python manage.py runserver
```

If port 8000 is already in use, you can choose another one, for example:
```
python manage.py runserver 8080
```

## Test Users
The system includes test accounts to explore the application with different roles:

**Administrator**
- Username: Prueba1
- Password: Kalena12
(Used to manage products, view orders, and create or edit users.)

**Waiter**
- Username: Mesero1
- Password: Kalena12
(Used to create new orders, add products to them, and view only their own orders.)

You can also create a **superuser** to access Django’s admin panel with full database control and permission management:
```
python manage.py createsuperuser
```
## Online Deployment: 
The project is also deployed on PythonAnywhere and can be accessed here:  
https://kadiha.pythonanywhere.com/
```

