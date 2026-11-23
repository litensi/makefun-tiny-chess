import json,os,sys
from urllib.request import Request,urlopen
a=os.environ["MAKEFUN_ENV_URL"]
def b(c,d):
 e=Request(a+c,json.dumps(d).encode(),{"content-type":"application/json"})
 return json.load(urlopen(e))
f=[7]*144
g=f
h=0
i=0
j=-1
k=0
l=[]
m=0
n=[]
o=[]
p=0
q=""
r=[0,0]
s=0
t=0
u=150000
v={}
w=[[0,0]for x in range(80)]
y=[0]*16384
z=[0,100,320,330,500,900,0]
A=0x2545F491
B=[]
for x in range(2048):
 A^=(A<<13)&0xFFFFFFFF
 A^=A>>17
 A^=(A<<5)&0xFFFFFFFF
 B.append(A&0xFFFFFFFF)
C=[0]*2048
for D in range(128):
 if D&0x88:
  continue
 E=D&7
 F=D>>4
 for G in(0,1):
  H=F if G==0 else 7-F
  for I in range(1,7):
   if I==1:
    J=H*8+(10 if 2<E<5 else 0)+(H*4 if H>4 else 0)
   elif I<4:
    J=30-5*abs(2*E-7)-5*abs(2*H-7)
   elif I==4:
    J=12*(H==6)
   elif I==5:
    J=12-3*abs(2*E-7)-2*abs(2*H-7)
   else:
    J=24 if H<1 and 2<E<6 else-6*(2<E<5 and 2<H<6)
   C[(D<<4)|I|(G<<3)]=J
K=[D for D in range(128)if not D&0x88]
L=(33,31,18,14,-14,-18,-31,-33)
M=(17,16,15,1,-1,-15,-16,-17)
N=(17,15,-15,-17)
O=(16,1,-1,-16)
def P(Q):
 global g,f,h,i,j,k,m,l,n,r,q
 q=Q
 R=Q.split()
 f=[7]*144
 g=f
 for D in range(128):
  if not D&0x88:
   g[D]=0
 F=7
 E=0
 for G in R[0]:
  if G=="/":
   F-=1
   E=0
  elif G.isdigit():
   E+=int(G)
  else:
   g[(F<<4)|E]=" pnbrqk".index(G.lower())+(0 if G.isupper()else 8)
   E+=1
 f[:]=g
 h=0 if R[1]=="w" else 1
 for D in range(128):
  if not D&0x88 and g[D]==6:
   r[0]=D
  elif not D&0x88 and g[D]==14:
   r[1]=D
 i=0
 for S,G in enumerate("KQkq"):
  if G in R[2]:
   i|=1<<S
 j=-1 if R[3]=="-" else((int(R[3][1])-1)<<4)|"abcdefgh".index(R[3][0])
 k=0
 m=0
 for D in range(128):
  if not D&0x88 and g[D]:
   m^=B[(D<<4)|g[D]]
 if h:
  m^=0x5A5A5A5A
 v.clear()
 l=[]
 n=o[:]+[m]
def T(U,V):
 g=f
 R=1|(V<<3)
 W=-16 if V==0 else 16
 if g[U+W-1]==R or g[U+W+1]==R:
  return 1
 for X in L:
  if not(U+X)&0x88 and g[U+X]==R+1:
   return 1
 for X in M:
  if not(U+X)&0x88 and g[U+X]==R+5:
   return 1
 for Y,Z,aa in((N,2,4),(O,3,4)):
  for X in Y:
   I=U+X
   while not I&0x88:
    D=g[I]
    if D:
     if D==R+Z or D==R+aa:
      return 1
     break
    I+=X
 return 0
