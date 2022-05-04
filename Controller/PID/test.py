import pigpio

pi = pigpio.pi()

PWM1 = 19

pi.set_mode(PWM1, pigpio.OUTPUT)

pi.set_PWM_frequency(PWM1, 1000)


try:
    while True:
        pi.set_PWM_dutycycle(PWM1, 125)

except KeyboardInterrupt:
    pass
pi.set_PWM_dutycycle(PWM1, 0)
pi.cleaup()


