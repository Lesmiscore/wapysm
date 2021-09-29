#include <math.h>

void print_console(double);

__attribute__((visibility("default")))
void gauss_legendre(int iterations){
  double ax = 1.;
  double bx = 1. / sqrt(2.);
  double tx = 0.25;

  for(int i = 0; i < iterations; i++){
    double ax1 = (ax + bx) / 2;
    double bx1 = sqrt(ax * bx);
    double tx1 = tx - (1 << i) * pow(ax - ax1, 2);
    ax = ax1; bx = bx1; tx = tx1;
  }

  print_console(pow(ax + bx, 2) / (4 * tx));
}

void _start(){
  print_console(42.);
}
