#include<bits/stdc++. h>
using namespace std;
 string dtob(int &num, string &s)
  {
      if(num<2)
      {
          s+=tostring(num);
          return s;
      }
      s+=tostring(num%2);
      num=num>>1;
      return dtob(num,s);
      
  }
int main()
{
string s="";
int n=70;
dtob(num,s);
cout<<s<<endl;
}
