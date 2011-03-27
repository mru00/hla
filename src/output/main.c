
#include <avr.h>


/*not implemented : <class 'modBase.Target'>*/



static u8 counter;

ISR(INT0) {
    counter = 0;
}

void main() {


        counter = 0;
      direction = low;
/*not implemented : <class 'modLowlevel.CallC'>*/


  for(;;) {

      if ( pulse == high ) {
          counter++;
          while ( pulse == high ) {
              counter = 1;
          }
      }


      if ( counter == 100 ) {
          direction = ! direction;
          counter = 0;
      }


      if ( counter == 10 ) {
          direction = ! direction;
          counter = 0;
      }

  }

}

