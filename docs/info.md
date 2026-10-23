<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Calculates prediction error (e = x - mu) and updates internal state mu using gradient descent.
Includes an adaptive suppression gate (alert_gate) to reduce learning rate during high-variance input.
Apply 8-bit Q1.14 input values to ui_in and observe internal state mu on uo_out.

## How to test

Apply 8-bit Q1.14 input values to ui_in and observe internal state mu on uo_out.

## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any
