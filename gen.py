# 生成 index.html
import os
os.makedirs("templates", exist_ok=True)

html = r'''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>校园电动车数字孪生监管系统</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;user-select:none}
body{font-family:'Microsoft YaHei',sans-serif;background:#0f172a;color:#e2e8f0;height:100vh;overflow:hidden}
.header{background:linear-gradient(135deg,#1e293b,#334155);padding:14px 30px;display:flex;align-items:center;justify-content:space-between;border-bottom:2px solid #3b82f6}
.header h1{font-size:20px;font-weight:700}
.header h1 span{color:#3b82f6}
.toolbar{display:flex;gap:10px;padding:8px 30px;background:#1e293b;align-items:center;border-bottom:1px solid #334155;flex-wrap:wrap}
.btn{padding:6px 16px;border:none;border-radius:6px;font-size:13px;font-weight:600;cursor:pointer;transition:.2s}
.btn-primary{background:#3b82f6;color:#fff}
.btn-primary:hover{background:#2563eb}
.btn-primary:disabled{background:#475569;cursor:not-allowed}
.btn-purple{background:#8b5cf6;color:#fff}
.btn-purple.active{background:#6d28d9}
.btn-warning{background:#f59e0b;color:#000}
.stats{display:flex;gap:16px;margin-left:auto;font-size:13px}
.stats .num{font-weight:700;font-size:16px}
.s-green .num{color:#22c55e}
.s-red .num{color:#ef4444}
.s-blue .num{color:#3b82f6}
.main{display:flex;height:calc(100vh - 90px)}
.sidebar{width:200px;background:#1e293b;padding:12px;border-right:1px solid #334155;overflow-y:auto;flex-shrink:0}
.sidebar h3{font-size:13px;color:#94a3b8;margin-bottom:10px}
.card{background:#334155;border-radius:8px;padding:8px;margin-bottom:10px;cursor:grab;border:2px solid transparent;position:relative;transition:.2s}
.card:hover{border-color:#3b82f6;transform:translateY(-2px)}
.card img{width:100%;height:80px;object-fit:cover;border-radius:4px}
.card .label{font-size:11px;margin-top:4px;text-align:center;color:#cbd5e1}
.card .badge{position:absolute;top:4px;right:4px;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:600}
.badge-ok{background:#22c55e;color:#000}
.badge-no{background:#ef4444;color:#fff}
.badge-wait{background:#f59e0b;color:#000}
#scene3d{flex:1;position:relative}
#scene3d canvas{display:block;width:100%!important;height:100%!important}
#camBox{position:absolute;bottom:20px;right:20px;width:200px;height:150px;border:2px solid #475569;border-radius:8px;overflow:hidden;z-index:100;background:#000;display:none}
#camBox video{width:100%;height:100%;object-fit:cover;transform:scaleX(-1)}
#cursor{position:fixed;pointer-events:none;z-index:999;display:none}
#cursor .dot{width:16px;height:16px;border-radius:50%;background:rgba(139,92,246,.7);border:2px solid #8b5cf6;position:absolute;top:-8px;left:-8px;transition:.05s}
#cursor .ring{width:40px;height:40px;border-radius:50%;border:2px solid rgba(139,92,246,.3);position:absolute;top:-20px;left:-20px;transition:.1s}
#cursor.pinch .dot{background:rgba(239,68,68,.8);border-color:#ef4444;transform:scale(1.3)}
#cursor.pinch .ring{border-color:rgba(239,68,68,.5);width:30px;height:30px;top:-15px;left:-15px}
#toast{position:fixed;top:20px;right:20px;padding:12px 20px;border-radius:8px;font-weight:600;z-index:9999;display:none;animation:fadeIn .3s;box-shadow:0 4px 12px rgba(0,0,0,.3)}
#toast.show{display:block}
#toast.ok{background:#22c55e;color:#000}
#toast.err{background:#ef4444;color:#fff}
#toast.info{background:#3b82f6;color:#fff}
@keyframes fadeIn{from{opacity:0;transform:translateX(50px)}to{opacity:1;transform:translateX(0)}}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:#1e293b}
::-webkit-scrollbar-thumb{background:#475569;border-radius:3px}
</style>
</head>
<body>
<div class=header>
<div><h1>🏫 <span>校园电动车</span>数字孪生监管系统</h1></div>
</div>
<div class=toolbar>
<button class="btn btn-primary" id=btnDetect onclick=detectAll()>🔍 YOLO检测</button>
<button class="btn btn-purple" id=btnGesture onclick=toggleGesture()>✋ 手势:关</button>
<button class="btn btn-warning" onclick=resetAll()>🔄 重置</button>
<div class=stats>
<span class="s-green">🟢 合规 <span class=num id=ctOk>0</span></span>
<span class="s-red">🔴 违规 <span class=num id=ctBad>0</span></span>
<span class="s-blue">📦 已放 <span class=num id=ctPlaced>0</span></span>
</div>
</div>
<div class=main>
<div class=sidebar id=side><h3>📷 图片资源</h3><div id=cards>加载中...</div></div>
<div id=scene3d></div>
</div>
<div id=camBox><video id=webcam></video></div>
<div id=cursor><div class=dot></div><div class=ring></div></div>
<div id=toast></div>
<script>
// ============ 全局状态 ============
let IMGS=[], placed={};
const drag={active:false,source:null,clone:null,offX:0,offY:0,el3d:null,bikeIdx:-1,startX:0,startZ:0};

// ============ YOLO检测 ============
async function detectAll(){
  const btn=document.getElementById('btnDetect'); btn.disabled=true; btn.textContent='⏳ 检测...';
  for(let i=0;i<IMGS.length;i++){
    try{
      const r=await fetch('/api/detect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({file:IMGS[i].file})});
      const d=await r.json();
      IMGS[i].detected=true; IMGS[i].isBike=d.has_bicycle; IMGS[i].detections=d.detections;
    }catch(e){IMGS[i].detected=false}
    renderCards();
  }
  btn.disabled=false; btn.textContent='🔍 YOLO检测';
  toast('✅ 检测完成！绿色=自行车可拖动','ok');
}

// ============ 渲染卡片 ============
function renderCards(){
  const c=document.getElementById('cards'); c.innerHTML='';
  IMGS.forEach((img,i)=>{
    const cd=document.createElement('div'); cd.className='card'; cd.dataset.idx=i;
    let badge='';
    if(img.detected) badge=img.isBike?'<span class="badge badge-ok">🚲</span>':'<span class="badge badge-no">❌</span>';
    else badge='<span class="badge badge-wait">⏳</span>';
    cd.innerHTML=badge+'<img src="'+img.url+'" onerror="this.src=\'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22100%22 height=%22100%22><rect fill=%22%23334155%22 width=%22100%22 height=%22100%22/><text x=%2250%22 y=%2255%22 text-anchor=%22middle%22 fill=%22%2394a3b8%22 font-size=%2212%22>加载失败</text></svg>\'"><div class=label>'+img.label+'</div>';
    cd.onmousedown=e=>startDragFromCard(e,i);
    cd.ontouchstart=e=>{e.preventDefault();const t=e.touches[0];startDragFromCard({clientX:t.clientX,clientY:t.clientY},i)};
    c.appendChild(cd);
  });
}

async function loadImgs(){
  try{
    const r=await fetch('/api/images'); const imgs=await r.json();
    IMGS=imgs.map(x=>({...x,detected:false,isBike:false}));
    renderCards();
  }catch(e){document.getElementById('cards').textContent='❌ 加载失败'}
}

// ============ 卡片拖出(创建拖拽克隆) ============
function startDragFromCard(e,idx){
  if(!IMGS[idx].detected) {toast('⏳ 先点YOLO检测','info');return}
  if(!IMGS[idx].isBike) {toast('❌ 只有自行车可以拖入场景','info');return}
  if(placed[idx]&&placed[idx].mesh) {toast('🔄 该图片已放置，在场景中拖动它','info');return}
  drag.active=true; drag.source='card'; drag.bikeIdx=idx;
  const cl=document.createElement('img'); cl.className='drag-clone'; 
  cl.src=IMGS[idx].url; cl.style.cssText='position:fixed;width:100px;height:75px;object-fit:cover;border-radius:6px;z-index:1000;pointer-events:none;box-shadow:0 4px 16px rgba(0,0,0,.5)';
  document.body.appendChild(cl); drag.clone=cl;
  drag.offX=50; drag.offY=37;
  cl.style.left=(e.clientX-50)+'px'; cl.style.top=(e.clientY-37)+'px';
  document.addEventListener('mousemove',onDrag);
  document.addEventListener('mouseup',onDrop);
  document.addEventListener('touchmove',onDragTouch,{passive:false});
  document.addEventListener('touchend',onDropTouch);
}

function onDrag(e){if(drag.clone){drag.clone.style.left=(e.clientX-drag.offX)+'px';drag.clone.style.top=(e.clientY-drag.offY)+'px'}}
function onDragTouch(e){e.preventDefault();const t=e.touches[0];if(drag.clone){drag.clone.style.left=(t.clientX-drag.offX)+'px';drag.clone.style.top=(t.clientY-drag.offY)+'px'}}

function onDrop(e){endDrag(e.clientX,e.clientY)}
function onDropTouch(e){endDrag(e.changedTouches[0].clientX,e.changedTouches[0].clientY)}

function endDrag(cx,cy){
  document.removeEventListener('mousemove',onDrag);
  document.removeEventListener('mouseup',onDrop);
  document.removeEventListener('touchmove',onDragTouch);
  document.removeEventListener('touchend',onDropTouch);
  if(drag.clone){drag.clone.remove();drag.clone=null}
  if(!drag.active) return;
  // 获取3D场景位置
  const canvas=document.querySelector('#scene3d canvas');
  if(!canvas){drag.active=false;return}
  const rect=canvas.getBoundingClientRect();
  if(cx<rect.left||cx>rect.right||cy<rect.top||cy>rect.bottom){
    drag.active=false; drag.source=null; return
  }
  // 转3D坐标
  const mouse=new THREE.Vector2(
    ((cx-rect.left)/rect.width)*2-1,
    -((cy-rect.top)/rect.height)*2+1
  );
  const raycaster=new THREE.Raycaster();
  raycaster.setFromCamera(mouse,camera);
  const intersects=raycaster.intersectObject(ground);
  if(intersects.length>0){
    const pt=intersects[0].point;
    const x3d=Math.max(-18,Math.min(18,pt.x));
    const z3d=Math.max(-12,Math.min(12,pt.z));
    if(placed[drag.bikeIdx]&&placed[drag.bikeIdx].mesh){
      // 已有：移动位置
      moveBike(drag.bikeIdx,x3d,z3d);
    }else if(drag.source==='card'){
      placeBike(drag.bikeIdx,x3d,z3d);
    }
  }
  drag.active=false; drag.source=null; drag.bikeIdx=-1;
}
</script>
</body>
</html>'''
# 截断测试
print(len(html))
