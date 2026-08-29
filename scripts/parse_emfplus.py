from pathlib import Path
import struct, sys

p=Path(sys.argv[1]); b=p.read_bytes()
comment_size=struct.unpack_from('<I',b,4)[0]
start=0x70
if b[start:start+4] != b'EMF+':
    start=b.find(b'EMF+')
pos=start+4
print('file',len(b),'EMF+ at',hex(start),'comment size',comment_size)
names={
0x4001:'Header',0x4002:'EndOfFile',0x4003:'Comment',0x4004:'GetDC',0x4008:'Object',
0x4009:'Clear',0x400A:'FillRects',0x400B:'DrawRects',0x400C:'FillPolygon',0x400D:'DrawLines',
0x400E:'FillEllipse',0x400F:'DrawEllipse',0x4010:'FillPie',0x4011:'DrawPie',0x4012:'DrawArc',
0x4013:'FillRegion',0x4014:'FillPath',0x4015:'DrawPath',0x401A:'DrawImage',0x401B:'DrawImagePoints',
0x401C:'DrawString',0x4021:'Save',0x4022:'Restore',0x4023:'BeginContainer',0x4024:'BeginContainerNoParams',
0x4025:'EndContainer',0x4026:'SetWorldTransform',0x4027:'ResetWorldTransform',0x4028:'MultiplyWorldTransform',
0x4029:'TranslateWorldTransform',0x402A:'ScaleWorldTransform',0x402B:'RotateWorldTransform',0x4030:'SetPageTransform',
0x4035:'SetClipRect',0x4036:'SetClipPath',0x4037:'SetClipRegion',0x4038:'OffsetClip'}
i=0
while pos+12<=len(b):
    typ,flags,size,datasize=struct.unpack_from('<HHII',b,pos)
    if size<12 or pos+size>len(b):
        print('bad at',hex(pos),hex(typ),flags,size,datasize); break
    data=b[pos+12:pos+size]
    extra=''
    if typ==0x4008 and len(data)>=4:
        obj_type=(flags>>8)&0x7f; obj_id=flags&0xff
        extra=f' objectId={obj_id} objectType={obj_type}'
    sigs=[]
    for sig,label in [(b'\x89PNG\r\n\x1a\n','PNG'),(b'\xff\xd8\xff','JPEG'),(b'BM','BMP'),(b' EMF','EMF')]:
        at=data.find(sig)
        if at>=0:sigs.append(f'{label}@{at}')
    if sigs: extra += ' sigs='+','.join(sigs)
    print(i,hex(pos),hex(typ),names.get(typ,'?'),'flags='+hex(flags),'size='+str(size),'data='+str(datasize)+extra)
    pos+=size;i+=1
    if typ==0x4002:break
