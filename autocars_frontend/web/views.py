from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth import logout as django_logout
from django.views.decorators.csrf import csrf_exempt
import json
from .decorators import token_required
from django.contrib import messages

API_URL = "http://127.0.0.1:8000/api"  # Your backend API

def home(request):
    return render(request, "web/index.html")

@csrf_exempt
def register_view(request):
    error = None
    if request.method == "POST":
        data = {
            "username": request.POST["username"],
            "email": request.POST["email"],
            "password": request.POST["password"],
            "password2": request.POST["password2"],
            "is_seller": "is_seller" in request.POST,
        }
        res = requests.post(f"{API_URL}/auth/register/", headers={"Content-Type": "application/json"}, data=json.dumps(data))
        print(res.status_code, res.text)
        if res.status_code in [200, 201]:
            # Auto-login
            login_res = requests.post(f"{API_URL}/token/", headers={"Content-Type": "application/json"}, data=json.dumps({"username": data["username"], "password": data["password"]}))
            if login_res.status_code == 200:
                request.session["token"] = login_res.json()["access"]
                return redirect("cars")
            else:
                error = "Registration succeeded but login failed"
        else:
            try:
                error = res.json()
            except:
                error = "Registration failed"
    return render(request, "web/register.html", {"error": error})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        res = requests.post(f"{API_URL}/token/", data={"username": username, "password": password})

        if res.status_code == 200:
            tokens = res.json()
            access = tokens.get("access")
            refresh = tokens.get("refresh")

            request.session["token"] = access
            request.session["refresh"] = refresh

            # Fetch user info
            user_res = requests.get(
                f"{API_URL}/users/me/",
                headers={"Authorization": f"Bearer {access}"}
            )

            if user_res.status_code == 200:
                user = user_res.json()
                request.session["username"] = user.get("username")
                request.session["is_seller"] = user.get("is_seller", False)  # 👈 important
            else:
                request.session["is_seller"] = False
            
            # 🔍 Debug session content
            print("SESSION DATA:", dict(request.session))

            return redirect("cars")
        

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "web/login.html")


@token_required
def cars(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(f"{API_URL}/cars/", headers=headers)
        if res.status_code == 200:
            data = res.json()
            cars = data.get("results", [])  # 👈 only the results list
        else:
            cars = []
    except Exception as e:
        print("Error fetching cars:", e)
        cars = []

    return render(request, "web/cars.html", {"cars": cars})


def logout_view(request):
    # Remove JWT token from session
    request.session.pop("token", None)
    # Optionally log out from Django auth (if used)
    django_logout(request)
    return redirect("home")

def add_car(request):
    token = request.session.get("token")
    if not token:
        return redirect("login")

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        data = {
            "make": request.POST.get("make"),
            "model": request.POST.get("model"),
            "year": request.POST.get("year"),
            "price": request.POST.get("price"),
            "description": request.POST.get("description"),
            "is_available": True,
        }
        files = {}
        if request.FILES.get("image"):
            files["image"] = request.FILES["image"]

        res = requests.post(f"{API_URL}/cars/", headers=headers, data=data, files=files)

        if res.status_code in [200, 201]:
            messages.success(request, "Car added successfully!")
            return redirect("cars")
        else:
            messages.error(request, f"Failed to add car: {res.text}")

    return render(request, "web/addcar.html")
