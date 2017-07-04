#include "mpc-master/mpc.h"

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

int main(int argc, char** argv) {

	// 创建一些解析器
	mpc_parser_t* Number    = mpc_new("number");

	mpc_parser_t* Operator 	= mpc_new("operator");

	mpc_parser_t* Expr	= mpc_new("expr"); 

	mpc_parser_t* Lispy 	= mpc_new("lispy");

	/*
		Program		------	输入由操作符，一个或者多个表达式组成
		Expresssion	------	由一个数字或者 '(' 操作符+其它的表达式 ')'
		Operation	------	'+'，'-'，'*'，或者 '/'
		Number		------	由0－9数字组成，也可以用'-'来表示负数

		正则表达式的基础规则：
			.	------	可以匹配任何字母
			a	------	只能匹配字符 a
			[abcdef]------	可以匹配在字符串中的任意一个字母
			[a-f]   ------	可以匹配在 a-f 里的任意一个字母
			a?	------	字符 a 是可要可不要
			a*	------	可以匹配0个到多个 a
			a+	------	可以匹配1个到多个 a
			^	------	表示匹配的开始符号
			$	------	表示匹配的结束符号
	*/
	mpca_lang(MPCA_LANG_DEFAULT, "number: /-?[0-9]+/ ; operator: '+' | '-' | '*' | '/' ; expr: <number> | '(' <operator> <expr>+ ')' ; lispy: /^/ <operator> <expr>+ /$/ ;", Number, Operator, Expr, Lispy);

	puts("Lispy Version 0.2");
	puts("Press Ctrl+c to Exit\n");

	while (1) {

		char* input = readline("lispy> ");
		add_history(input);
		
		/* 
			尝试解析用户的输入，mpc_parse 函数将结合 Lispy，输入的字符串为 input 。
			这段代码将解析的结果保存在 r 里，如果解析成功则返回1，失败为0。
		*/
		mpc_result_t r;

		if (mpc_parse("<stdin>", input, Lispy, &r)) {
			/* On Success Print the AST */
			mpc_ast_print(r.output);
			mpc_ast_delete(r.output);
		} else {
			/* Otherwise Print the Error */
			mpc_err_print(r.error);
			mpc_err_delete(r.error);
		}
	
		free(input);

	}

	mpc_cleanup(4, Number, Operator, Expr, Lispy);

	return 0;
	
}
