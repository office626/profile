import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
export const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
export function inside(root,target){const rel=path.relative(fs.realpathSync(root),fs.realpathSync(target));if(rel.startsWith('..')||path.isAbsolute(rel))throw Error('Source escapes configured folder');return fs.realpathSync(target)}
export function walk(root){if(!fs.existsSync(root))return[];const out=[];for(const e of fs.readdirSync(root,{withFileTypes:true})){const p=path.join(root,e.name);if(e.isSymbolicLink()||e.name.startsWith('.'))continue;if(e.isDirectory())out.push(...walk(p));else if(e.isFile())out.push(p)}return out}
export function writeJSON(target,value){fs.mkdirSync(path.dirname(target),{recursive:true});const text=JSON.stringify(value,null,2)+'\n';if(fs.existsSync(target)&&fs.readFileSync(target,'utf8')===text)return false;fs.writeFileSync(target+'.tmp',text);fs.renameSync(target+'.tmp',target);return true}
export function configuration(file){const full=path.resolve(file);const c=JSON.parse(fs.readFileSync(full,'utf8'));const base=path.dirname(full);for(const key of ['files','activities','approved','localState']){if(typeof c[key]!=='string')throw Error('Missing configuration: '+key);c[key]=path.resolve(base,c[key])}return c}
export function cleanString(value,name,max=3000){if(typeof value!=='string'||!value.trim()||value.length>max)throw Error('Invalid '+name);if(/(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|-----BEGIN .*PRIVATE KEY-----)/.test(value))throw Error('Possible secret in '+name);return value.trim()}
export function publicURL(value){const u=new URL(value);if(u.protocol!=='https:'||u.username||u.password)throw Error('Only public HTTPS URLs are allowed');return u.href}
