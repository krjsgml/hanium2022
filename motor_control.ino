#include <SoftwareSerial.h>
#define RXD 8
#define TXD 7
SoftwareSerial bluetooth(RXD, TXD);

#define Dir_linear  12
#define SPD 11
#define BRK 13

// 오른쪽
int dir1 = 2; // High면 후진?
int dir2 = 3; // High면 전진
// 왼쪽
int dir3 = 4; // High면 후진?
int dir4 = 5; // High면 전진

int pwm1 = 9;
int pwm2 = 10;
char sig = '0';
int wheel_SPD;
int wheel_R_SPD;
  
void setup() {
 Serial.begin(9600);
 bluetooth.begin(9600);
 pinMode(dir1, OUTPUT);
 pinMode(dir2, OUTPUT);
 pinMode(dir3, OUTPUT);
 pinMode(dir4, OUTPUT);
 pinMode(pwm1, OUTPUT);
 pinMode(pwm2, OUTPUT);
 pinMode(Dir_linear, OUTPUT);
 pinMode(SPD, OUTPUT);  
 pinMode(BRK, OUTPUT);
 digitalWrite(BRK, LOW);
 digitalWrite(Dir_linear, LOW);
 analogWrite(SPD, 255);
 delay(10000);
 analogWrite(SPD, 0);

}

void loop() {

   if (bluetooth.available()) {
     sig = bluetooth.read();
     Serial.write(sig);
 
    if (sig == '1') {
      analogWrite(pwm1, 0);
      analogWrite(pwm2, 0);
      digitalWrite(Dir_linear, LOW);
      analogWrite(SPD, 255);
      delay(7000);
      digitalWrite(Dir_linear, LOW);
      analogWrite(SPD, 0);
      Serial.println("up");
    }
    
    else if (sig == '2') {
      analogWrite(pwm1, 0);
      analogWrite(pwm2, 0);
      digitalWrite(Dir_linear, HIGH);
      analogWrite(SPD, 255);
      delay(7000);   
      digitalWrite(Dir_linear, HIGH);
      analogWrite(SPD, 0);
      Serial.println("down");
    }
    
    else if (sig == 'c'){
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 50);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 50);
    }
    
    else if (sig == 'v'){
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 50);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 30);
    }
    
    else if (sig == 'x'){ 
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 30);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 50);
    }

    else if (sig == 'e'){
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 30);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 30);
    }
    
    else if (sig == 'r'){
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 30);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 0);
    }
    
    else if (sig == 'w'){ 
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 0);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 30);
    }

    else if (sig == 'd'){
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 40);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 40);
    }
    
    else if (sig == 'f'){
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 40);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 25);
    }
    
    else if (sig == 's'){ 
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, HIGH);
      analogWrite(pwm1, 25);
       
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, HIGH);
      analogWrite(pwm2, 40);
    }

     else if (sig == 't'){ 
      digitalWrite(dir1, HIGH);
      digitalWrite(dir2, LOW);
      analogWrite(pwm1, 30);
       
      digitalWrite(dir3, HIGH);
      digitalWrite(dir4, LOW);
      analogWrite(pwm2, 30);
    }
    
      else if (sig == 'q'){ 
      digitalWrite(dir1, LOW);
      digitalWrite(dir2, LOW);
      analogWrite(pwm1, 0);
     
      digitalWrite(dir3, LOW);
      digitalWrite(dir4, LOW);
      analogWrite(pwm2, 0);
    }

  }
  if (Serial.available()) {
    bluetooth.write(Serial.read());
  }
}
