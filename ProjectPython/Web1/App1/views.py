from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .forms import AddLoginForm, AddRegisterForm, AddAppartmentForm, RequestForm, UpdateStatusForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from .models import Appartment
from .models import Appartment, Seller, Request


# Create your views here.
def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(
            data=request.POST
        )
        print("POST Data:", request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if (
                    hasattr(user, "isSeller") and user.isSeller
                ):  # בדיקה ש-`user` מכיל `isBuyer`
                    return redirect("/seller_dashboard/")
                else:
                    return redirect("apartment_list")
        else:
            return render(request, "Login.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "Login.html", {"form": form})


def Register(request):
    if request.method == "POST":
        form = AddRegisterForm(request.POST)
        if form.is_valid():
            isSeller = form.cleaned_data["isSeller"]
            username = form.cleaned_data["username"]
            if isSeller:
                user = form.save()
                seller = Seller.objects.all()
                s = Seller(id=len(seller) + 1, personId=user)
                s.save()
            else:
                form.save()  # שמירת המשתמש החדש
            return redirect("/login")  # לאחר ההרשמה, אפשר להפנות לעמוד התחברות
    else:
        form = AddRegisterForm()
    return render(request, "register.html", {"form": form})

def homePage(request):
    return render(request, "HomePage.html")
def add_appartment(request):
    if request.method == "POST":
        form = AddAppartmentForm(request.POST, request.FILES)

        if form.is_valid():
            # יש לבדוק שהמוכר מחובר ולא "אורח"
            if request.user.is_authenticated:
                # מוצאים את המוכר הקיים
                seller = Seller.objects.get(personId=request.user)
                # אם המוכר לא קיים, זה לא אפשרי להוסיף דירה
                if not seller:
                    return redirect("error")  # דף טעות, לדוגמה

                # יצירת דירה חדשה עם המוכר המחובר
                appartment = form.save(commit=False)
                appartment.sellerId = seller
                appartment.save()
                # לאחר השמירה, הפנייה לדף המוכר
                return redirect("seller_dashboard")
    else:
        form = AddAppartmentForm()

    return render(request, "addApartment.html", {"form": form})

@login_required
def seller_dashboard(request):
    user = request.user

    if not user.isSeller:
        return redirect("home")

    seller = Seller.objects.get(personId=user)

    # מצא את כל הדירות של המוכר
    appartments = Appartment.objects.filter(sellerId=seller)

    # הוסף פניות לכל דירה
    for appartment in appartments:
        appartment.requests = Request.objects.filter(apartmentId=appartment)
        print(f"Appartment: {appartment.id}, Requests: {appartment.requests}")

    # צור דיקשנרי עם המידע כדי לשלוח לתבנית
    context = {
        "appartments": appartments,
    }

    return render(request, "seller_dashboard.html", context)

def apartment_list(request):
    city = request.GET.get("city", "")
    street = request.GET.get("street", "")
    room_num = request.GET.get("room_num", "")
    condition = request.GET.get("condition", "")

    apartments = Appartment.objects.filter(status=False)
    # סינון לפי עיר
    if city:
        apartments = apartments.filter(city__icontains=city)
    # סינון לפי רחוב
    if street:
        apartments = apartments.filter(street__icontains=street)
    # סינון לפי מספר חדרים אם הוא לא ריק
    if room_num and room_num != "0":
        apartments = apartments.filter(roomNum=room_num)
    # סינון לפי מצב הדירה אם הוא לא ריק
    if condition:
        apartments = apartments.filter(condition=condition)
    # החזר את הדירות שמסוננות או את כל הדירות אם לא בוצע סינון
    return render(request, "apartment_list.html", {"apartments": apartments})

def request_form(request, apartment_id):
    apartment = Appartment.objects.get(id=apartment_id)

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            # יצירת פנייה חדשה
            new_request = form.save(commit=False)
            new_request.apartmentId = apartment
            new_request.sellerId = apartment.sellerId
            new_request.personId = request.user
            new_request.save()
            return redirect("apartment_list")
    else:
        form = RequestForm()

    return render(request, "send_request.html", {"form": form, "apartment": apartment})


@login_required
def update_status(request):
    if request.method == "POST":
        appartment_id = request.POST.get('appartment_id')
        appartment = get_object_or_404(Appartment, id=appartment_id)

        # עדכון הסטטוס של הדירה (נמכרה או לא)
        appartment.status = not appartment.status  # אם היה false, יהפוך ל-True ולהפך
        appartment.save()

        # בדיקה אם המוכר הוא מתווך
        if appartment.sellerId:  # אם יש למוכר מזהה
            seller = appartment.sellerId
            if seller.personId.isSeller:  # אם המוכר הוא מתווך (isSeller == True)
                # אם הדירה נמכרה, נוסיף עמלה מצטברת
                if appartment.status:  # אם הדירה נמכרה
                    seller.total_commission += 2500  # הוספת עמלה של 2500 ש"ח למתווך
                    seller.save()


    return redirect('seller_dashboard')
