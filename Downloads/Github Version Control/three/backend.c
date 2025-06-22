#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int generate_otp() {
    // Seed the random number generator with current time
    srand(time(NULL));
    
    // Generate random number between 100 and 999
    int otp = 100 + (rand() % 900);
    
    return otp;
}

// Example usage in main function
int main() {
    int otp = generate_otp();
    printf("Your 3-digit OTP is: %d\n", otp);
    return 0;
}