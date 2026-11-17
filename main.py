import sys,json,urllib.request as u
U="http://localhost:8081"
def Q(p):return json.loads(u.urlopen(u.Request(p,data=b"{}",headers={"Content-Type":"application/json"},method="POST"),timeout=5).read().decode())
def M(d):return json.loads(u.urlopen(u.Request(U+"/move",data=json.dumps(d).encode(),headers={"Content-Type":"application/json"},method="POST"),timeout=5).read().decode())
V=[20000,900,500,330,320,100,0];D=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)];H=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)];P={"r":0,"n":3,"b":4,"q":1,"k":5,"p":2,"R":6,"N":9,"B":10,"Q":7,"K":11,"P":8}
def E(b,c):
 s=0;k=-1
 for i,v in enumerate(b):
  if v>=0:
   p=v%6;x=V[p]
   if p in(3,4):x+=max(0,4-abs((i&7)-3.5)-abs((i>>4)-3.5))*10
   if p==5 and(v<6)==c:k=i
   s+=x*(1 if v<6 else-1)
 s=s if c else-s
 if k>=0:
  kf,kr=k&7,k>>4
  for df in(-1,0,1):
   f=kf+df
   if 0<=f<8:
    for r in range(kr+1,8)if c else range(kr-1,-1,-1):
     v=b[16*r+f]
     if v>=0:
      if v%6==2 and(v<6)==c:s+=20
      break
 return s
def L(f):
 b=[-1]*128;i=0
 for c in f.split()[0]:
  if c=="/":continue
  if c.isdigit():i+=int(c)
  else:s=16*(i//8)+(i%8);b[s]=P[c];i+=1
 return b
def G(b,c):
 m=[];a=[]
 for s in range(128):
  v=b[s]
  if v<0 or(v<6)!=c:continue
  p=v%6
  if p==2:
   d=-16 if c else 16;t=s+d
   if 0<=t<128 and b[t]==-1:m+=[(s,t,0)]
   for dc in(-1,1):
    t=s+d+dc
    if 0<=t<128 and b[t]>=0 and(b[t]<6)!=c and b[t]%6!=5:a+=[(s,t,0)]
  elif p==3:
   for dx,dy in H:
    t=s+dx+dy*16
    if 0<=t<128 and(s&7)-dx in range(8)and b[t]>=0 and(b[t]<6)!=c and b[t]%6!=5:a+=[(s,t,0)]
  elif p in(4,1):
   for dx,dy in D[4:]:
    t=s
    while 1:
     t+=dx+dy*16
     if not(0<=t<128 and(t&7)-dx in range(8)):break
     if b[t]>=0:
      if(b[t]<6)!=c and b[t]%6!=5:a+=[(s,t,0)]
      break
     m+=[(s,t,0)]
  if p in(0,1):
   for dx,dy in D[:4]:
    t=s
    while 1:
     t+=dx+dy*16
     if not(0<=t<128 and(t&7)-dx in range(8)):break
     if b[t]>=0:
      if(b[t]<6)!=c and b[t]%6!=5:a+=[(s,t,0)]
      break
     m+=[(s,t,0)]
  if p==5:
   for dx,dy in D:
    t=s+dx+dy*16
    if 0<=t<128 and(t&7)-dx in range(8)and b[t]>=0 and(b[t]<6)!=c and b[t]%6!=5:a+=[(s,t,0)]
 return a+m
def K(b,c):
 k=5 if c else 11
 for i,v in enumerate(b):
  if v==k:return i
 return-1
def C(b,c):
 k=K(b,not c)
 if k<0:return 0
 o=not c
 for s in range(128):
  v=b[s]
  if v<0 or(v<6)!=o:continue
  p=v%6
  if p==2:
   d=-16 if o else 16
   for dc in(-1,1):
    if k==s+d+dc:return 1
  elif p==3:
   for dx,dy in H:
    if k==s+dx+dy*16 and(s&7)-dx in range(8):return 1
  elif p in(4,1):
   for dx,dy in D[4:]:
    t=s
    while 1:
     t+=dx+dy*16
     if not(0<=t<128 and(t&7)-dx in range(8)):break
     if t==k:return 1
     if b[t]>=0:break
  if p in(0,1):
   for dx,dy in D[:4]:
    t=s
    while 1:
     t+=dx+dy*16
     if not(0<=t<128 and(t&7)-dx in range(8)):break
     if t==k:return 1
     if b[t]>=0:break
  if p==5:
   for dx,dy in D:
    t=s+dx+dy*16
    if 0<=t<128 and(t&7)-dx in range(8)and t==k:return 1
 return 0
def N(b,m,c):b=b[:];f,t,pr=m;pc=b[f];b[f]=-1;b[t]=6+c if pr else pc;return b
def S(b,c,d,a,b_):
 if d==0:return E(b,c)
 m=G(b,c)
 if not m:return-2e4 if C(b,c)else 0
 for mv in m:
  v=-S(N(b,mv,c),not c,d-1,-b_,-a)
  if v>a:a=v
  if a>=b_:return a
 return a
def B(b,c,lm):
 bv=-3e4;bu=None
 for u in lm:
  f=16*(8-int(u[1]))+(ord(u[0])-97);t=16*(8-int(u[3]))+(ord(u[2])-97)
  nb=N(b,(f,t,0),c);v=-S(nb,not c,2,-3e4,3e4)+100*C(nb,not c)
  if v>bv:bv=v;bu=u
 return bu
def main():
 g=Q(U+"/game")
 while g.get("game",0)<=6:
  gn=g["game"];c=g["colour"]=="white"
  while g.get("status")!="over":
   b=L(g["fen"]);lm=g.get("legal_moves",[]);uci=B(b,c,lm)
   if not uci:break
   sys.stderr.write(f"game {gn} move {uci}\n");g=M({"game":gn,"move":uci})
  g=Q(U+"/game")
  if g.get("status")=="done":break
if __name__=="__main__":main()