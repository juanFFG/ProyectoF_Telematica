from flask import jsonify, Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__)

acceso = False

# Ruta para mostrar el formulario de login
@app.route('/')
def show_login():
    return render_template('login.html')

# Ruta para procesar los datos del formulario de login
@app.route('/login', methods=['POST', 'GET'])
def do_login():
    ArrayUsers = []
    ArrayPasswords = []
    global acceso
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        url="http://172.31.80.215:8080/enviar_usuarios" 
        data = pd.read_json(url, convert_dates=True)

        for index, row in data.iterrows():
            ArrayUsers.append(row['username'])
            ArrayPasswords.append(row['password'])

        for i in range(len(ArrayUsers)):
            if ArrayUsers[i] == username and str(ArrayPasswords[i]) == password:
                acceso = True

        if acceso:
            return redirect(url_for('fig'))
        else:
            return render_template('acceso_denegado.html')
    return render_template('login.html')



@app.route('/fig')
def fig():

        if(acceso):
                 url = "http://172.31.80.215:8100/mostrar_estacionesnivel?psw=12345678"
                 data = pd.read_json(url,convert_dates='True')

                 latr = []
                 lonr = []
                 zr = []
                 for i in range(0,100):
                         zr.append(data['datos'][i]['porcentajeNivel'])
                         latr.append(data['datos'][i]['coordenadas'][0]['latitud'])
                         lonr.append(data['datos'][i]['coordenadas'][0]['longitud'])

                 fig = go.Figure(go.Densitymapbox(lat=latr,lon=lonr,z=zr,radius=20, opacity=0.9, zmin=0, zmax = 100))
                 fig.update_layout(mapbox_style="stamen-terrain",mapbox_center_lon=-75.589,mapbox_center_lat=6.2429)
                 fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) 
                 graphJSON = fig.to_json()

                 return render_template('front.html', graphJSON=graphJSON)

        else:
                return render_template('acceso_denegado.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8000)
