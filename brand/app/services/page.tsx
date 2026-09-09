import {ServiceGrid,CTA,Head,Flow} from '@/components/site';
export const metadata={title:'相談できること'};
export default function Page(){return <main className="wrap"><Head label="SERVICES" title="何を進めたいか、から選ぶ。" description="お立場と課題に合わせた6つの入口。支援内容、成果物、費用の目安、関連実績をご覧いただけます。"/><ServiceGrid/><section className="section"><Flow/></section><CTA/></main>}
