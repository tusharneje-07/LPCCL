#include <stdio.h>

int main() {
    int a = 10, b = 20;
    float result = 0.0;

    if (a < b && b > 0) {
        result = a + b * 2;
        printf("Sum is: %d\n", result);
    }

    for (int i = 0; i < 5; i++) {
        printf("Value: %d\n", i);
    }

    while (a <= b) {
        a = a + 1;
    }

    return 0;
}