#include <stdlib.h>
#include <stdio.h>
void change2(int *a1, int a2)
{
  int v3; // [esp+Ch] [ebp-18h]
  int v4; // [esp+10h] [ebp-14h]
  int v5; // [esp+18h] [ebp-Ch]
  int v6; // [esp+1Ch] [ebp-8h]

  v4 = -1;
  v3 = -1 - a2 + 1;
  v6 = 1231;
  v5 = a2 + 1231;
  while ( v3 )
  {
    ++v6;
    --*a1;
    --v3;
    --v5;
  }
  while ( v4 )
  {
    --v5;
    ++*a1;
    --v4;
  }
  ++*a1;
}


void change(int *a1, int a2)
{
  int v3; // [esp+Ch] [ebp-1Ch]
  int v4; // [esp+14h] [ebp-14h]
  int v5; // [esp+18h] [ebp-10h]
  int v6; // [esp+18h] [ebp-10h]
  int v7; // [esp+1Ch] [ebp-Ch]
  int v8; // [esp+20h] [ebp-8h] BYREF

  v4 = *a1;
  v5 = a2;
  v3 = -1;
  v8 = 0;
  v7 = a2 * v4;
  int *p=v8;
  while ( a2 )
  {
    v6 = v7 * v4;
    change2(p, *a1);
    ++v7;
    --a2;
    v5 = v6 - 1;
  }
  while ( v3 )
  {
    ++v7;
    ++*a1;
    --v3;
    --v5;
  }
  ++*a1;
  *a1 = v8;
}

int main()
{
   	int  v120[32];
   	int i;
   	for(i=0;i<32;i++)
   		v120[i]=1;
   	
    return 0;
}
