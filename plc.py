from pyModbusTCP.client import ModbusClient
import time

try:
	c = ModbusClient(host='10.41.110.255', port=502, unit_id=1,auto_open=True)
except ValueError:
	print("Error with host or port params")

# open the socket for 2 reads then close it.
	
"""if c.open():
    regs_list_1 = c.read_input_registers(0, 4)
    write = c.write_multiple_registers(0, [0x0F]*2)
    print(regs_list_1)                      # use information
    c.close()
"""
while True:
    try:
        regs_list_1 = c.read_input_registers(0, 4)
        print(regs_list_1)                      
    except:
        print("conexion cerrada")
        c.close()
        break
    time.sleep(1)