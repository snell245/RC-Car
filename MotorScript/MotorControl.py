import 1293d.driver as 1293d

motor1 = 1293d.motor(22,18,16)
motor2 = 1293d.motor(15,13,11)

for i in range(0,10) :
    motor1.clockwise()
    motor2.clockwise()

1293d.cleanup()