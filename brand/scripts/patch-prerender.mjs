import fs from 'node:fs';
// vinext 1.0.0-beta.5 sends unprefixed, noncanonical URLs to its own prerender handler.
// Keep this narrow compatibility fix version-bound; it changes build requests only.
const pkg=JSON.parse(fs.readFileSync('node_modules/vinext/package.json','utf8'));
if(pkg.version!=='1.0.0-beta.5')throw Error('Review the prerender compatibility fix before changing vinext');
const file='node_modules/vinext/dist/build/prerender.js';let text=fs.readFileSync(file,'utf8');const before='`http://localhost${urlPath}`';const after='`http://localhost${config.basePath || ""}${config.trailingSlash && urlPath !== "/" && !urlPath.endsWith("/") ? urlPath + "/" : urlPath}`';if(text.includes(after)){console.log('Prerender compatibility fix already present')}else{if(text.split(before).length-1!==2)throw Error('Unexpected prerender source; compatibility fix not applied');text=text.replaceAll(before,after);fs.writeFileSync(file,text);console.log('Applied base-path and trailing-slash prerender compatibility fix')}
