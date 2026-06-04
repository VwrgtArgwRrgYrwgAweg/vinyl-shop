from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main.models import Order  # 👈 ДОБАВЬ ЭТУ СТРОКУ (импорт заказов)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # 👈 ДОБАВЬ ЭТУ СТРОКУ
    return render(request, 'users/profile.html', {'orders': orders})  # 👈 ИСПРАВЬ ЭТУ СТРОКУ (добавь orders)

def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')