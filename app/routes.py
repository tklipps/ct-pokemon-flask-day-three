from flask import render_template, request, redirect, url_for
import requests
from app import app
from .forms import PokeForm, LoginForm, RegisterForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():        
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()

        if u and u.check_hashed_password(password):
            login_user(u)        
            return redirect(url_for("index"))
        error_string = "Invalid Email password combo"
        return render_template('login.html.j2', error = error_string, form=form)
    return render_template('login.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password": form.password.data
            }
            
            new_user_object = User()            
            new_user_object.from_dict(new_user_data)            
            new_user_object.save()
        except:
            error_string = "There was an unexpected Error creating your account. Please Try again."
            return render_template('register.html.j2',form=form, error = error_string) 
        return redirect(url_for('login'))
    return render_template('register.html.j2', form = form) 


@app.route('/pokeinfo', methods=['GET', 'POST'])
@login_required
def pokeinfo():
    form = PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        poke = request.form.get('poke_id')
        url = f"https://pokeapi.co/api/v2/pokemon/{poke}"
        
        response = requests.get(url)
        if response.ok:            
            data = response.json()
                  
            
            poke_dict={
                'poke_name':data['name'],
                'base_hp':data['stats'][0]['base_stat'],
                'base_defense':data['stats'][2]['base_stat'],
                'base_attack':data['stats'][1]['base_stat'],                    
                'front_shiny':data["sprites"]["front_shiny"],
            }
                
            print(poke_dict)
            return render_template('pokeinfo.html.j2', poke=poke_dict, form=form)     
        
        else:
            return "That's not a Pokemon!!!"
            

    return render_template('pokeinfo.html.j2', form=form)