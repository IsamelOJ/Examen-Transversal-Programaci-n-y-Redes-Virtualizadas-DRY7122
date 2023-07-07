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

# Definir la configuración de la interfaz de loopback
netconf_loopback = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>1</name>
                <description>Configuracion de loopback mediante ncclient ET</description>
                <ip>
                    <address>
                        <primary>
                            <address>1.1.1.1</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

# Aplicar la configuración de la interfaz de loopback al dispositivo
netconf_reply = m.edit_config(target="running", config=netconf_loopback)

# Imprimir la respuesta XML prettified de la configuración de la interfaz de loopback
print("Respuesta de cambio de configuración - Interfaz de Loopback:")
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
