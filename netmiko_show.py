from netmiko import ConnectHandler

# Establecer la conexión SSH con el router
sshCli = ConnectHandler(
    device_type='cisco_ios',
    host='192.168.80.39',
    port=22,
    username='cisco',
    password='cisco123!'
)

# Lista de comandos a enviar
commands = [
    "show version",
    "show running-config",
    "show ip interface brief",
]

# Enviar los comandos al router y almacenar la salida en una lista
output = []
for command in commands:
    result = sshCli.send_command(command)
    output.append(result)

# Imprimir la salida de cada comando
for i in range(len(commands)):
    print("==== '{}' ====".format(commands[i]))
    print(output[i])
    print("=" * 50)  # Separador entre cada comando
