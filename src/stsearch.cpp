#include<iostream>
#include "ivl_target.h"

using namespace std;


extern "C" void target_design(ivl_design_t design) { 
	cout<<"Hello World"<<endl;
}