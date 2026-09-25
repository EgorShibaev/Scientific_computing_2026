/** Lecture 4. Native editable PowerPoint text, tables, and scientific charts.
 * Run with @oai/artifact-tool available, or set ARTIFACT_TOOL_MODULE to its
 * absolute ES-module entry point. See README.md for build and validation.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const repo = path.resolve(process.env.COURSE_REPO ?? path.join(here, '../..'));
const out = path.resolve(process.env.SLIDE_BUILD_DIR ?? path.join(repo, 'tmp/lecture-04-slides/build'));
const moduleId = process.env.ARTIFACT_TOOL_MODULE;
const { Presentation, PresentationFile } = await import(moduleId ? pathToFileURL(moduleId).href : '@oai/artifact-tool');
await fs.mkdir(out, { recursive: true });

const C = { ink:'#16324F', blue:'#1F4E79', orange:'#C46A13', teal:'#007D80', muted:'#526477', grid:'#E0E7EE', white:'#FFFFFF' };
const FONT = 'Arial';
const MATH = 'STIX Two Math';
const p = Presentation.create({slideSize:{width:1280,height:720}});
const slides = [];
const logPlan = [];
const chartOwners = new Set();
const tableOwners = new Set();
let chartIndex = 0;

function text(slide, value, x, y, w, h, opts={}) {
  const shape = slide.shapes.add({
    name: opts.name ?? value.slice(0,48), geometry:'textbox',
    position:{left:x,top:y,width:w,height:h}, fill:'none', line:{fill:'none',width:0},
  });
  shape.text = value;
  shape.text.style = {
    typeface:opts.math ? MATH : FONT, fontSize:opts.size ?? 32,
    bold:opts.bold ?? false, color:opts.color ?? C.ink,
    alignment:opts.align ?? 'left', verticalAlignment:'top',
    autoFit:'none', wrap:'square',
    insets:{left:0,right:0,top:0,bottom:0},
  };
  return shape;
}
function body(s, value, y, opts={}) { return text(s,value,64,y,1152,opts.h??88,opts); }
function eq(s, value, y, opts={}) { return body(s,value,y,{math:true,size:44,h:74,...opts}); }
function slide(title, section, notes='') {
  const s = p.slides.add();
  s.background.fill = C.white;
  slides.push({number:slides.length+1,title,section});
  text(s,title,64,40,1152,76,{size:44,bold:true,name:'Slide title'});
  text(s,`Conspect §${section}`,64,682,800,24,{size:18,color:C.muted});
  text(s,String(slides.length),1140,682,76,24,{size:18,color:C.muted,align:'right'});
  s.speakerNotes.textFrame.setText(
    `Source: lectures/lecture-04-limit-theorems.tex, section ${section}.\n`+
    `Repository: https://github.com/EgorShibaev/Scientific_computing_2026\n${notes}`
  );
  return s;
}
async function data(name) {
  const lines = (await fs.readFile(path.join(repo,'figures/data',name),'utf8')).trim().split(/\n/);
  const names = lines.shift().split(/\s+/);
  return lines.map(line=>Object.fromEntries(line.trim().split(/\s+/).map((v,i)=>[names[i],Number(v)])));
}
function series(rows, x, y, name, color, style='solid', opts={}) {
  return {name, xValues:rows.map(r=>r[x]), values:rows.map(r=>r[y]),
    line:{fill:opts.markers?'none':color,width:opts.width??3.5,style},
    marker:opts.markers?{symbol:'circle',size:7}:{symbol:'none'},
    fill:color,
  };
}
function chart(s, seriesList, opts={}) {
  chartIndex++;
  chartOwners.add(slides.length);
  const axis = (title,min,max,majorUnit,format='0.0') => ({
    visible:true,title:{text:title,textStyle:{typeface:FONT,fontSize:23,fill:C.ink}},
    min,max,...(majorUnit===undefined?{}:{majorUnit}),numberFormatCode:format,
    textStyle:{typeface:FONT,fontSize:22,fill:C.muted},
    line:{fill:'#9BAABA',width:1},majorGridlines:{fill:C.grid,width:1},minorGridlines:null,
  });
  const ch=s.charts.add('scatter',{
    position:{left:opts.x??64,top:opts.y??146,width:opts.w??1152,height:opts.h??448},
    ...(opts.title?{title:opts.title,titleTextStyle:{typeface:FONT,fontSize:28,bold:true,fill:C.ink}}:{}),
    series:seriesList, scatterOptions:{style:seriesList.some(v=>v.marker?.symbol==='circle')?'lineWithMarkers':'line'},
    hasLegend:opts.legend!==false,
    legend:{position:'top',overlay:false,textStyle:{typeface:FONT,fontSize:22,fill:C.ink}},
    xAxis:axis(opts.xTitle??'',opts.xMin,opts.xMax,opts.xStep,opts.xFormat??'0'),
    yAxis:axis(opts.yTitle??'',opts.yMin,opts.yMax,opts.yStep,opts.yFormat??'0.0'),
    chartFill:C.white,chartLine:{fill:'none',width:0},
    plotAreaFill:C.white,plotAreaLine:{fill:'none',width:0},
  });
  const markerStyles=seriesList.flatMap((v,i)=>v.marker?.symbol==='circle'?
    [{seriesIndex:i+1,color:v.fill.replace('#',''),size:8}]:[]);
  logPlan.push({chartIndex,xLog:!!opts.xLog,yLog:!!opts.yLog,
    axesAtMin:true,straightLines:true,...(markerStyles.length?{markerStyles}:{})});
  return ch;
}
function table(s, values, widths, y=230, rowHeight=78, size=28) {
  tableOwners.add(slides.length);
  const t=s.tables.add({rows:values.length,columns:values[0].length,
    left:64,top:y,width:1152,height:values.length*rowHeight,
    columnWidths:widths,values});
  t.styleOptions={headerRow:false,bandedRows:false};
  t.borders.assign({fill:'#D9E2EC',width:1,style:'solid'});
  for(let r=0;r<values.length;r++) {
    t.rows[r].height=rowHeight;
    for(let c=0;c<values[0].length;c++) {
      const cell=t.getCell(r,c);
      cell.fill=r===0?'#EDF3F8':C.white;
      cell.text.style={typeface:FONT,fontSize:size,color:C.ink,bold:r===0,
        verticalAlignment:'middle',autoFit:'none',insets:{left:16,right:12,top:12,bottom:10}};
    }
  }
  return t;
}

// 1. Title. The deck starts from the same waiting-time example as the chapter.
{
  const s=p.slides.add(); slides.push({number:1,title:'Samples, concentration, and limit theorems',section:'4'});
  s.background.fill=C.ink;
  text(s,'Scientific Computing 2026',64,62,1152,45,{size:28,color:'#BED3E4'});
  text(s,'Samples, concentration,\nand limit theorems',64,206,1152,210,{size:68,bold:true,color:C.white});
  text(s,'Lecture 4',64,537,1152,52,{size:34,color:C.white});
  s.speakerNotes.textFrame.setText('Source: lectures/lecture-04-limit-theorems.tex. Lecture4 follows sections4.1–4.6 of the cumulative course conspect.');
}
{
  const s=slide('One hundred waiting times','4.1');
  body(s,'Record 100 waits. Compute their average.\nRepeat with another 100 waits.',146,{size:34,h:104});
  eq(s,'Tᵢ ∼ Exp(0.2)       μ = 5 min       σ = 5 min',303,{size:44});
  body(s,'How far might either average be from five minutes?',440,{size:34});
  body(s,'The observations follow the same model as Chapter 2.',570,{size:25,color:C.muted});
}
{
  const s=slide('Samples and sampling distributions','4.1');
  body(s,'An i.i.d. sample has mutually independent observations\nwith the same distribution.',140,{h:96});
  eq(s,'X̄ₙ = (X₁ + ⋯ + Xₙ) / n',280,{size:52});
  body(s,'Before collection: random variables X₁, …, Xₙ.\nAfter collection: recorded values x₁, …, xₙ.',390,{h:90});
  body(s,'Repeat the whole sampling experiment. The distribution\nof the resulting averages is the sampling distribution.',527,{h:100});
}
{
  const s=slide('Standard deviation and standard error','4.1');
  body(s,'For i.i.d. observations with finite variance:',140);
  eq(s,'E[X̄ₙ] = μ       Var(X̄ₙ) = σ² / n',230,{size:50});
  eq(s,'SE(X̄ₙ) = σ / √n',334,{size:56,color:C.blue});
  body(s,'One wait: SD = 5 minutes.\nAverage of 100 waits: SE = 0.5 minutes.',450,{size:32,h:90});
  body(s,'Individual waits keep their spread as the sample grows.',588,{size:26,color:C.muted});
}
{
  const s=slide('The exact distribution of an average','4.1','Figure4.1. The Gamma second parameter is a rate. Data: figures/data/ch4-sampling-density.dat.');
  const d=await data('ch4-sampling-density.dat');
  chart(s,[series(d,'x','n1','n = 1',C.blue),series(d,'x','n4','n = 4',C.orange,'dashed'),series(d,'x','n25','n = 25',C.teal,'dotted')],
    {xTitle:'Average waiting time (minutes)',yTitle:'Density',xMin:0,xMax:16,xStep:2,yMin:0,yMax:.45,yStep:.1});
  body(s,'T̄ₙ ∼ Gamma(n, 0.2n), with rate 0.2n. The mean stays at five minutes.',618,{math:true,size:29,h:44});
}
{
  const s=slide('When the population variance is unknown','4.1');
  body(s,'Estimate the spread within the observed sample:',144);
  eq(s,'Sₙ² = [∑ᵢ₌₁ⁿ (Xᵢ − X̄ₙ)²] / (n − 1)',247,{size:48});
  body(s,'The denominator accounts for centering at the sample mean.\nWe derive the correction in the estimation chapter.',356,{size:30,h:90});
  eq(s,'Estimated SE(X̄ₙ) = Sₙ / √n       (n ≥ 2)',489,{size:44,color:C.blue});
  body(s,'The interpretation still depends on the sampling assumptions.',605,{size:26,color:C.muted});
}
{
  const s=slide('The probability of a large error','4.2');
  body(s,'Suppose the average wait should be within one minute\nof the population mean.',152,{size:34,h:104});
  eq(s,'P(|T̄₁₀₀ − 5| ≥ 1) = ?',312,{size:64});
  body(s,'The standard error gives an error scale.\nA probability statement needs more reasoning.',481,{size:34,h:110});
}
{
  const s=slide('Markov’s inequality','4.2','The proof uses the indicator expectation rule already introduced in Chapter2.');
  body(s,'Assume W ≥ 0, a > 0, and a finite expectation.',141,{size:32});
  eq(s,'W ≥ a · 1{W ≥ a}',231,{size:48});
  eq(s,'E[W] ≥ a · P(W ≥ a)',341,{size:48});
  eq(s,'P(W ≥ a) ≤ E[W] / a',461,{size:54,color:C.blue});
  body(s,'Frequent large values force the mean upward.',596,{size:29,color:C.muted});
}
{
  const s=slide('Why Markov can be conservative','4.2');
  body(s,'Any nonnegative wait with mean five minutes:',139);
  eq(s,'P(T ≥ 20) ≤ 5 / 20 = 0.25',217,{size:50});
  body(s,'Under the exponential model:',322,{size:30});
  eq(s,'P(T ≥ 20) = exp(−4) ≈ 0.0183',384,{size:48,color:C.blue});
  body(s,'The bound is attainable: probability ¼ at 20 and ¾ at 0.\nA mean alone cannot distinguish these distributions.',523,{size:29,h:100});
}
{
  const s=slide('Chebyshev’s inequality','4.2');
  body(s,'Let X have mean μ and finite variance σ². Choose ε > 0.',140,{size:31});
  eq(s,'W = (X − μ)²       a = ε²',226,{size:46});
  eq(s,'P(|X − μ| ≥ ε) = P(W ≥ ε²)',333,{size:46});
  eq(s,'P(|X − μ| ≥ ε) ≤ σ² / ε²',446,{size:52,color:C.blue});
  body(s,'Squaring deviations makes Markov apply to both tails.',587,{size:29,color:C.muted});
}
{
  const s=slide('A finite-sample guarantee','4.2');
  eq(s,'P(|X̄ₙ − μ| ≥ ε) ≤ min(1, σ² / (nε²))',146,{size:44});
  body(s,'For the inbox, ε = 1 minute and n = 100:',263,{size:30});
  eq(s,'P(|T̄₁₀₀ − 5| ≥ 1) ≤ 25 / 100 = 0.25',329,{size:44});
  body(s,'To make the bound at most δ, it suffices that',437,{size:30});
  eq(s,'n ≥ σ² / (δε²)       δ = 0.05 gives n = 500',505,{size:42,color:C.blue});
  body(s,'Use the true variance or a known upper bound. A sample-variance\nplug-in needs further justification.',603,{size:24,h:61,color:C.muted});
}
{
  const s=slide('The weak law of large numbers','4.3');
  body(s,'For i.i.d. observations with mean μ and finite variance,\nevery fixed tolerance ε > 0 satisfies',141,{size:31,h:98});
  eq(s,'P(|X̄ₙ − μ| > ε) → 0     as n → ∞',283,{size:52,color:C.blue});
  body(s,'Chebyshev proves this directly:',406,{size:30});
  eq(s,'P(|X̄ₙ − μ| > ε) ≤ σ² / (nε²) → 0',475,{size:44});
  body(s,'This is convergence in probability.',601,{size:30});
}
{
  const s=slide('Running averages fluctuate','4.3','Figure4.2. Three independent simulated sequences, fixed seeds104729,130363,155921. Data: figures/data/ch4-running-means.dat.');
  const d=await data('ch4-running-means.dat');
  chart(s,[series(d,'n','path1','Dataset 1',C.blue),series(d,'n','path2','Dataset 2',C.orange,'dashed'),series(d,'n','path3','Dataset 3',C.teal,'dash-dot'),
    {name:'Mean = 5',xValues:[1,1000],values:[5,5],line:{fill:C.muted,width:2,style:'dotted'},marker:{symbol:'none'}}],
    {xTitle:'Number of observations n (log scale)',yTitle:'Running average (minutes)',xMin:1,xMax:1000,xLog:true,yMin:0,yMax:12,yStep:2,yFormat:'0'});
  body(s,'A new observation can increase the error. These paths illustrate the LLN.',618,{size:26,h:48});
}
{
  const s=slide('The scope of the law of large numbers','4.3');
  body(s,'The fixed-tolerance error probability tends to zero\nacross repeated datasets.',144,{size:34,h:102});
  body(s,'The general i.i.d. LLN needs only E[|X₁|] < ∞.\nFinite variance is enough for our short proof.',314,{size:32,h:100});
  body(s,'Sampling bias remains: recording only short waits\nlearns the mean of that selected population.',493,{size:32,h:108});
}
{
  const s=slide('The shape of the sampling error','4.4');
  body(s,'The LLN makes the error small.\nWhat distribution describes the remaining fluctuations?',148,{size:34,h:116});
  eq(s,'X̄ₙ − μ       has standard deviation σ / √n',320,{size:44});
  body(s,'The exponential example has an exact Gamma answer.\nFor a complicated measurement or loss, we need an approximation.',482,{size:31,h:110});
}
{
  const s=slide('Standardized sampling error','4.4');
  body(s,'Measure the error in standard-error units:',148,{size:34});
  eq(s,'Zₙ = (X̄ₙ − μ) / (σ / √n)',252,{size:56,color:C.blue});
  eq(s,'E[Zₙ] = 0       Var(Zₙ) = 1',376,{size:48});
  body(s,'Rescaling keeps the shrinking fluctuations visible.\nThe new claim concerns their distributional shape.',520,{size:31,h:108});
}
{
  const s=slide('The central limit theorem','4.4');
  body(s,'Assume i.i.d. observations with mean μ and 0 < σ² < ∞.',136,{size:30});
  eq(s,'P(Zₙ ≤ z) → Φ(z)     as n → ∞',226,{size:50,color:C.blue});
  body(s,'For every real z: convergence in distribution\nto the standard Gaussian.',324,{size:31,h:90});
  eq(s,'X̄ₙ ≈ N(μ, σ² / n)',464,{size:50});
  body(s,'Gaussian observations give this law exactly for every n.\nThe original observations keep their own distribution.',574,{size:26,h:74,color:C.muted});
}
for (const pair of [[1,4],[25,100]]) {
  const s=slide(pair[0]===1?'The CLT at small sample sizes':'The CLT at larger sample sizes','4.4',
    `Figure4.3. Exact standardized Gamma densities. n=${pair.join(',')}. Same x and y limits on both CLT slides. Data: figures/data/ch4-clt-n*.dat.`);
  for(let j=0;j<2;j++) {
    const n=pair[j], d=await data(`ch4-clt-n${n}.dat`);
    chart(s,[series(d,'z','exact','Exact',C.blue),series(d,'z','normal','Normal',C.orange,'dashed')],
      {x:64+j*590,y:140,w:562,h:444,title:`n = ${n}`,xTitle:'Standardized average z',yTitle:'Density',xMin:-4,xMax:5,xStep:2,yMin:0,yMax:1.1,yStep:.5});
  }
  body(s,pair[0]===1?'The support starts at −√n. Small-sample averages remain asymmetric.':'The same axes reveal the change in shape as n grows.',615,{size:28,h:48});
}
{
  const s=slide('One minute equals two standard errors','4.4');
  eq(s,'n = 100       SE(T̄₁₀₀) = 5 / √100 = 0.5',149,{size:46});
  eq(s,'P(|T̄₁₀₀ − 5| > 1) = P(|Z₁₀₀| > 2)',284,{size:48});
  eq(s,'≈ 2[1 − Φ(2)] ≈ 0.04550',425,{size:58,color:C.blue});
  body(s,'About 4.55% under the Gaussian approximation.',584,{size:31});
}
{
  const s=slide('Bound, approximation, and exact probability','4.4',
    'For n100 the exact Gamma lower tail is0.0171083130351 and upper tail0.0278637398905. Their sum is0.0449720529257. G_n is the CDF of Gamma(n,0.2n).');
  body(s,'The Gamma model lets us check the approximation:',138,{size:30});
  eq(s,'P(T̄₁₀₀ < 4) ≈ 0.017108',211,{size:41});
  eq(s,'P(T̄₁₀₀ > 6) ≈ 0.027864',280,{size:41});
  table(s,[['Method','Value','Meaning'],['Chebyshev','≤ 0.25000','Upper bound'],['CLT','≈ 0.04550','Approximation'],['Exact Gamma','≈ 0.04497','Exact model, rounded']],[360,290,502],377,65,27);
}
{
  const s=slide('Error probability across sample sizes','4.4','Figure4.4. Full data: figures/data/ch4-tail-comparison.dat. Values are exact Gamma tails, Chebyshev bounds capped at1, and Gaussian approximations.');
  const d=await data('ch4-tail-comparison.dat');
  chart(s,[series(d,'n','exact','Exact Gamma',C.blue),series(d,'n','chebyshev','Chebyshev bound',C.orange,'dashed'),series(d,'n','clt','CLT approximation',C.teal,'dotted')],
    {xTitle:'Number of observations n',yTitle:'P(|average − 5| > 1), log scale',xMin:0,xMax:200,xStep:50,yMin:.003,yMax:1,yLog:true,yFormat:'0.000'});
  body(s,'The exact and CLT curves nearly coincide here. Chebyshev stays an upper bound.',615,{size:26,h:56});
}
{
  const s=slide('Finite-sample accuracy of the CLT','4.4');
  body(s,'There is no universal sample size, such as 30,\nthat guarantees a useful Gaussian approximation.',147,{size:34,h:112});
  body(s,'Skewness and rare extreme values can delay convergence.',323,{size:32,h:80});
  body(s,'A small absolute CDF error can still mean a large\nrelative error for a tiny tail probability.',479,{size:32,h:108});
}
{
  const s=slide('A shared calibration error','4.5');
  eq(s,'Xᵢ = μ + B + εᵢ',149,{size:56});
  body(s,'B stays fixed within one dataset.\nA new independently calibrated dataset gets a fresh B.',261,{size:31,h:108});
  body(s,'The reading errors εᵢ are centered and independent,\nand independent of the centered calibration error B.',404,{size:29,h:100});
  eq(s,'X̄ₙ = μ + B + (ε₁ + ⋯ + εₙ) / n',553,{size:43,color:C.blue});
}
{
  const s=slide('Covariance leaves a variance floor','4.5');
  body(s,'Each reading has variance σ². Distinct pairs have\ncorrelation ρ, with 0 ≤ ρ ≤ 1.',136,{size:31,h:98});
  eq(s,'Var(X̄ₙ) = [nσ² + n(n − 1)ρσ²] / n²',277,{size:44});
  eq(s,'= σ²[ρ + (1 − ρ) / n]',382,{size:52,color:C.blue});
  body(s,'n diagonal covariance terms and n(n − 1) off-diagonal terms.',490,{size:27,h:66});
  eq(s,'Var(X̄ₙ) → ρσ²     as n → ∞',566,{size:44});
}
{
  const s=slide('One hundred correlated readings','4.5','Figure4.5. Pairwise correlationrho0.1. n_eff100/[1+99*.1]=9.1743. This compares mean variances, not full distributions. Data: ch4-dependent-averages.dat.');
  const d=await data('ch4-dependent-averages.dat');
  chart(s,[series(d,'n','independent','Independent',C.blue),series(d,'n','dependent','Correlation ρ = 0.1',C.orange,'dashed'),
    {name:'Floor ≈ 0.316',xValues:[1,1000],values:[.316227766017,.316227766017],line:{fill:C.muted,width:2,style:'dotted'},marker:{symbol:'none'}}],
    {xTitle:'Number of observations n (log scale)',yTitle:'Standard error / individual SD',xMin:1,xMax:1000,xLog:true,yMin:0,yMax:1,yStep:.2});
  body(s,'For n = 100, Var(X̄ₙ) = 0.109σ²: the same mean variance\nas about 9.17 independent readings.',610,{size:25,h:66});
}
{
  const s=slide('Finite mean and finite variance','4.5');
  body(s,'For i.i.d. Student observations with ν = 3/2:',145,{size:34});
  eq(s,'E[|X₁|] < ∞       Var(X₁) = ∞',245,{size:53});
  body(s,'The general LLN applies: the sample mean converges\nin probability to zero.',375,{size:33,h:102});
  body(s,'The finite-variance Chebyshev argument and classical CLT\ndo not apply. There is no finite σ for σ / √n.',537,{size:30,h:100});
}
{
  const s=slide('Cauchy averages keep the same spread','4.5',
    'Figure4.6. Left standard Gaussian observations; right standard Cauchy t1 observations. Separate y-axis scales. Exact densities. Data: figures/data/ch4-heavy-tail-means.dat.');
  const d=await data('ch4-heavy-tail-means.dat');
  chart(s,[series(d,'x','n1','n = 1',C.blue),series(d,'x','n4','n = 4',C.orange,'dashed'),series(d,'x','n25','n = 25',C.teal,'dotted')],
    {x:64,y:135,w:562,h:415,title:'Standard Gaussian',xTitle:'Sample average',yTitle:'Density',xMin:-4,xMax:4,xStep:2,yMin:0,yMax:2.1,yStep:.5});
  chart(s,[series(d,'x','cauchy','Every n',C.blue)],
    {x:654,y:135,w:562,h:415,title:'Standard Cauchy',xTitle:'Sample average',yTitle:'Density',xMin:-4,xMax:4,xStep:2,yMin:0,yMax:.35,yStep:.1});
  eq(s,'X̄ₙ ∼ t₁       P(|X̄ₙ| > 1) = 1/2     for every n',572,{size:37,h:52});
  body(s,'The Cauchy mean is undefined. Zero is its symmetry center. Panel scales differ.',635,{size:24,h:38,color:C.muted});
}
{
  const s=slide('Monte Carlo estimation','4.6');
  body(s,'To estimate I = E[g(X)], draw independent observations\nfrom the target distribution and average their evaluations.',139,{size:31,h:100});
  eq(s,'Îₙ = [g(X₁) + ⋯ + g(Xₙ)] / n',288,{size:52,color:C.blue});
  body(s,'E[|g(X)|] < ∞ gives the LLN.\nFinite positive τ² also gives the CLT.',398,{size:29,h:84});
  eq(s,'SE(Îₙ) = τ / √n       τ² = Var(g(X))',484,{size:44});
  body(s,'When τ is unknown, estimate SE as Sᵧ / √n, using\nthe sample standard deviation of the values g(Xᵢ).',596,{size:25,h:70,color:C.muted});
}
{
  const s=slide('A Monte Carlo example with a known answer','4.6');
  eq(s,'T ∼ Exp(0.2)       g(t) = exp(−t)',144,{size:46});
  body(s,'Time is in minutes. The exponent uses one per minute.',242,{size:28});
  eq(s,'I = E[g(T)] = 1/6       E[g(T)²] = 1/11',340,{size:44});
  eq(s,'τ² = 1/11 − 1/36 = 25/396',457,{size:50,color:C.blue});
  body(s,'The known value lets us check the numerical method.',599,{size:29});
}
{
  const s=slide('Precision has a computational cost','4.6');
  eq(s,'RMSE(Îₙ) = √E[(Îₙ − I)²] = τ / √n',143,{size:47});
  body(s,'Four times as many evaluations halves RMSE.\nA tenfold reduction costs one hundred times as many.',273,{size:31,h:98});
  eq(s,'n = 1000       RMSE ≈ 0.00795',404,{size:46});
  eq(s,'RMSE ≤ 0.005       needs n ≥ 2526',500,{size:45,color:C.blue});
  body(s,'An RMSE target does not bound the error in every run.',614,{size:26,h:45,color:C.muted});
}
{
  const s=slide('Monte Carlo error across repeated runs','4.6',
    'Figure4.7. Simulation uses2000 independent repetitions and fixed seed20260925. Each point estimates RMSE across repetitions. Data: figures/data/ch4-monte-carlo-error.dat.');
  const d=await data('ch4-monte-carlo-error.dat');
  chart(s,[series(d,'n','theory','Exact RMSE',C.blue),series(d,'n','simulated','Simulation (2,000 runs)',C.orange,'solid',{markers:true,width:0})],
    {xTitle:'Number of independent draws n (log scale)',yTitle:'Root mean squared error (log scale)',xMin:10,xMax:10000,xLog:true,yMin:.002,yMax:.1,yLog:true,yFormat:'0.000'});
  body(s,'The dots measure variation across independent runs, rather than one running path.',615,{size:26,h:56});
}
{
  const s=slide('Uncertainty in a test-set average','4.6');
  body(s,'Fix f before evaluation. Use i.i.d. test observations\nindependent of all data used to choose f.',135,{size:30,h:94});
  eq(s,'Lᵢ = ℓ(f(Xᵢ), Yᵢ)       R(f) = E[Lᵢ]',254,{size:41});
  eq(s,'R̂ₙ(f) = [L₁ + ⋯ + Lₙ] / n',334,{size:43});
  body(s,'Population accuracy 0.8, with 400 independent test examples:',438,{size:28});
  eq(s,'SE = √(0.8 × 0.2 / 400) = 0.02',501,{size:43,color:C.blue});
  body(s,'This measures test-sample variation. Choosing f on the same test set\nbreaks the fixed-model premise.',605,{size:24,h:60,color:C.muted});
}
{
  const s=slide('Batch size and the variance of an average','4.6');
  body(s,'At a fixed model, average b independent losses,\neach with variance τ².',140,{size:33,h:105});
  eq(s,'Var(batch average) = τ² / b',284,{size:50,color:C.blue});
  body(s,'A fourfold increase in b halves the standard deviation.',407,{size:31});
  body(s,'For a fixed dataset, sampling indices with replacement uses\nits empirical loss variance. Dependence and sampling\nwithout replacement require different variance calculations.',505,{size:28,h:140});
}
{
  const s=slide('What each result tells us','4.6');
  table(s,[['Result','Question it answers'],
    ['Chebyshev','How large can a finite-sample error probability be?'],
    ['Law of large numbers','Does the average approach the population quantity?'],
    ['Central limit theorem','What shape do the rescaled fluctuations approach?']],
    [410,742],168,100,29);
  body(s,'Independence, moment assumptions, and the sampling process\ndetermine which conclusion is justified.',590,{size:27,h:66});
}

await (await PresentationFile.exportPptx(p)).save(path.join(out,'candidate.pptx'));
await fs.writeFile(path.join(out,'log-axes.json'),JSON.stringify(logPlan,null,2)+'\n');
await fs.writeFile(path.join(out,'slide-map.json'),JSON.stringify(slides,null,2)+'\n');
await fs.writeFile(path.join(out,'requirements.json'),JSON.stringify({
  requiredNativeChartOwnerSlides:[...chartOwners],
  requiredNativeTableOwnerSlides:[...tableOwners],
  materializeLiteralChartWorkbooks:true,
  fontPolicy:{basis:'design',families:[FONT,MATH]},
  slideCount:slides.length,
},null,2)+'\n');
if(process.env.RENDER_PREVIEWS==='1') {
  await fs.mkdir(path.join(out,'previews'),{recursive:true});
  for(let i=0;i<slides.length;i++) {
    const blob=await p.export({slide:p.slides.getItem(i),format:'png',scale:1});
    await fs.writeFile(path.join(out,'previews',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
  }
}
console.log(JSON.stringify({slides:slides.length,nativeCharts:chartIndex,nativeTables:tableOwners.size,out},null,2));
