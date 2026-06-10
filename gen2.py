# Part 2: 追加 Three.js 场景和完整逻辑
import os
# 读取已生成的部分
with open('templates/index.html','r') as f:
    html = f.read()

# 找到 </script> 位置，插入新代码
insert = r'''
// ============ Three.js 3D场景 ============
let scene, camera, renderer, ground;
const PARKING={x1:-5,z1:-4,x2:5,z2:4};

function initScene(){
  const box=document.getElementById('scene3d');
  scene=new THREE.Scene();
  scene.background=new THREE.Color(0x87ceeb);
  camera=new THREE.PerspectiveCamera(45,box.clientWidth/box.clientHeight,0.1,100);
  camera.position.set(0,18,16);
  camera.lookAt(0,0,0);
  renderer=new THREE.WebGLRenderer({antialias:true});
  renderer.setSize(box.clientWidth,box.clientHeight);
  renderer.shadowMap.enabled=true;
  box.appendChild(renderer.domElement);

  // 灯光
  const amb=new THREE.AmbientLight(0xffffff,0.6);
  scene.add(amb);
  const dir=new THREE.DirectionalLight(0xffffff,0.8);
  dir.position.set(10,20,10);
  dir.castShadow=true;
  scene.add(dir);

  // 草地
  const gGeo=new THREE.PlaneGeometry(40,28);
  const gMat=new THREE.MeshLambertMaterial({color:0x7ec87e});
  ground=new THREE.Mesh(gGeo,gMat);
  ground.rotation.x=-Math.PI/2;
  ground.position.set(0,0,0);
  ground.receiveShadow=true;
  scene.add(ground);

  // 网格
  scene.add(new THREE.GridHelper(40,20,0x555555,0x444444));

  // 道路
  const roadMat=new THREE.MeshLambertMaterial({color:0x666666});
  const r1=new THREE.Mesh(new THREE.PlaneGeometry(40,4),roadMat);
  r1.rotation.x=-Math.PI/2;r1.position.set(0,0.01,-10);
  scene.add(r1);
  const r2=new THREE.Mesh(new THREE.PlaneGeometry(4,28),roadMat);
  r2.rotation.x=-Math.PI/2;r2.position.set(-12,0.01,0);
  scene.add(r2);

  // 建筑
  const colors=[0x4a90d9,0x8b7355,0x6b8e23,0xcd853f];
  const blds=[
    {x:-10,z:-10,w:8,h:4,d:6,c:colors[0]},
    {x:-14,z:4,w:5,h:2.5,d:5,c:colors[1]},
    {x:10,z:-8,w:6,h:3,d:5,c:colors[2]},
    {x:12,z:6,w:7,h:3.5,d:5,c:colors[3]},
    {x:-8,z:10,w:6,h:2,d:4,c:0xa0522d},
  ];
  blds.forEach(b=>{
    const m=new THREE.Mesh(new THREE.BoxGeometry(b.w,b.h,b.d),new THREE.MeshLambertMaterial({color:b.c}));
    m.position.set(b.x,b.h/2,b.z);m.castShadow=true;
    scene.add(m);
  });

  // 树
  const trees=[
    [-15,-6],[-16,0],[-15,6],[8,-12],[9,-5],[11,4],[14,8],[-6,-12],[-4,8]
  ];
  trees.forEach(t=>{
    const trunk=new THREE.Mesh(new THREE.CylinderGeometry(0.15,0.2,0.8),new THREE.MeshLambertMaterial({color:0x8B4513}));
    trunk.position.set(t[0],0.4,t[1]);
    scene.add(trunk);
    const crown=new THREE.Mesh(new THREE.SphereGeometry(0.6),new THREE.MeshLambertMaterial({color:0x2d8a2d}));
    crown.position.set(t[0],1.0,t[1]);
    scene.add(crown);
  });

  // 停车位
  drawParking();

  window.addEventListener('resize',()=>{
    const w=box.clientWidth,h=box.clientHeight;
    camera.aspect=w/h;camera.updateProjectionMatrix();
    renderer.setSize(w,h);
  });

  animate();
}

function drawParking(){
  const pts=[
    new THREE.Vector3(PARKING.x1,0.02,PARKING.z1),
    new THREE.Vector3(PARKING.x2,0.02,PARKING.z1),
    new THREE.Vector3(PARKING.x2,0.02,PARKING.z2),
    new THREE.Vector3(PARKING.x1,0.02,PARKING.z2),
  ];
  const g=new THREE.BufferGeometry().setFromPoints(pts.concat(pts[0]));
  const mat=new THREE.LineBasicMaterial({color:0xf59e0b,linewidth:3});
  scene.add(new THREE.Line(g,mat));

  // 停车位底部半透明填充
  const fill=new THREE.Mesh(
    new THREE.PlaneGeometry(PARKING.x2-PARKING.x1,PARKING.z2-PARKING.z1),
    new THREE.MeshLambertMaterial({color:0xf59e0b,transparent:true,opacity:0.12})
  );
  fill.rotation.x=-Math.PI/2;
  fill.position.set((PARKING.x1+PARKING.x2)/2,0.015,(PARKING.z1+PARKING.z2)/2);
  scene.add(fill);

  // "P" 文字用 Sprite
  const canvas=document.createElement('canvas'); canvas.width=128; canvas.height=128;
  const ctx=canvas.getContext('2d');
  ctx.fillStyle='rgba(245,158,11,0.6)';ctx.font='bold 80px Arial';ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillText('P',64,64);
  const tex=new THREE.CanvasTexture(canvas);
  const spr=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true}));
  spr.position.set((PARKING.x1+PARKING.x2)/2,1.5,(PARKING.z1+PARKING.z2)/2);
  spr.scale.set(2,2,1);
  scene.add(spr);
}

function isInParking(x,z){
  return x>=PARKING.x1&&x<=PARKING.x2&&z>=PARKING.z1&&z<=PARKING.z2;
}

function createBike3D(color){
  const group=new THREE.Group();
  // 车轮
  const wheelGeo=new THREE.TorusGeometry(0.4,0.12,8,12);
  const wheelMat=new THREE.MeshLambertMaterial({color:0x222222});
  const w1=new THREE.Mesh(wheelGeo,wheelMat);w1.position.set(-0.4,0.2,0);w1.rotation.y=Math.PI/2;
  const w2=new THREE.Mesh(wheelGeo,wheelMat);w2.position.set(0.4,0.2,0);w2.rotation.y=Math.PI/2;
  group.add(w1);group.add(w2);
  // 车架
  const frameMat=new THREE.MeshLambertMaterial({color});
  const bar=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,0.8),frameMat);
  bar.rotation.z=Math.PI/2;bar.position.set(0,0.4,0);
  group.add(bar);
  // 三角架
  const tri=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,0.5),frameMat);
  tri.position.set(-0.15,0.35,0);tri.rotation.z=0.6;
  group.add(tri);
  const tri2=new THREE.Mesh(new THREE.CylinderGeometry(0.04,0.04,0.5),frameMat);
  tri2.position.set(0.15,0.35,0);tri2.rotation.z=-0.6;
  group.add(tri2);
  // 坐垫
  const seat=new THREE.Mesh(new THREE.BoxGeometry(0.15,0.04,0.08),new THREE.MeshLambertMaterial({color:0x333333}));
  seat.position.set(-0.15,0.55,0);
  group.add(seat);
  // 车把
  const handle=new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.03,0.25),new THREE.MeshLambertMaterial({color:0x333333}));
  handle.position.set(0.4,0.45,0);handle.rotation.z=0.3;
  group.add(handle);
  return group;
}

function placeBike(idx,x3d,z3d){
  const color=isInParking(x3d,z3d)?0x22c55e:0xef4444;
  const bike=createBike3D(color);
  bike.position.set(x3d,0,z3d);
  scene.add(bike);
  placed[idx]={mesh:bike,idx,x:x3d,z:z3d,compliant:color===0x22c55e};
  updateStats();
  toast(color===0x22c55e?'✅ 合规停放':'❌ 违规停放',color===0x22c55e?'ok':'err');
}

function moveBike(idx,x3d,z3d){
  if(!placed[idx]||!placed[idx].mesh)return;
  const color=isInParking(x3d,z3d)?0x22c55e:0xef4444;
  placed[idx].mesh.position.set(x3d,0,z3d);
  placed[idx].x=x3d;placed[idx].z=z3d;placed[idx].compliant=color===0x22c55e;
  // 更新颜色（重建）
  scene.remove(placed[idx].mesh);
  const bike=createBike3D(color);
  bike.position.set(x3d,0,z3d);
  scene.add(bike);
  placed[idx].mesh=bike;
  updateStats();
  toast(color===0x22c55e?'✅ 合规停放':'❌ 违规停放',color===0x22c55e?'ok':'err');
}

// ============ 3D鼠标拖拽(已放置的自行车) ============
function setup3DDrag(){
  const canvas=renderer.domElement;
  let selected=null, selIdx=-1, isDragging3d=false;
  let planeIntersect=new THREE.Vector3();

  canvas.addEventListener('mousedown',e=>{
    const rect=canvas.getBoundingClientRect();
    const mouse=new THREE.Vector2(((e.clientX-rect.left)/rect.width)*2-1,-((e.clientY-rect.top)/rect.height)*2+1);
    const raycaster=new THREE.Raycaster();raycaster.setFromCamera(mouse,camera);
    // 检测自行车
    const bikes=Object.values(placed).filter(p=>p.mesh).map(p=>p.mesh);
    const hits=raycaster.intersectObjects(bikes,true);
    if(hits.length>0){
      let obj=hits[0].object;
      while(obj.parent&&!Object.values(placed).find(p=>p.mesh===obj))obj=obj.parent;
      const entry=Object.values(placed).find(p=>p.mesh===obj);
      if(entry){selected=entry.mesh;selIdx=entry.idx;isDragging3d=true;
        const plane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
        raycaster.ray.intersectPlane(plane,planeIntersect);
        drag.offX=planeIntersect.x-selected.position.x;
        drag.offZ=planeIntersect.z-selected.position.z;
      }
    }
  });

  canvas.addEventListener('mousemove',e=>{
    if(!isDragging3d||!selected)return;
    const rect=canvas.getBoundingClientRect();
    const mouse=new THREE.Vector2(((e.clientX-rect.left)/rect.width)*2-1,-((e.clientY-rect.top)/rect.height)*2+1);
    const raycaster=new THREE.Raycaster();raycaster.setFromCamera(mouse,camera);
    const plane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
    raycaster.ray.intersectPlane(plane,planeIntersect);
    const x=Math.max(-18,Math.min(18,planeIntersect.x-drag.offX));
    const z=Math.max(-12,Math.min(12,planeIntersect.z-drag.offZ));
    selected.position.set(x,0,z);
  });

  canvas.addEventListener('mouseup',e=>{
    if(!isDragging3d||!selected||selIdx<0){isDragging3d=false;return}
    const x=selected.position.x,z=selected.position.z;
    const color=isInParking(x,z)?0x22c55e:0xef4444;
    if(placed[selIdx]){
      placed[selIdx].x=x;placed[selIdx].z=z;placed[selIdx].compliant=color===0x22c55e;
      scene.remove(selected);
      const bike=createBike3D(color);bike.position.set(x,0,z);
      scene.add(bike);
      placed[selIdx].mesh=bike;
      updateStats();
    }
    selected=null;selIdx=-1;isDragging3d=false;
  });
}

function animate(){
  requestAnimationFrame(animate);
  renderer.render(scene,camera);
}

function updateStats(){
  const vals=Object.values(placed).filter(p=>p.mesh);
  let ok=vals.filter(v=>v.compliant).length;
  let bad=vals.filter(v=>!v.compliant).length;
  document.getElementById('ctOk').textContent=ok;
  document.getElementById('ctBad').textContent=bad;
  document.getElementById('ctPlaced').textContent=vals.length;
}

function toast(msg,type){
  const t=document.getElementById('toast');
  t.textContent=msg;t.className='toast show '+type;
  clearTimeout(t._timer);t._timer=setTimeout(()=>t.classList.remove('show'),2000);
}

function resetAll(){
  Object.values(placed).filter(p=>p.mesh).forEach(p=>scene.remove(p.mesh));
  placed={};
  updateStats();
  toast('🔄 已重置','info');
}

// ============ 手势控制 ============
let gestureEnabled=false, gestureReady=false;
const gesture={isPinching:false,x:0,y:0,prev:false};

function toggleGesture(){
  if(gestureEnabled){stopGesture();return}
  initGesture();
}

function initGesture(){
  const btn=document.getElementById('btnGesture');
  btn.textContent='✋ 手势:加载中';btn.disabled=true;
  const video=document.getElementById('webcam');
  const camBox=document.getElementById('camBox');
  camBox.style.display='block';

  const hands=new Hands({locateFile:f=>'https://cdn.jsdelivr.net/npm/@mediapipe/hands/'+f});
  hands.setOptions({maxNumHands:1,modelComplexity:1,minDetectionConfidence:.5,minTrackingConfidence:.5});

  hands.onResults(results=>{
    if(results.multiHandLandmarks&&results.multiHandLandmarks.length>0){
      const lm=results.multiHandLandmarks[0];
      const thumb=lm[4],index=lm[8];
      gesture.x=(1-index.x)*window.innerWidth;
      gesture.y=index.y*window.innerHeight;
      const d=Math.hypot((thumb.x-index.x)*3,(thumb.y-index.y)*3,(thumb.z-index.z)*3);
      gesture.prev=gesture.isPinching;
      gesture.isPinching=d<0.045;
      updateCursor();
      handleGestureDrag();
    }else{
      gesture.prev=gesture.isPinching;
      gesture.isPinching=false;
      updateCursor();
    }
  });

  const camera2=new Camera(video,{
    onFrame:async()=>{await hands.send({image:video})},
    width:320,height:240
  });
  camera2.start().then(()=>{
    gestureReady=true;gestureEnabled=true;
    btn.textContent='✋ 手势:开';btn.className='btn btn-purple active';btn.disabled=false;
  }).catch(()=>{
    btn.textContent='✋ 手势:失败';btn.disabled=false;
  });
}

function stopGesture(){
  gestureEnabled=false;gestureReady=false;
  document.getElementById('camBox').style.display='none';
  document.getElementById('cursor').style.display='none';
  document.getElementById('btnGesture').textContent='✋ 手势:关';
  document.getElementById('btnGesture').className='btn btn-purple';
  if(drag.active) endDrag(gesture.x,gesture.y);
}

function updateCursor(){
  const c=document.getElementById('cursor');
  if(!gestureEnabled){c.style.display='none';return}
  c.style.display='block';
  c.style.left=gesture.x+'px';c.style.top=gesture.y+'px';
  c.className=gesture.isPinching?'pinch':'';
}

function handleGestureDrag(){
  if(!gestureEnabled)return;
  const pinching=gesture.isPinching,prev=gesture.prev;
  if(pinching&&!prev){
    // 捏合开始：检测是否在3D场景中
    const el=document.elementFromPoint(gesture.x,gesture.y);
    if(!el)return;
    const canvas=document.querySelector('#scene3d canvas');
    if(!canvas)return;
    const rect=canvas.getBoundingClientRect();
    if(gesture.x<rect.left||gesture.x>rect.right||gesture.y<rect.top||gesture.y>rect.bottom)return;
    const mouse=new THREE.Vector2(
      ((gesture.x-rect.left)/rect.width)*2-1,
      -((gesture.y-rect.top)/rect.height)*2+1
    );
    const r=new THREE.Raycaster();r.setFromCamera(mouse,camera);
    const bikes=Object.values(placed).filter(p=>p.mesh).map(p=>p.mesh);
    const hits=r.intersectObjects(bikes,true);
    if(hits.length>0){
      let obj=hits[0].object;
      while(obj.parent&&!Object.values(placed).find(p=>p.mesh===obj))obj=obj.parent;
      const entry=Object.values(placed).find(p=>p.mesh===obj);
      if(entry){
        drag.active=true;drag.source='gesture';drag.bikeIdx=entry.idx;
        drag.el3d=entry.mesh;
        const plane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
        r.ray.intersectPlane(plane,new THREE.Vector3());
        drag.offX=0;drag.offY=0;
      }
    }else{
      // 手势从空白处开始不处理，后续跟踪
      drag.active=false;
    }
  }else if(pinching&&prev){
    if(drag.active&&drag.el3d){
      const canvas=document.querySelector('#scene3d canvas');
      const rect=canvas.getBoundingClientRect();
      const mouse=new THREE.Vector2(
        ((gesture.x-rect.left)/rect.width)*2-1,
        -((gesture.y-rect.top)/rect.height)*2+1
      );
      const r=new THREE.Raycaster();r.setFromCamera(mouse,camera);
      const plane=new THREE.Plane(new THREE.Vector3(0,1,0),0);
      const pt=new THREE.Vector3();
      r.ray.intersectPlane(plane,pt);
      const x=Math.max(-18,Math.min(18,pt.x));
      const z=Math.max(-12,Math.min(12,pt.z));
      drag.el3d.position.set(x,0,z);
    }
  }else if(!pinching&&prev){
    if(drag.active&&drag.el3d&&drag.bikeIdx>=0){
      const x=drag.el3d.position.x,z=drag.el3d.position.z;
      const color=isInParking(x,z)?0x22c55e:0xef4444;
      if(placed[drag.bikeIdx]){
        placed[drag.bikeIdx].x=x;placed[drag.bikeIdx].z=z;
        placed[drag.bikeIdx].compliant=color===0x22c55e;
        scene.remove(drag.el3d);
        const bike=createBike3D(color);bike.position.set(x,0,z);
        scene.add(bike);
        placed[drag.bikeIdx].mesh=bike;
        updateStats();
      }
    }
    drag.active=false;drag.source=null;drag.el3d=null;drag.bikeIdx=-1;
  }
}

// ============ 初始化 ============
loadImgs();
setTimeout(()=>{initScene();setup3DDrag()},100);
</script>
</body>
</html>'''

# 找到 </script> 的最后一个位置，在其前面插入
pos = html.rfind('</script>')
if pos > 0:
    html = html[:pos] + insert + html[pos:]

with open('templates/index.html','w') as f:
    f.write(html)
print(f'写入完成: {len(html)} bytes')
print(f'Three.js: {"three.min.js" in html}')
print(f'手势: {"@mediapipe/hands" in html}')
print(f'3D自行车: {"createBike3D" in html}')
print(f'拖拽3D: {"setup3DDrag" in html}')
