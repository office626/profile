const config={...(process.env.GITHUB_PAGES==='true'?{output:'export' as const,basePath:process.env.NEXT_PUBLIC_BASE_PATH||'',trailingSlash:true}:{})};
export default config;


