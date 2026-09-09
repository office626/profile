import {Head,CTA} from '@/components/site';import Portfolio from './portfolio';export const metadata={title:'実績・ポートフォリオ'};
export default function Page(){return <main className="wrap"><Head label="PORTFOLIO" title="つないできたこと。\n動かしてきたこと。" description="政策、経営、まちづくり。土屋俊博の関わり方と成果を、領域ごとに紹介します。守秘義務のある事例は匿名化して掲載しています。"/><Portfolio/><CTA/></main>}
