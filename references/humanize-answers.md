# 答案去 AI 味 / Humanize Answers(v2.0 新增)

> 何时读:Step 6 生成「改进后的参考回答」之后、写入任何 STAR 故事定稿之前。
> 装了 `humanizer` skill(jooray,基于 Wikipedia「Signs of AI writing」)就直接对文本跑它;
> 没装就按下面的清单自查。两者目标一致:**面试官听到的必须像这个人自己说的话。**

## 为什么这步不可跳过

2026 年的面试官(和 AI 面试的真人复核员)每天都在听 AI 写的答案,识别力已经训练出来了。
一段被听出 AI 味的"完美回答"传递的信息是:此人偷懒、且以为我听不出来——双重扣分,
比一段朴素但真实的回答伤害大得多。参考回答的价值是给用户一个**骨架**,
用户要用自己的词汇重讲;所以骨架本身必须先像人话。

## 检查清单(逐条过,中英答案通用)

1. **三段式排比** — "not only... but also..."、"从 X 到 Y 到 Z" 连用三个并列。
   人说话很少凑齐三个。砍成一个或两个。
2. **Em-dash 与分号密度** — 口语答案里几乎不该有;改成短句。
3. **AI 高频词** — delve / leverage / robust / seamless / crucial / 赋能 / 抓手 / 闭环 /
   沉淀 / 助力。全部换成具体动词。
4. **空洞归因** — "研究表明"、"业界普遍认为"、"It's widely recognized"。面试里只有
   "我当时看到的数据是——"。
5. **完美对称结构** — 每段都是"背景-动作-结果"等长三句,像模板灌出来的。
   打乱节奏:重要的部分多说,次要的一笔带过。
6. **过度总结句** — 每段结尾都来一句"这体现了我的 X 能力"。删掉,让面试官自己得出结论;
   最多在整个答案末尾点一次题。
7. **零瑕疵叙事** — 全程英明神武。真人故事有犹豫、有走弯路("我一开始判断错了,
   两天后发现……")——保留一处小挫折反而最可信。
8. **口语锚点缺失** — 加回真人说话的痕迹:具体的人名化称呼("我们 TL")、
   具体时间("大概去年三月")、具体数字(哪怕是约数)。

## 操作方式

- 生成参考回答 → 过清单 → 直接交付改后版本(不用展示改前版,除非用户想看差异)。
- storybank 故事定稿同样处理;`--action evolve` 更新版本时重过一遍。
- 提醒用户:参考回答是骨架,面试前要用自己的话重讲三遍——背诵痕迹本身就是 AI 味。

---

# English quick list

Rule of three overuse · em-dash/semicolon density · AI vocabulary (delve, leverage, robust,
seamless, crucial) · vague attribution ("studies show", "it's widely recognized") · perfectly
symmetric paragraph rhythm · trailing self-summaries ("this demonstrates my...") · flawless-hero
narratives (keep one honest stumble — it's the most credible sentence in the answer) · missing
oral anchors (real names/roles, rough dates, approximate numbers).

Deliver the humanized version directly; remind the user the reference answer is a skeleton —
retell it in your own words three times before the interview, because recitation itself reads as AI.
