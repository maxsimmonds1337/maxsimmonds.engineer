# Programming Portfolio

## [Numerically Controlled Oscillator, C](./c/NCO.md)

**Start Date:** 01/07/2022

**End Date:** 30/07/2022

A numerically controlled oscillator is a method for generating a value that changes sinusoidally at a given frequency. Usually, sine waves and cosine waves are generated via a lookup table. This is an alternative method that doesn't require a large table of memory.

---

## [Markdown Graph Interpreter, Python](./Python/graphPlotter.md)

**Start Date:** 01/08/2022

**End Date:** 26/08/2022

When I was working on the [NCO, Numerically Controller Oscillator](./c/NCO.md) I realised that there was no convienent way to plot graphs in Markdown. The only thing that came close was [Mermaid](https://mermaid-js.github.io/mermaid/#/), which allows you to use text and code to generate diagrams, but no real _graphs_. So, graphPlotter is a python script that's called from a git hook, that searches through committed markdown files that have been modified, searches for the tag "```graphPlotter" and interprets the text after.

An example might be, to plot an arrow, :

```
```graphPlotter
-> 0 0 0.8 0 0.02 0.1
`` `
```

This would render:

![image](https://user-images.githubusercontent.com/58208872/190349504-6e1215de-5b5f-4f08-98f5-7c5d34f86025.png)

The alt text is then changed to the command, so that the data isn't lost.

---

## [CORS Proxy](./JS/CORS-proxy.md)

**Start Date:** 13/09/2022

**End Date:** 17/09/2022

I recently wanted to present (on my CV) my leetcode stats. Leetcode doesn't have a dedicated way of showing this data, unless you're logged in. In order to use their GraphQL API 

---

## [JS Wave Emulator](./JS/Wave/wave.html)

**Start Date:** 20/09/2022

**End Date:** 

Some javascript code that allows you to "drop" a stone into a virtual pond, and watch the waves it generates propagate. 

---
