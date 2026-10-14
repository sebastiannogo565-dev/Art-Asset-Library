const fs=require('fs'),path=require('path'),sharp=require('sharp');
(async()=>{
 for(const file of fs.readdirSync(__dirname).filter(f=>/^SL_BLD_C01_MAIN_01_REFERENCE_01_P\d+[A-Z]?\.svg$/.test(f))){
  const r=await sharp(path.join(__dirname,file)).flatten({background:'#F4F2EB'}).removeAlpha().png().toFile(path.join(__dirname,file.replace('.svg','.png')));
  console.log(JSON.stringify({file,width:r.width,height:r.height,bytes:r.size}));
 }
})();
