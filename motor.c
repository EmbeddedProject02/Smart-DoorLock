#include <SoftwareSerial.h> //시리얼 통신 라이브러리 호출

int blueTx=7;   //Tx (블투 보내는핀 설정)
int blueRx=8;   //Rx (블투 받는핀 설정)
int RELAY = 3; //릴레이 Signal 핀 설정 ,
 
SoftwareSerial mySerial(blueRx, blueTx);  //시리얼 통신을 위한 객체선언

void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(RELAY, OUTPUT);
}

void loop()
{
  
   int cmd;
//   int cmd2;

   if(mySerial.available()){
    cmd=mySerial.read();
    Serial.print(cmd); 
    if(cmd == 48) //메시지 0 수신시
    { 
      digitalWrite(RELAY, HIGH);
      delay(10000);
      digitalWrite(RELAY, LOW); 
      delay(500);
    }
   }
   
   if(mySerial2.available()){
    cmd2=mySerial2.read();
    Serial.print(cmd2); 
    if(cmd2 == 48) //메시지 0 수신시
    { 
      digitalWrite(RELAY, HIGH);
      delay(500);      
      digitalWrite(RELAY, LOW); 
      delay(500);
    }
   }  
}