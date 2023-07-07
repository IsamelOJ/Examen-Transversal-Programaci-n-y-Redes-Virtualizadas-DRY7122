import urllib.parse
import requests
from googletrans import Translator
import math

# URL base de la API de MapQuest
main_api = "https://www.mapquestapi.com/directions/v2/route?"

# Clave de acceso para la API de MapQuest (reemplazar por una clave válida)
key = "Xd35VebxDItDc2GZLOopJW2kZRWgrbPL"

# Eficiencia promedio del combustible en MPG (millas por galón)
average_fuel_efficiency = 25

# Instancia de Translator para traducción de texto
translator = Translator()

# Función para formatear un valor numérico con un solo decimal
def format_decimal(value):
    return "{:.1f}".format(value)

# Función para formatear una duración en segundos como horas, minutos y segundos
def format_duration(seconds):
    hours = math.floor(seconds / 3600)
    minutes = math.floor((seconds % 3600) / 60)
    seconds = seconds % 60
    return f"{hours} horas, {minutes} minutos, {seconds} segundos"

# Bucle principal del programa
while True:
    # Solicitar ubicación de partida al usuario
    orig = input("Ubicación de partida: ")
    if orig == "S" or orig == "s":
        break
    
    # Solicitar destino al usuario
    dest = input("Destino: ")
    if dest == "S" or dest == "s":
        break

    # Construir la URL de la API utilizando urllib.parse.urlencode para codificar los parámetros
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL: " + url)

    # Realizar una solicitud GET a la API y obtener la respuesta en formato JSON
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        # La llamada de ruta fue exitosa, se procesan los datos
        print("Estado de la API: " + str(json_status) + " = Llamada de ruta exitosa.\n")
        print("=============================================")
        print("Cómo llegar desde " + orig + " a " + dest)

        # Duración del viaje en horas, minutos y segundos
        duration_seconds = json_data["route"]["time"]
        duration_formatted = format_duration(duration_seconds)
        print("Duración del viaje:   " + duration_formatted)

        print("Kilómetros: " + format_decimal(json_data["route"]["distance"] * 1.61))

        # Estimación del combustible utilizado
        if "fuelUsed" in json_data["route"]:
            fuel_used = json_data["route"]["fuelUsed"]
            print("Combustible utilizado (Ltr): " + format_decimal(fuel_used * 3.78))
        else:
            distance_miles = json_data["route"]["distance"]
            fuel_used_estimation = distance_miles / average_fuel_efficiency
            print("No se pudieron obtener los datos de combustible de MapQuest.")
            print("Estimado del combustible utilizado (Ltr): " + format_decimal(fuel_used_estimation * 3.78))

        print("=============================================")

        print("Maniobras en español:")
        maneuvers = json_data["route"]["legs"][0]["maneuvers"]
        for maneuver in maneuvers:
            narrative = maneuver["narrative"]
            distance_km = maneuver["distance"] * 1.61
            translated_narrative = translator.translate(narrative, dest="es").text
            print("- " + translated_narrative + " (" + format_decimal(distance_km) + " km)")

        print("=============================================")
        
    elif json_status == 402:
        # Entradas de usuario inválidas para una o ambas ubicaciones
        print("**********************************************")
        print("Código de estado: " + str(json_status) + "; Entradas de usuario inválidas para una o ambas ubicaciones.")
        print("**********************************************\n")
    elif json_status == 611:
        # Falta una entrada para una o ambas ubicaciones
        print("**********************************************")
        print("Código de estado: " + str(json_status) + "; Falta una entrada para una o ambas ubicaciones.")
        print("**********************************************\n")
    else:
        # Otro código de estado, se muestra un mensaje de error y un enlace para más información
        print("************************************************************************")
        print("Para el código de estado: " + str(json_status) + "; Consulte:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")
