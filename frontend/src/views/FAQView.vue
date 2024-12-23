<script setup>
const title = window.title
const contact = window.contact
</script>
<template>
  <p>来了？坐，欢迎来到 {{ title }}。</p>
  <p>
    众所周知，信息学的题目筛选起来是比较困难的，我们不知道一道题难还是简单。而且对于应该训练哪些题目完全没有头绪。特别是同一场比赛中的题目在难度上可以相差很大。有些题目适合我们当前水平，有些太难了，而有些又过于简单。此外，由于事先不知道题目的难度，我们经常因为看了题解而浪费了一个高质量但超出我们能力范围的好题目。
  </p>
  <p>而且有时候我们想与出题人进行对话，留下一些评论，讨论一些问题……</p>
  <p>这个时候 Rating System 出现了，于是 {{ title }} 就使用了这套系统。</p>
  <p>
    我们希望通过这个项目能够解决上面这个问题。通过对难度和质量进行量化，大家可以更容易地找到适合自己水平的题目来进行训练。
  </p>
  <h3>常见问题解答</h3>
  <p><strong>如何理解这些数字？</strong></p>
  <p>
    {{ title }} 提供了两个指标：难度和质量。难度是一个介于800到3500之间的数值，大致与
    <a href="https://codeforces.com/">Codeforces</a>
    的评分体系相对应。质量则是在0到5之间打分，5表示非常高质量，0表示非常无趣。虽然质量的评价相对主观一些，但它仍然是选择好题以及避开差题的一个不错的工具。
  </p>
  <p><strong>这些数字是如何计算出来的？</strong></p>
  <p>
    我们采用了一种民主投票机制，允许用户根据自己的判断给出对题目难度和质量的估计。这种做法旨在集合广大用户的智慧，以期得到更准确、更公正的结果。随着越来越多的人参与投票，每个题目的难度和质量分数也会逐渐趋于稳定，并且更加可靠。
  </p>
  <p><strong>我有意见或建议，该如何反馈？</strong></p>
  <p>
    目前 {{ title }} 刚刚起步，还有很多地方有待完善。发现BUG、发现槽点都可以联系我们，联系方式见下。
  </p>
  <p v-html="contact"></p>
  <p>
    如果是系统本身的问题，也可以在
    <a href="https://github.com/znpdco/rating-system">GitHub</a> 上提交 issue。
  </p>
  <p>祝各位在 {{ title }} 玩得愉快！（求不虐萌萌哒服务器～！）</p>
  <h3>相关条款</h3>
  <p>继续使用本服务代表您知情并同意下方条款。</p>
  <p><strong>使用条款</strong></p>
  <p>
    请您不要在网站中发布违反服务器所在地司法管辖区法律的言论。为了保证服务在中国大陆的可用性，也请您尽可能避免发表违反中国大陆法律的言论。
  </p>
  <p>如果您做出不合适的行为，您的评分权可能被取消。</p>
  <p><strong>隐私条款</strong></p>
  <p>您的评分以及评论会被实名保存，但我们会在匿名化后透露这些数据。</p>
  <p>除了整体的统计数据，我们不会随意分享细节数据。这些数据只会被分享给出题人或其它利益相关者。</p>
  <p><strong>免责声明</strong></p>
  <p>本网站原样提供用户的评价。不为此承担潜在的法律责任。</p>
  <p><strong>版权声明</strong></p>
  <p>本网站参考并修改了开源项目 CodeTiger927/USACO-Rating。下面是其开源协议。</p>
  <pre style="white-space: pre-wrap; word-wrap: break-word">
MIT License
Copyright (c) 2021 Alex Fan
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
</pre
  >
</template>
