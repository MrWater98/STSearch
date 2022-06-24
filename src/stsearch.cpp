#include<iostream>
#include "ivl_target.h"

using namespace std;


extern "C" int target_design(ivl_design_t design) { 
	cout<<"Hello World"<<endl;
	return 0;
}