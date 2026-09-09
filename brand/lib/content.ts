import profileData from '@/content/profile.json';
import portfolioData from '@/content/portfolio.json';
import collected from '@/content/collected-cases.json';
export const profile=profileData;
export type Case={id:string;category:string;title:string;client:string;role:string;period:string;scope:string;result:string;related_service:string;featured?:boolean;public_links?:{label:string;url:string}[];attachments?:{label:string;url:string}[];updated?:string};
export const cases=[...portfolioData.cases,...collected] as Case[];
export const packages=profile.service_menu.items;
export const services=[
{slug:'management',num:'01',title:'経営・事業づくり',audience:'中小企業・個人事業主',headline:'頭の中の構想を、\n経営の次の一手に。',summary:'事業計画、経営改善、生産性向上。現場と数字をつなぎ、実行の優先順位を整理します。',problem:'日々の仕事に追われ、計画づくりまで手が回らない。資金繰りや次の事業について、相談できる相手がほしい。',codes:['01','02','03','13'],categories:['中小企業'],proof:'中小企業診断士・認定経営革新等支援機関として、計画策定から月次のモニタリングまで支援。'},
{slug:'ai-dx',num:'02',title:'AI・DXの業務実装',audience:'経営者・業務改革の担当者',headline:'AIを学ぶところから、\n仕事で使えるところまで。',summary:'業務の棚卸しから小さな試作、運用ルールづくりまで。現場で使える形に整えます。',problem:'生成AIを導入したものの使い方が広がらない。どの業務から改善するか、情報の扱いも含めて整理したい。',codes:['04','03','11','10'],categories:['中小企業','研修・講演'],proof:'NECでの業務改革の経験と、地域企業の生産性向上支援を接続。G検定合格。'},
{slug:'smart-city',num:'03',title:'政策・スマートシティ',audience:'自治体・行政の担当者',headline:'まちの構想を、\n実行できる政策へ。',summary:'計画策定、DX推進、地域幸福度指標の活用。庁内と地域の対話から、事業の道筋をつくります。',problem:'計画と現場の動きがつながらない。庁内の目線を揃え、住民にとっての価値から事業を設計したい。',codes:['05','06','10','12'],categories:['国・政策','自治体'],proof:'内閣府での政策立案、スマートシティガイドブック策定への関与、自治体アドバイザーの経験。'},
{slug:'co-creation',num:'04',title:'官民共創・新規事業',audience:'企業の経営企画・新規事業部門',headline:'企業と地域の接点を、\n続いていく事業に。',summary:'自治体連携、地域課題の探索、関係者調整。構想と現場のあいだをつなぎます。',problem:'自治体に提案したいが、話を進める手順が見えない。実証のあとも続く体制と事業モデルをつくりたい。',codes:['07','01','08','13'],categories:['大企業','大企業・自治体'],proof:'NECでの経営企画・グループ経営と、のべ約300団体が参画したコンソーシアムの設立・運営経験。'},
{slug:'training',num:'05',title:'研修・講演・対話の場',audience:'自治体・商工団体・研修主催者',headline:'聞いて終わらない。\n次の行動につながる時間を。',summary:'経営指導員・自治体職員・経営者向けの研修から、会議の進行、パネルモデレートまで。',problem:'参加者が自分の仕事に持ち帰れる研修にしたい。関係者の多い会議で、議論を具体的な行動につなげたい。',codes:['09','10','11','12','08'],categories:['研修・講演'],proof:'DX・AI研修、地域幸福度指標を使う対話の場、ラジオのパーソナリティなど、伝える・引き出す実践。'},
{slug:'community',num:'06',title:'地域・コミュニティづくり',audience:'市民団体・NPO・自治会',headline:'地域への思いを、\n続けられる活動に。',summary:'活動の目的、役割分担、発信、行政・企業との連携。市民起点の活動の土台を整えます。',problem:'思いを持つ仲間はいるけれど、運営が一部の人に偏っている。団体化や世代交代も含め、続く形を考えたい。',codes:['12','13'],categories:['NPO・地域活動'],proof:'Code for Nagareyama、Civic Tech Zen Chiba、地域の市民活動、子ラボ屋での当事者としての実践。'}
];
export function serviceForCase(c:Case){return services.find(s=>s.categories.includes(c.category))||services[0]}

