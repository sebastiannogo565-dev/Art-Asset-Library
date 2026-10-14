const fs=require('fs'),path=require('path'),sharp=require('sharp');
(async()=>{
for(const f of fs.readdirSync(__dirname).filter(f=>/^SL_BLD_C01_MAIN_01_REFERENCE_01_REV_01_P\d+[A-Z]?\.svg$/.test(f))){
 const info=await sharp(path.join(__dirname,f)).flatten({background:'#F4F2EB'}).removeAlpha().png().toFile(path.join(__dirname,f.replace('.svg','.png')));
 console.log(JSON.stringify({f,width:info.width,height:info.height}));
}})();
