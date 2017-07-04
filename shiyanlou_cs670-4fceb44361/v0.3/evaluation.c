#include "../v0.2/mpc-master/mpc.h"

#ifdef _WIN32

static char buffer[2048];

char* readline(char* prompt) {

        fputs(prompt, stdout);
        fgets(buffer, 2048, stdin);
        char* cpy = malloc(strlen(buffer)+1);
        strcpy(cpy, buffer);
        cpy[strlen(cpy)-1] = '\0'
        return cpy;

}

void add_history(char* unused) {}

#else
#include <editline/readline.h>
#include <editline/history.h>
#endif

/* 根据输入操作符与数字来返回计算结果 */
long eval_op(long x, char* op, long y) {
	
	if(strcmp(op, "+") == 0){ return x + y; }
	if(strcmp(op, "-") == 0){ return x - y; }
	if(strcmp(op, "*") == 0){ return x * y; }
	if(strcmp(op, "/") == 0){ return x / y; }
	return 0;

}

/*
	atoi	------	将一个 char* 转为 long 型
	strcmp	------	输入两个字符串，如果相等返回0
	strstr	------	输入两个字符串，如果第二个是第一个的子串，就返回首次出现的下标，如果第二个没有出现在第一个字符串内就输出0

	demo:
		lispy> * 10 (+ 1 51)
		>
		  regex
		  operator|char:1:1 '*'
		  expr|number|regex:1:3 '10'
		  expr|>
		    char:1:6 '('
		    operator|char:1:7 '+'
		    expr|number|regex:1:9 '1'
		    expr|number|regex:1:11 '51'
		    char:1:13 ')'
		  regex
*/
long eval(mpc_ast_t* t) {

	/* 如果标记为数字直接返回 */
	if (strstr(t->tag, "number")) {
		return atoi(t->contents);
	}

	/* 操作符为第二个子节点 */
	char* op = t->children[1]->contents;

	/* 结果存储在第三个节点 */
	long x = eval(t->children[2]);

	/* 迭代余下节点 */
	int i = 3;

	while (strstr(t->children[i]->tag, "expr")) {
		x = eval_op(x, op, eval(t->children[i]));
		i++;
	}

	return x;

}

int main(int argc, char** argv) {

	mpc_parser_t* Number    = mpc_new("number");

	mpc_parser_t* Operator 	= mpc_new("operator");

	mpc_parser_t* Expr	= mpc_new("expr"); 

	mpc_parser_t* Lispy 	= mpc_new("lispy");

	mpca_lang(MPCA_LANG_DEFAULT, "number: /-?[0-9]+/ ; operator: '+' | '-' | '*' | '/' ; expr: <number> | '(' <operator> <expr>+ ')' ; lispy: /^/ <operator> <expr>+ /$/ ;", Number, Operator, Expr, Lispy);

	puts("Lispy Version 0.3");
	puts("Press Ctrl+c to Exit\n");

	while (1) {

		char* input = readline("lispy> ");
		add_history(input);

		mpc_result_t r;

		if (mpc_parse("<stdin>", input, Lispy, &r)) {
			long result = eval(r.output);
			printf("%li\n", result);
			mpc_ast_delete(r.output);
		} else {
			mpc_err_print(r.error);
			mpc_err_delete(r.error);
		}
	
		free(input);

	}

	mpc_cleanup(4, Number, Operator, Expr, Lispy);

	return 0;
	
}

/*
	mpc_ast_t* a = r.output;
	printf("Tag: %s\n", a->tag);
	printf("Contents: %s\n", a->contents);
	printf("Number of children: %i\n", a->children_num);

	mpc_ast_t* c0 = a->children[0];
	printf("First Child Tag: %s\n", c0->tag);
	printf("First Child Contents: %s\n", c0->contents);
	printf("First Child Number of children: %i\n", c0->children_num);

	int number_of_nodes(mpc_ast_t* t) {

		if (t->children_num == 0) { return 1;}
		if (t->children_num >= 1) { 
			int total = 1;
			for (int i=0;i<t->children_num;i++) {
				total = total + number_of_nodes(t->children[i]);	
			}
			return total;
		}
		return 0;

	}
	long result = eval(r.output);
	printf("%li\n", result);
	mpc_ast_delete(r.output);
*/