def bb(cc,dd=0,ee=0):
 g=f
 ff=h
 gg=[]
 hh=16 if ff==0 else-16
 ii=7 if ff==0 else 0
 for U in K:
  R=g[U]
  if not R or R>>3!=ff:
   continue
  I=R&7
  if I==1:
   jj=U+hh
   if not jj&0x88 and not g[jj]:
    if jj>>4==ii:
     gg+=[U<<7|jj|kk<<14 for kk in(5,4,3,2)]
    elif not cc:
     gg.append(U<<7|jj)
     if(U>>4)==(1 if ff==0 else 6)and not g[jj+hh]:
      gg.append(U<<7|jj+hh)
   for jj in(U+hh-1,U+hh+1):
    if jj&0x88:
     continue
    D=g[jj]
    if D and D>>3!=ff:
     if jj>>4==ii:
      gg+=[U<<7|jj|kk<<14 for kk in(5,4,3,2)]
     else:
      gg.append(U<<7|jj)
    elif jj==j:
     gg.append(U<<7|jj)
  else:
   Y=L if I==2 else M if I==6 else N if I==3 else O if I==4 else N+O
   ll=I!=2 and I!=6
   for W in Y:
    jj=U+W
    while not jj&0x88:
     D=g[jj]
     if D:
      if D>>3!=ff:
       gg.append(U<<7|jj)
      break
     if not cc:
      gg.append(U<<7|jj)
     if not ll:
      break
     jj+=W
  if I==6 and not cc:
   if ff==0:
    if i&1 and not g[5]and not g[6]and not T(4,1)and not T(5,1):
     gg.append(4<<7|6)
    if i&2 and not g[3]and not g[2]and not g[1]and not T(4,1)and not T(3,1)and not T(2,1):
     gg.append(4<<7|2)
   else:
    if i&4 and not g[117]and not g[118]and not T(116,0)and not T(117,0):
     gg.append(116<<7|118)
    if i&8 and not g[115]and not g[114]and not g[113]and not T(116,0)and not T(115,0)and not T(114,0):
     gg.append(116<<7|114)
 mm=[]
 nn=[]
 oo=w[ee&63]
 for pp in gg:
  jj=pp&0x7F
  qq=g[jj]
  rr=pp>>14
  if rr or qq:
   mm.append((z[qq&7]*9+(rr<<8)-z[g[(pp>>7)&0x7F]&7],pp))
  elif pp==oo[0]:
   nn.append(pp)
  else:
   nn.append(pp)
 mm.sort(reverse=True)
 F=[pp for x,pp in mm]
 if dd:
  F.insert(0,dd)
 for pp in oo:
  if pp and pp not in F and g[(pp>>7)&0x7F]and(g[(pp>>7)&0x7F]>>3)==ff:
   F.append(pp)
 for pp in gg:
  if not(pp>>14)and not g[pp&0x7F]and pp not in F:
   F.append(pp)
 return F
def ss(pp):
 global h,i,j,k,m
 g=f
 tt=(pp>>7)&0x7F
 jj=pp&0x7F
 uu=g[tt]
 vv=g[jj]
 rr=pp>>14
 ff=h
 hh=16 if ff==0 else-16
 ww=-1
 if(uu&7)==1 and jj==j and not vv:
  ww=jj-hh
 l.append((pp,vv,ww,i,j,k,m,1))
 m^=B[(tt<<4)|uu]^B[(jj<<4)|(rr|(ff<<3)if rr else uu)]
 g[tt]=0
 g[jj]=(rr|(ff<<3))if rr else uu
 if(uu&7)==6:
  r[ff]=jj
 if ww>=0:
  m^=B[(ww<<4)|g[ww]]
  g[ww]=0
 elif vv:
  m^=B[(jj<<4)|vv]
 if(uu&7)==6 and abs(jj-tt)==2:
  Z=tt+3 if jj>tt else tt-4
  aa=tt+1 if jj>tt else tt-1
  m^=B[(Z<<4)|g[Z]]^B[(aa<<4)|g[aa]]
  g[aa]=g[Z]
  g[Z]=0
 if tt==4:
  i&=12
 elif tt==0:
  i&=13
 elif tt==7:
  i&=14
 elif tt==116:
  i&=3
 elif tt==112:
  i&=7
 elif tt==119:
  i&=11
 if jj==0:
  i&=13
 elif jj==7:
  i&=14
 elif jj==116:
  i&=3
 elif jj==112:
  i&=7
 elif jj==119:
  i&=11
 if(uu&7)==1 or vv:
  k=0
 else:
  k+=1
 j=(tt+jj)>>1 if(uu&7)==1 and abs(jj-tt)==32 else-1
 h=ff^1
 m^=0x5A5A5A5A
 if T(r[ff],h):
  l[-1]=(pp,vv,ww,i,j,k,m,0)
  xx()
  return 0
 n.append(m)
 return 1
