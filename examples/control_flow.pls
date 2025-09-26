// if-elif-else statement
bool is_positive(int x):
    if x > 0:
        return true;
    elif x == 0:
        return false;
    else:
        return false;

// while loop
int sum_to(int n):
    int total = 0;
    while n > 0:
        total = total + n;
        n = n - 1;
    return total;
