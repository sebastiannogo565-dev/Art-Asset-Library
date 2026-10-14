// NODE_PATH may point to the bundled sharp module directory; no dependency install required.
const fs=require('fs'), path=require('path'), sharp=require('sharp');
(async()=>{
 for(const file of fs.readdirSync(__dirname).filter(f=>/^SL_BLD_B01_HOME_01_REFERENCE_01_P\d+\.svg$/.test(f))){
  const out=path.join(__dirname,file.replace(/\.svg$/,'.png'));
  const r=await sharp(path.join(__dirname,file)).flatten({background:'#edf1ec'}).removeAlpha().png().toFile(out);
  console.log(JSON.stringify({file:path.basename(out),width:r.width,height:r.height,bytes:r.size}));
 }
})();