def xx():
 global h,i,j,k,m
 g=f
 pp,vv,ww,yy,zz,AA,BB,CC=l.pop()
 if pp<0:
  h^=1
  i=yy
  j=zz
  k=AA
  m=BB
  if CC:
   n.pop()
  return
 tt=(pp>>7)&0x7F
 jj=pp&0x7F
 rr=pp>>14
 uu=(1|((h^1)<<3))if rr else g[jj]
 g[tt]=uu
 g[jj]=vv
 if(uu&7)==6:
  r[h^1]=tt
 if ww>=0:
  g[ww]=1|(h<<3)
 if(uu&7)==6 and abs(jj-tt)==2:
  Z=tt+3 if jj>tt else tt-4
  aa=tt+1 if jj>tt else tt-1
  g[Z]=g[aa]
  g[aa]=0
 i=yy
 j=zz
 k=AA
 m=BB
 h=h^1
 if CC:
  n.pop()
def DD():
 g=f
 EE=0
 FF=[0]*8
 GG=[0]*8
 for D in K:
  R=g[D]
  if R==1:
   FF[D&7]+=1
  elif R==9:
   GG[D&7]+=1
 HH=0
 II=[0,0]
 for D in K:
  R=g[D]
  if not R:
   continue
  if R>14 or R==7:
   continue
  I=R&7
  E=D&7
  F=D>>4
  if I==5:
   HH+=1
  if I==3:
   II[R>>3]+=1
  if R>>3:
   if I==1:
    EE-=z[1]+C[(D<<4)|R]
    if FF[E]==0 and FF[E-1 if E else 0]==0 and FF[E+1 if E<7 else 7]==0:
     EE-=16+8*(7-F)
    if GG[E]>1:
     EE+=10
   else:
    EE-=z[I]+C[(D<<4)|R]
    if I==4 and not FF[E]and not GG[E]:
     EE-=12
  else:
   if I==1:
    EE+=z[1]+C[(D<<4)|R]
    if GG[E]==0 and GG[E-1 if E else 0]==0 and GG[E+1 if E<7 else 7]==0:
     EE+=16+8*F
    if FF[E]>1:
     EE-=10
   else:
    EE+=z[I]+C[(D<<4)|R]
    if I==4 and not FF[E]and not GG[E]:
     EE+=12
 EE+=II[0]*28-II[1]*28
 if HH<2:
  EE+=7*(3-abs((r[0]&7)-4))
  EE-=7*(3-abs((r[1]&7)-4))
 elif HH>3:
  for G in(0,1):
   JJ=r[G]&7
   KK=0
   for LL in(-1,0,1):
    MM=JJ+LL
    if MM<0 or MM>7:
     continue
    if(FF if G==0 else GG)[MM]==0:
     KK-=10
    elif g[r[G]+(16 if G==0 else-16)+LL]==1|(G<<3):
     KK+=9
    elif g[r[G]+(32 if G==0 else-32)+LL]==1|(G<<3):
     KK+=5
   EE+=KK if G==0 else-KK
 return EE+10 if h==0 else 10-EE
def NN(OO,PP,W):
 global s
 s+=1
 QQ=T(r[h],h^1)
 J=DD()
 if not QQ:
  if J>=PP or W>8:
   return J
  if J>OO:
   OO=J
 for pp in bb(0 if QQ else 1,0,W):
  if not QQ and J+z[g[pp&0x7F]&7]+120<OO:
   continue
  if not ss(pp):
   continue
  EE=-NN(-PP,-OO,W+1)
  xx()
  if EE>=PP:
   return EE
  if EE>OO:
   OO=EE
 if QQ and OO==-30000:
  return-30000+W
 return OO
