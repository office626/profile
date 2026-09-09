import {spawnSync} from 'node:child_process';
const fix=spawnSync(process.execPath,['scripts/patch-prerender.mjs'],{stdio:'inherit'});if(fix.status!==0)process.exit(fix.status??1);
const r=spawnSync(process.execPath,['node_modules/vinext/dist/cli.js','build'],{stdio:'inherit',env:{...process.env,GITHUB_PAGES:'true',NEXT_PUBLIC_BASE_PATH:process.env.NEXT_PUBLIC_BASE_PATH??'/profile'}});if(r.status!==0)process.exit(r.status??1);const check=spawnSync(process.execPath,['scripts/finalize-pages.mjs'],{stdio:'inherit',env:process.env});process.exit(check.status??1);

