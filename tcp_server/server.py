import socket
import requests
import json
import datetime

def convert_to_local_time(timestamp, timezone_offset):
    # Convert Unix timestamp to UTC time
    utc_time = datetime.datetime.utcfromtimestamp(timestamp)
    
    # Convert timezone offset from seconds to timedelta
    time_diff = datetime.timedelta(seconds=timezone_offset)
    
    # Adjust time to local timezone
    local_time = utc_time + time_diff
    
    # Format local time into a human-readable string
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return formatted_time

def fetch_weather(city):
    api_key = "2daef3a757430743c872e0ad0a0352e5"  # Get your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    print(data)
    if data["cod"] == 200:
        
        main_data = data["main"]
        timezone = data["timezone"]
        dt = data["dt"]
        time = convert_to_local_time(timezone, dt)
        weather_data = data["weather"][0]
        wind = data["wind"]
        temp = main_data['temp']
        feels_like = main_data['feels_like']
        humidity =  main_data['humidity']
        description = weather_data['description']
        icon = weather_data['icon']
        wind_speed = round(wind['speed'] * 3.6)
        
        weather_info = f"|{temp}|{feels_like}|{humidity}|{description}|{time}|{icon}|{wind_speed}|"
    else:
        weather_info = 'error'
    
    return weather_info


def server_program():
    host = '192.168.13.88'  # Server IP address
    port = 8080       # Port to bind

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)  # Listen for one client
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

  
    city = conn.recv(1024).decode()  # Receive city name from client
    weather_info = fetch_weather(city)  # Fetch weather information
    conn.send(json.dumps(weather_info).encode())
    conn.close()

if __name__ == "__main__":
    server_program()
