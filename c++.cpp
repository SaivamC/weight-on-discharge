#include<bits/stdc++.h>
using namespace std;
 string dtob(long long int num, string &s)
  {
      if(num<2)
      {
          s+=to_string(num);
          return s;
      }
      s+=to_string(num%2);
      num=num>>1;
      return dtob(num,s);
      
  }
int main()
{
string s="";
long long int num = 1000000000;
dtob(num,s);
reverse(s.begin(),s.end());
cout<<s<<endl;
}
