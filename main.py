import sys,os,math,time,json,urllib.request
U="https://make.fun/api/competitions/tiny-chess-01/env"
def q(p): return urllib.request.urlopen(p,timeout=5).read().decode()
def P(d): urllib.request.urlopen(U+"/move",data=json.dumps(d).encode(),headers={"Content-Type":"application/json"}).read()
B=0;W=1;K=0;Q=1;R=2;B=3;N=4;P=5
D=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
H=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
def I(b):
 b=[0]*120
 for i in range(64):
  r=i//8;f=i%8;b[r*10+f+21]=1
 return b
M=I([])
def S(f,t,p,c): return (f<<12)|(t<<6)|(p<<3)|c
def U(m): return m>>12&63,m>>6&63,m>>3&7,m&7
def A(b,s):
 if s==W: return b
 r=[0]*120
 for i,v in enumerate(b):
  if v: r[119-i]=v^1 if v<6 else v
 return r
def G(b,c):
 m=[];o=6 if c else 0;p=o+P;k=o+K
 for i,v in enumerate(b):
  if v==p:
   t=i-10 if c else i+10
   if M[t] and b[t]==0:
    if t//10 in (1,8): m+=[S(i,t,Q,0),S(i,t,R,0),S(i,t,B,0),S(i,t,N,0)]
    else: m+=[S(i,t,0,0)]
   if i%10<9 and b[t-1]>>1!=c: m+=[S(i,t-1,Q,0) if t//10 in(1,8) else S(i,t-1,0,0)]
   if i%10>2 and b[t+1]>>1!=c: m+=[S(i,t+1,Q,0) if t//10 in(1,8) else S(i,t+1,0,0)]
  if v==o+N:
   for dx,dy in H:
    t=i+dx*10+dy
    if M[t] and b[t]>>1!=c: m+=[S(i,t,0,0)]
  if v==o+B or v==o+Q:
   for dx,dy in D[4:]:
    t=i
    while 1:
     t+=dx*10+dy
     if not M[t]: break
     if b[t]: 
      if b[t]>>1!=c: m+=[S(i,t,0,0)]
      break
     m+=[S(i,t,0,0)]
  if v==o+R or v==o+Q:
   for dx,dy in D[:4]:
    t=i
    while 1:
     t+=dx*10+dy
     if not M[t]: break
     if b[t]:
      if b[t]>>1!=c: m+=[S(i,t,0,0)]
      break
     m+=[S(i,t,0,0)]
  if v==o+K:
   for dx,dy in D:
    t=i+dx*10+dy
    if M[t] and b[t]>>1!=c: m+=[S(i,t,0,0)]
 return m
V=[0,100,500,320,330,900,20000]
def E(b):
 s=0
 for v in b:
  if v: s+=V[v&7]*(1 if v<6 else -1)
 return s
def N(b,m,c):
 b=b[:];f,t,p,_=U(m);pc=b[f];b[f]=0
 if p: b[t]=6+c if c else 6+W
 else: b[t]=pc
 return b
def D(b,c,d,a,b_,k):
 if d==0: return E(b) if c else -E(b)
 m=G(b,c)
 if not m: return -20000 if k else 20000
 for mv in m:
  nb=N(b,mv,c)
  v=-D(nb,not c,d-1,-b_,-a,True)
  if v>a: a=v
  if a>=b_: return a
 return a
def B(b,c):
 m=G(b,c)
 if not m: return None
 bv=-30000;bm=None
 for mv in m:
  nb=N(b,mv,c)
  v=-D(nb,not c,3,-30000,30000,True)
  if v>bv: bv=v;bm=mv
 return bm
def U(f,t): return chr(97+f%10-2)+str(8-f//10+2)+chr(97+t%10-2)+str(8-t//10+2)
def L(s):
 b=[0]*120
 for i in range(64): b[i//8*10+i%8+21]=0
 p={"r":4,"n":2,"b":3,"q":1,"k":0,"p":5,"R":10,"N":8,"B":9,"Q":7,"K":6,"P":11}
 for i,ch in enumerate(s.split()[0]):
  if ch=="/": continue
  if ch.isdigit(): i+=int(ch)-1
  else: b[i//8*10+i%8+21]=p[ch]+(0 if ch.islower() else 6); i+=1
 return b
def main():
 g=q(U+"/game").strip()
 b=L(g) if g else [0]*120
 c=W
 while 1:
  m=B(b,c)
  if not m: break
  f,t,_,_=U(m)
  P({"game":g,"move":U(f,t)})
  b=N(b,m,c)
  c=not c
  time.sleep(0.1)
if __name__=="__main__": main()
