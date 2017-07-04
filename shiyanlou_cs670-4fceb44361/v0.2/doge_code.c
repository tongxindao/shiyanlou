#include "mpc-master/mpc.h"

int main(int argc, char** argv) {

	//建立解析器 Ajective 来认识这个描述
	mpc_parser_t* Ajective = mpc_or(4,
		mpc_sym("wow"), mpc_sym("many"),
		mpc_sym("so"), mpc_sym("such"));

	//建立解析器 'Noun' 去描述事物
	mpc_parser_t* Noun = mpc_or(5,
		mpc_sym("lisp"), mpc_sym("language"),
		mpc_sym("book"), mpc_sym("build"),
		mpc_sym("c"));

	//短语
	mpc_parser_t* Phrase = mpc_and(2, mpcf_strfold, 
				Ajective, Noun, free);

	mpc_parser_t* Doge = mpc_many(mpcf_strfold, Phrase);

	//在这里做一些解析
	
	mpc_delete(Doge);

	return 0;

}
