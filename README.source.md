<!-- Original editorial design. CI owns README.md and .github/assets. -->

```aura width=860 height=280 link="https://github.com/rrddngtnn"
<div style={{width:'100%',height:'100%',display:'flex',flexDirection:'column',padding:48,background:'#f3efe6',color:'#242522',fontFamily:'Inter'}}>
  <div style={{display:'flex',justifyContent:'space-between',fontSize:13,letterSpacing:2,fontWeight:700,color:'#64675d'}}><span>RRDDNGTNN / PUBLIC WORK</span><span>CODE &amp; OPERATIONS</span></div>
  <div style={{display:'flex',alignItems:'baseline',gap:24,marginTop:24}}>
    <span style={{fontSize:76,fontWeight:700,letterSpacing:-4,lineHeight:1,color:'#8c4b30'}}>RED.</span>
    <span style={{fontSize:26,fontWeight:700,letterSpacing:-0.6}}>AI gateways &amp; command-line tools</span>
  </div>
  <div style={{display:'flex',marginTop:24,paddingTop:20,borderTop:'1px solid #c9c6bb',fontSize:17,color:'#64675d'}}>Routing models. Configuring prompts. Automating the repetitive parts.</div>
</div>
```

```aura width=860 height=244
<div style={{width:'100%',height:'100%',display:'flex',flexDirection:'column',padding:'32px 48px',background:'#242522',color:'#f3efe6',fontFamily:'Inter'}}>
  <div style={{display:'flex',justifyContent:'space-between',fontSize:13,letterSpacing:2,color:'#b9c4a6',fontWeight:700}}><span>01 / SELECTED REPOSITORIES</span><span>PUBLIC SOURCE</span></div>
  <div style={{display:'flex',marginTop:28,gap:32}}>
    <div style={{display:'flex',flexDirection:'column',width:366,paddingRight:24,borderRight:'1px solid #50534b'}}>
      <span style={{fontSize:30,fontWeight:700,letterSpacing:-1}}>StyxRouter</span>
      <span style={{fontSize:17,lineHeight:1.5,marginTop:12,color:'#d2d2c7'}}>AI model gateway with a React administration panel.</span>
      <span style={{fontSize:13,marginTop:20,color:'#b9c4a6'}}>TYPESCRIPT / HONO / BUN</span>
    </div>
    <div style={{display:'flex',flexDirection:'column',width:366}}>
      <span style={{fontSize:30,fontWeight:700,letterSpacing:-1}}>s0ulctl</span>
      <span style={{fontSize:17,lineHeight:1.5,marginTop:12,color:'#d2d2c7'}}>A CLI for configuring 9router's upstream system prompts.</span>
      <span style={{fontSize:13,marginTop:20,color:'#b9c4a6'}}>JAVASCRIPT / NODE.JS / SHELL</span>
    </div>
  </div>
</div>
```

[StyxRouter →](https://github.com/rrddngtnn/styxrouter) &nbsp; / &nbsp; [s0ulctl →](https://github.com/rrddngtnn/s0ulctl)

```aura width=860 height=204
<div style={{width:'100%',height:'100%',display:'flex',flexDirection:'column',padding:'32px 48px',background:'#f3efe6',color:'#242522',fontFamily:'Inter'}}>
  <div style={{display:'flex',fontSize:13,letterSpacing:2,color:'#64675d',fontWeight:700}}>02 / TOOLS IN THE REPOSITORIES</div>
  {[
    ['Languages', 'TypeScript · JavaScript · Python · Shell'],
    ['Runtime & web', 'Bun · Node.js · Hono · React'],
    ['Checks', 'node:test · ShellCheck · GitHub Actions']
  ].map(function(row) { return <div key={row[0]} style={{display:'flex',alignItems:'center',marginTop:20,fontSize:18}}><span style={{display:'flex',width:184,color:'#64675d',fontSize:15}}>{row[0]}</span><span style={{display:'flex',fontWeight:600}}>{row[1]}</span></div>; })}
</div>
```

```aura width=860 height=160
<div style={{width:'100%',height:'100%',display:'flex',padding:'28px 48px',background:'#242522',fontFamily:'Inter',color:'#f3efe6'}}>
  {[
    ['Public repos', github.stats.totalRepos],
    ['Stars', github.stats.totalStars],
    ['Repo commits', github.stats.totalCommits]
  ].map(function(row,i) { return <div key={row[0]} style={{display:'flex',flexDirection:'column',justifyContent:'center',width:254,paddingLeft:i ? 28 : 0,borderLeft:i ? '1px solid #50534b' : 'none'}}><span style={{fontSize:42,lineHeight:1,fontWeight:700,color:row[1] ? '#b9c4a6' : '#d2d2c7'}}>{String(row[1])}</span><span style={{fontSize:14,marginTop:12,color:'#d2d2c7'}}>{row[0]}</span></div>; })}
</div>
```

<sub>Public GitHub data, refreshed daily. “Repo commits” counts default-branch repository history, not personal contributions.</sub>

[Browse repositories](https://github.com/rrddngtnn?tab=repositories) · [Profile source](https://github.com/rrddngtnn/rrddngtnn/blob/main/README.source.md)

<sub>Cards rendered with [readme-aura](https://github.com/collectioneur/readme-aura).</sub>
