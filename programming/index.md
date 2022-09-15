# Programming Portfolio

## [Numerically Controlled Oscillator, C](./c/NCO.md)

**Start Date:** 01/07/2022

**End Date:** 30/07/2022

A numerically controlled oscillator is a method for generating a value that changes sinusoidally at a given frequency. Usually, sine waves and cosine waves are generated via a lookup table. This is an alternative method that doesn't require a large table of memory.

---

## [Markdown Graph Interpreter, Python](./Python/graphPlotter.md)

**Start Date:** 01/07/2022

**End Date:** 30/07/2022

When I was working on the [NCO, Numerically Controller Oscillator](./c/NCO.md) I realised that there was no convienent way to plot graphs in Markdown. The only thing that came close was [Mermaid](https://mermaid-js.github.io/mermaid/#/), which allows you to use text and code to generate diagrams, but no real _graphs_. So, graphPlotter is a python script that's called from a git hook, that searches through committed markdown files that have been modified, searches for the tag "```graphPlotter" and interprets the text after.

An example might be, to plot an arrow, :

```
\```graphPlotter
-> 0 0 0.8 0 0.02 0.1
\```
```


---

## [Numerically Controlled Oscillator, C](./c/NCO.md)

**Start Date:** 01/07/2022

**End Date:** 30/07/2022

A numerically controlled oscillator is a method for generating a value that changes sinusoidally at a given frequency. Usually, sine waves and cosine waves are generated via a lookup table. This is an alternative method that doesn't require a large table of memory.

---l
