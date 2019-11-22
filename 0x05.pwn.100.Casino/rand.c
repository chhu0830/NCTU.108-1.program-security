#include <stdio.h>
#include <stdlib.h>


int main(int argc, const char *argv[]) {
    srand(atoi(argv[1]));
    for (int i = 0; i < 6; i++) {
        printf("%d\n", rand() % 100);
    }
    return 0;
}