def RR(W,OO,PP,ee):
 global s,t,m,j,h,i,k,n
 s+=1
 if s>u or t:
  t=1
  return 0
 if ee and n and m!=n[-1]and m in n:
  return-4
 dd=v.get(m)
 if dd and dd[0]>=W:
  SS=dd[2]
  if SS>29000:
   SS-=ee
  elif SS<-29000:
   SS+=ee
  if dd[1]==0:
   return SS
  if dd[1]==1 and SS>=PP:
   return SS
  if dd[1]==2 and SS<=OO:
   return SS
 if W<1:
  return NN(OO,PP,0)
 QQ=T(r[h],h^1)
 if not QQ:
  J=DD()
  if J>=PP:
   return J
  if J>OO:
   OO=J
  if W>2 and PP-OO<200:
   l.append((-1,0,-1,i,j,k,m,1))
   j=-1
   h^=1
   m^=0x5A5A5A5A
   n.append(m)
   EE=-RR(W-3,-PP,-PP+1,ee+1)
   xx()
   if t:
    return 0
   if EE>=PP:
    return PP
 TT=-30000
 UU=0
 VV=0
 WW=OO
 for pp in bb(0,dd[3]if dd else 0,ee):
  jj=pp&0x7F
  XX=not(pp>>14)and not g[jj]
  if not ss(pp):
   continue
  VV+=1
  YY=1 if T(r[h],h^1)else 0
  if XX and VV>3 and W>2 and not QQ:
   EE=-RR(W-2+YY,-OO-1,-OO,ee+1)
   if not t and EE>OO:
    EE=-RR(W-1+YY,-PP,-OO,ee+1)
  elif VV>1:
   EE=-RR(W-1+YY,-OO-1,-OO,ee+1)
   if not t and EE>OO and EE<PP:
    EE=-RR(W-1+YY,-PP,-OO,ee+1)
  else:
   EE=-RR(W-1+YY,-PP,-OO,ee+1)
  xx()
  if t:
   return 0
  if EE>TT:
   TT=EE
   UU=pp
   if EE>OO:
    OO=EE
    if OO>=PP:
     if XX:
      y[((pp>>7)&0x7F)<<7|jj]+=W*W
      if pp!=w[0][0]:
       w[0][1]=w[0][0]
       w[0][0]=pp
     break
 if not VV:
  return-30000+ee if QQ else 0
 SS=TT+ee if TT>29000 else TT-ee if TT<-29000 else TT
 v[m]=(W,1 if TT>=PP else 2 if TT<=WW else 0,SS,UU)
 return TT
def ZZ():
 global s,t
 P(q)
 aaa=f[:]
 for kk in w:
  kk[0]=0
  kk[1]=0
 abb=[]
 for pp in bb(0):
  acc=f[(pp>>7)&0x7F]
  if(not acc or(acc>>3)!=h)and not(pp>>14):
   continue
  if ss(pp):
   abb.append(pp)
   xx()
 if not abb:
  abb=bb(0)[:1]
 TT=abb[0]
 for W in range(1,11):
  s=0
  t=0
  OO=-30000
  add=TT
  aee=1
  for pp in abb:
   if not ss(pp):
    continue
   if aee:
    EE=-RR(W-1,-30000,30000,1)
    aee=0
   else:
    EE=-RR(W-1,-OO-1,-OO,1)
    if not t and EE>OO:
     EE=-RR(W-1,-30000,-OO,1)
   if m in n[:-2]:
    EE-=40 if DD()>0 else 6
   xx()
   if t:
    break
   if EE>OO:
    OO=EE
    add=pp
  if not t:
   TT=add
   abb.remove(TT)
   abb.insert(0,TT)
  if s>u//2:
   break
 f[:]=aaa
 l.clear()
 tt=(TT>>7)&0x7F
 jj=TT&0x7F
 rr=TT>>14
 E="abcdefgh"
 return E[tt&7]+str((tt>>4)+1)+E[jj&7]+str((jj>>4)+1)+(" pnbrqk"[rr]if rr else "")
def aff():
 global p
 while 1:
  agg=b("/game",{})
  if agg["status"]=="done":
   break
  if agg["game"]!=p:
   p=agg["game"]
   o.clear()
  while agg["status"]=="your_move":
   P(agg["fen"])
   o.append(m)
   pp=ZZ()
   if pp not in agg["legal_moves"]:
    print("illegal",pp,file=sys.stderr)
    pp=agg["legal_moves"][0]
   agg=b("/move",{"game":agg["game"],"move":pp})
  print(agg.get("outcome"),agg.get("reason"),file=sys.stderr)
aff()
