Version 0.1 ------ libedit-dev prompt.c
Version 0.2 ------ mpc parsing.c
Version 0.3 ------ gcc -std=c99 -Wall evaluation.c ./mpc/mpc.c -ledit -lm -o evaluation
Version 0.4 ------ gcc -std=c99 -Wall error_handling.c ./mpc/mpc.c -ledit -lm -o error_handling
Version 0.5 ------ gcc -std=c99 -Wall s_expression.c ./mpc/mpc.c -ledit -lm -o s_expression
Version 0.6 ------ gcc -std=c99 -Wall q_expression.c ./mpc/mpc.c -ledit -lm -o q_expression
Version 0.7 ------ gcc -std=c99 -Wall variable.c ./mpc/mpc.c -ledit -lm -o variable
Version 0.8 ------ gcc -std=c99 -Wall functions.c ./mpc/mpc.c -ledit -lm -o functions
Version 0.9 ------ gcc -std=c99 -Wall conditions.c ./mpc/mpc.c -ledit -lm -o conditions
Version 1.0 ------ gcc -std=c99 -Wall string.c ./mpc/mpc.c -ledit -lm -o string
