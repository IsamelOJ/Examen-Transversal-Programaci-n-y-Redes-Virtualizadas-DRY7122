from ncclient import manager
import xml.dom.minidom

# Establecer conexión NETCONF
m = manager.connect(
    host="192.168.80.39",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# Definir el cambio de nombre de host
new_hostname = "MELINAO-OTEIZA-CUMILEF"

# Definir la variable para modificar la configuración
netconf_hostname = f"""
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>{new_hostname}</hostname>
    </native>
</config>
"""

# Aplicar el cambio de configuración al dispositivo
netconf_reply = m.edit_config(target="running", config=netconf_hostname)

# Imprimir la respuesta XML prettified del cambio de configuración
print("Respuesta de cambio de configuración:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Definir el filtro NETCONF para obtener la configuración actual
netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""

# Obtener configuración actual del dispositivo con el filtro
netconf_reply = m.get_config(source="running", filter=netconf_filter)

# Imprimir la respuesta XML prettified de la configuración actual
print("Configuración actual:")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())