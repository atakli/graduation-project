import RPi.GPIO as GPIO
#~ import pickle
import time
GPIO.setmode(GPIO.BOARD)

#~ pinout'lara şurdan bakabilirsin:
#~ https://rpi.science.uoit.ca/lab/gpio/
# iki tane pin convention'ı var. biri sıra sıra olan, diğeri GPIO...
# şeklinde olan. Burdaki numaralar sıra sıra olanlara göre. Yani Pin# sütunundakiler.
# ve rpi'yi gpio'lar sağda kalacak şekilde tutup ona göre hesapla pinleri.

#~ GPIO.setwarnings(False) bunu kullanmalı mıyız bakmak gerek


var_herhalde=0


# genel amaçlı pinlerden herhangi biri kullanılabiliyo. Ben rastgele bunları seçtim.
in1 = 37
in2 = 35
motorOutputPin1 = 38 # 32 33 35 (board) 12 13 19 (bcm)
#~ 32 12 33 35 ( board )
#~ 12 18 13 19 ( bcm )
# sağ

in3 = 33
in4 = 31
motorOutputPin2 = 29 

maksimum = 100

pid_p_angle = pid_p_distance = pwmleft = pwmright = 0
#~ elapsedTime, ac_time, timePrev = 0

PID = error_distance = error_angle = previous_error = pid_p = pid_i = pid_d = 0
##################PID CONSTANTS of distance##################
kp_distance=15#3.55
kd_distance=0.0 #2.05
####################################

##################/ID CONSTANTS of angle#####################
kp_angle=2.2*(180/3.14) #2.2
kd_angle=0.0 #2.05
#############################################################

desired_angle = 0 # This is the angle in which we want the
                  # balance to stay steady

desired_distance = 0 # This is the distance in which we want the
                     # balance to stay steady
                       
# burası eksik olabilir
GPIO.setup(motorOutputPin1, GPIO.OUT)
GPIO.setup(motorOutputPin2, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

#Send PWM signal to L298N Enable 
pwm_yaz_sol = GPIO.PWM(motorOutputPin1, 500) # PWM has timing resolution of 1 us according to:
pwm_yaz_sag = GPIO.PWM(motorOutputPin2, 500) # https://www.electronicwings.com/raspberry-pi/raspberry-pi-pwm-generation-using-python-and-c
# şimdi software pwm'i kullanıyoruz.
# bize eğer 1us (1000 Hz)'den daha yüksek bir resolution lazımsa hardware PWM'i kullanmak lazım. Onu araştırmadım.

pwm_yaz_sol.start(pwmleft)
pwm_yaz_sag.start(pwmright)
# means that daha dongu() fonksiyonunu çapırmadan önce ta video.py'nin başında
# bu control.py'yi import ettiğimiz zaman ilgili pinler pwm vermeye başlıyo, ama 0. (fyi)
direction=1

def yer(yon):
    global direction, in1, in2
    ters = 0
    if yon == 0:
        ters = 1
    if (error_distance >= 40):
        if (direction==1):
            pwmleft  = 90 + pid_p_angle
            pwmright = 90 - pid_p_angle
        else:
            pwmleft  = 90 + 0.7*pid_p_angle
            pwmright = 90 - 1.4*pid_p_angle
    
    #~ elif (error_distance <= 30 and error_distance >= 20):
        #~ pwmleft  = 50 - pid_p_angle 
        #~ pwmright = 50 + pid_p_angle 
    #~ else:##sonradan ekledik
        #~ pwmleft = 0
        #~ pwmright =0 
    else:
        pwmleft  = 30 - 0.7 * pid_p_angle 
        pwmright = 30 + 0.7 * pid_p_angle  
    if (pwmleft >= 0):
        GPIO.output(in1, yon)
        GPIO.output(in2, ters)
        direction=1
    else:
        pwmleft = -pwmleft;
        GPIO.output(in1, ters)
        GPIO.output(in2, yon)
        direction=2

    if (pwmright >= 0):
        GPIO.output(in3, yon)
        GPIO.output(in4, ters)
    else:
        pwmright = -pwmright;
        GPIO.output(in3, ters)
        GPIO.output(in4, yon)
        
    pwmleft = min(pwmleft,maksimum)
    pwmright = min(pwmright,maksimum)
    pwm_yaz_sol.ChangeDutyCycle(pwmleft)
    pwm_yaz_sag.ChangeDutyCycle(pwmright)    
   
    
    return pwmleft,pwmright

def dongu(angle=None, distance=None,yok_mu = 0,tersmi_duzmu = 1):
    global error_distance,error_angle,pid_p_distance, pid_p_angle, var_herhalde, direction, in1, in2
    #~ with open('result.obj','rb') as dist:
        #~ result = pickle.load(dist)
    #~ First calculate the error between the desired angle and 
    #~ the real measured angle and for distance
    if yok_mu == 1:
        #~ if result < 10:
            #~ pwmleft  = 0
            #~ pwmright = 0
        #~ else:
        if var_herhalde == 1:
            pwmright = 80
            pwmleft = 80
            GPIO.output(in1, GPIO.LOW)#LOW
            GPIO.output(in2, GPIO.HIGH)
            GPIO.output(in4, GPIO.LOW)#LOW
            GPIO.output(in3, GPIO.HIGH)
            pwm_yaz_sol.ChangeDutyCycle(pwmleft)
            pwm_yaz_sag.ChangeDutyCycle(pwmright)       
            
            time.sleep(0.3)
            
            var_herhalde=0 
            
        else:
            pwmright = 80
            pwmleft = 80
            GPIO.output(in1, GPIO.HIGH)#HIGH
            GPIO.output(in2, GPIO.LOW)
            GPIO.output(in4, GPIO.HIGH)#HIGH
            GPIO.output(in3, GPIO.LOW)
            pwm_yaz_sol.ChangeDutyCycle(pwmleft)
            pwm_yaz_sag.ChangeDutyCycle(pwmright)
            
             
        return pwmleft,pwmright 
        
        
    else:
        var_herhalde=1
        
        error_angle = angle - desired_angle
        error_distance = distance - desired_distance

        #~ Next the proportional value of the PID is just a proportional constant
        #~ multiplied by the error

        pid_p_angle = kp_angle * error_angle

        pid_p_distance = kp_distance * error_distance

        #kd'ye girmedik ihtiyac olursa bak

        #~ PID_angle = pid_p_angle + pid_d_angle;
        #~ PID_distance = pid_p_distance + pid_d_distance;
        
        if tersmi_duzmu == 1: #picam
            pwmleft,pwmright = yer(0)

        else: #webcam
            pwmleft,pwmright = yer(1)
            
        pwm_yaz_sol.ChangeDutyCycle(pwmleft)
        pwm_yaz_sag.ChangeDutyCycle(pwmright)

            
    #~ pwm_yaz_sol.ChangeFrequency(100)
    #~ pwm_yaz_sag.ChangeFrequency(100)
    
    #~ pwm_yaz_sol.ChangeDutyCycle(pwmleft)
    #~ pwm_yaz_sag.ChangeDutyCycle(pwmright)
        
        #~ pwm_yaz_sol.stop()
    return pwmleft,pwmright

