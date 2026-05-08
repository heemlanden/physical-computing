from machine import Pin

# Voorbeeld voor een simpele actuator (geen driver nodig):
pin_num = 9 # Dit is het nummer van de pinout waarmee je de actuator verbonden hebt. 9 is een willekeurig voorbeeld.
actuator = Pin(pin_num, Pin.OUT)

# Met actuator.value(0) of value(1) kan je vervolgens de actuator uit en aanzetten.
# (De koppeling van 0 en 1 aan uit en aan verschilt per actuator.)


# Voorbeeld voor een simpele sensor (geen driver nodig):
pin_num = 9 # Dit is het nummer van de pinout waarmee je de sensor verbonden hebt. 9 is een willekeurig voorbeeld.
sensor = Pin(pin_num, Pin.IN, Pin.PULL_UP) # Test zelf wat er gebeurt als je Pin.PULL_UP verandert in Pin.PULL_DOWN en wat bij jou logisch is. 
# Met sensor.value() krijg je vervolgens de huidige waarde van de sensor.

