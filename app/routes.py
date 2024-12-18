from flask import Blueprint, render_template, request
import socket
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']

    weather_info = get_weather_info(city)
    
    # If error message returned, display it
    if isinstance(weather_info, str) and weather_info.startswith("error"):
        error_message = weather_info
        return render_template('base.html', error_message=error_message)
    else:
        weather_info, icon, description, temp, feels_like, humidity, wind_speed, time = weather_info
        return render_template('city.html', cityname=city, weather_info=weather_info, icon=icon, description=description, 
                               temp=temp, feels_like=feels_like, humidity=humidity, wind_speed=wind_speed, time=time)

def get_weather_info(city):
    host = '192.168.13.88'  # Server IP address
    port = 8080              # Port to connect to

    try:
        # Create socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)  # Set a timeout for the connection

        # Try connecting to the server
        client_socket.connect((host, port))
        
        # Send the city name
        client_socket.send(city.encode())

        # Receive the weather data
        weather_info = client_socket.recv(1024).decode()
        
        # Close the socket
        client_socket.close()

        if weather_info == '\"error\"':
            return "error: City not found or invalid data."

        # Split and validate the received data
        weather_info_parts = weather_info.split('|')
        
        if len(weather_info_parts) < 8:
            return "error: Incomplete data received."

        temp = weather_info_parts[1]
        feels_like = weather_info_parts[2]
        humidity = weather_info_parts[3]
        description = weather_info_parts[4]
        time = weather_info_parts[5]
        icon = f"https://openweathermap.org/img/wn/{weather_info_parts[6]}.png"
        wind_speed = weather_info_parts[7]

        return weather_info, icon, description, temp, feels_like, humidity, wind_speed, time
    
    except socket.timeout:
        return "error: Timeout occurred while trying to connect to the server."
    except socket.error as e:
        return f"error: Unable to connect to the server. Error: {str(e)}"
    except Exception as e:
        return f"error: An unexpected error occurred. Error: {str(e)}"
