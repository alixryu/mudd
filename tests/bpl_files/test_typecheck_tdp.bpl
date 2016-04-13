/* A program to test top down pass of typechecker*/

int x;
string y;
int z[10];
string *k;

int first(void) {
    int x; int y;
    {
        string j; int e[9];
    }
}

int second(int a, string b, int *c) {
    string at[2];

    if(a > 3) {
        int inif;
        x = a * 2;
    } else {
        string inelse;
        x = a / 2;
    }

    while(x != 10) {
        string inwhile;
        x = x + 1;
    }
    x = first();
    x = second(a, b, *c);
    return x;
}

void third(void) {}
